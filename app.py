import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Tuple
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Page configuration
st.set_page_config(
    page_title="BOB ATM Strategy Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Helper functions
@st.cache_data
def load_data():
    """Load and cache the combined dataset"""
    df = pd.read_csv('data/combined_locations.csv')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    return df

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in km"""
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def get_display_name(source: str) -> str:
    """Get display-friendly name for sources"""
    mapping = {
        'OBA Bank': 'OBA Supermarket',
        'Bravo Supermarket': 'Bravo Supermarket',
        'Bazarstore': 'Bazarstore'
    }
    return mapping.get(source, source)

def calculate_coverage_gaps(data: pd.DataFrame, bob_atms: pd.DataFrame, radius_km: float = 2.0):
    """Calculate locations with no BOB ATM within specified radius"""
    atm_types = ['ATM', 'A', 'atm', 'network_atm']
    competitor_atms = data[
        (data['type'].isin(atm_types)) &
        (data['source'] != 'Bank of Baku')
    ].copy()

    gaps = []
    for _, comp in competitor_atms.iterrows():
        distances = bob_atms.apply(
            lambda bob: haversine_distance(
                comp['latitude'], comp['longitude'],
                bob['latitude'], bob['longitude']
            ), axis=1
        )
        min_distance = distances.min() if len(distances) > 0 else float('inf')

        if min_distance > radius_km:
            gaps.append({
                'latitude': comp['latitude'],
                'longitude': comp['longitude'],
                'source': comp['source'],
                'address': comp['address'],
                'distance_to_bob': min_distance,
                'competitor_density': len(competitor_atms[
                    competitor_atms.apply(
                        lambda x: haversine_distance(
                            comp['latitude'], comp['longitude'],
                            x['latitude'], x['longitude']
                        ) <= 1.0, axis=1
                    )
                ])
            })

    return pd.DataFrame(gaps)

def calculate_roi_score(gap_row, retail_locations: pd.DataFrame):
    """Calculate ROI score for a location"""
    # Competition density (30%)
    gap_score = min(gap_row['distance_to_bob'] / 10, 1.0) * 30

    # Competitor density (40%)
    demand_score = min(gap_row['competitor_density'] / 10, 1.0) * 40

    # Retail proximity (30%)
    retail_distances = retail_locations.apply(
        lambda r: haversine_distance(
            gap_row['latitude'], gap_row['longitude'],
            r['latitude'], r['longitude']
        ), axis=1
    )
    nearest_retail = retail_distances.min() if len(retail_distances) > 0 else 10
    retail_score = max(0, (2.0 - nearest_retail) / 2.0) * 30

    return gap_score + demand_score + retail_score

# Load data
data = load_data()

# Sidebar
st.sidebar.markdown("# 🏦 BOB ATM Strategy")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "🗺️ Interactive Map", "🎯 Coverage Gaps",
     "🏪 Retail Opportunities", "📈 Competitor Analysis", "💰 ROI Rankings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

# Global filters
atm_types = ['ATM', 'A', 'atm', 'network_atm']
bank_atms = data[data['type'].isin(atm_types)]
bob_atms = data[(data['source'] == 'Bank of Baku') & (data['type'].isin(atm_types))]
competitor_atms = data[(data['type'].isin(atm_types)) & (data['source'] != 'Bank of Baku')]

branch_types = ['Branch', 'branch', 'Store', 'store']
retail_locations = data[data['type'].isin(branch_types)]

selected_banks = st.sidebar.multiselect(
    "Select Banks",
    options=sorted(bank_atms['source'].unique()),
    default=sorted(bank_atms['source'].unique())
)

radius_km = st.sidebar.slider(
    "Coverage Radius (km)",
    min_value=0.5,
    max_value=5.0,
    value=2.0,
    step=0.5
)

# Main content based on page selection
if page == "📊 Overview":
    st.markdown('<div class="main-header">Bank of Baku ATM Strategy Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("BOB ATMs", len(bob_atms), delta=None)

    with col2:
        st.metric("Total Market ATMs", len(bank_atms), delta=None)

    with col3:
        market_share = (len(bob_atms) / len(bank_atms) * 100) if len(bank_atms) > 0 else 0
        st.metric("Market Share", f"{market_share:.1f}%", delta=None)

    with col4:
        leader = bank_atms['source'].value_counts().iloc[0]
        st.metric("Market Leader ATMs", leader, delta=None)

    with col5:
        gap_to_leader = leader - len(bob_atms)
        st.metric("Gap to Leader", gap_to_leader, delta=None, delta_color="inverse")

    st.markdown("---")

    # Market share chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Market Share by Bank")
        bank_counts = bank_atms['source'].value_counts().reset_index()
        bank_counts.columns = ['Bank', 'ATM Count']

        fig = px.bar(
            bank_counts,
            x='ATM Count',
            y='Bank',
            orientation='h',
            color='ATM Count',
            color_continuous_scale='Blues',
            title='ATM Distribution by Bank'
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Geographic Distribution")
        fig = px.scatter_mapbox(
            bank_atms[bank_atms['source'].isin(selected_banks)],
            lat='latitude',
            lon='longitude',
            color='source',
            size_max=10,
            zoom=10,
            mapbox_style="open-street-map",
            title='All Bank ATM Locations',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    # Coverage gaps preview
    st.markdown("---")
    st.subheader(f"Coverage Gap Analysis (>{radius_km}km from BOB ATM)")

    gaps_df = calculate_coverage_gaps(data, bob_atms, radius_km)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Coverage Gaps", len(gaps_df))
    with col2:
        avg_distance = gaps_df['distance_to_bob'].mean() if len(gaps_df) > 0 else 0
        st.metric("Avg Distance to BOB", f"{avg_distance:.1f} km")
    with col3:
        avg_density = gaps_df['competitor_density'].mean() if len(gaps_df) > 0 else 0
        st.metric("Avg Competitor Density", f"{avg_density:.1f}")

elif page == "🗺️ Interactive Map":
    st.markdown('<div class="main-header">Interactive ATM Location Map</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Map controls
    col1, col2, col3 = st.columns(3)

    with col1:
        show_bob = st.checkbox("Show BOB ATMs", value=True)
    with col2:
        show_competitors = st.checkbox("Show Competitor ATMs", value=True)
    with col3:
        show_retail = st.checkbox("Show Retail Locations", value=False)

    # Create map
    fig = go.Figure()

    if show_bob:
        fig.add_trace(go.Scattermapbox(
            lat=bob_atms['latitude'],
            lon=bob_atms['longitude'],
            mode='markers',
            marker=dict(size=12, color='#1f77b4'),
            name='BOB ATMs',
            text=bob_atms['address'],
            hovertemplate='<b>Bank of Baku</b><br>%{text}<extra></extra>'
        ))

    if show_competitors:
        for bank in selected_banks:
            if bank != 'Bank of Baku':
                bank_data = competitor_atms[competitor_atms['source'] == bank]
                fig.add_trace(go.Scattermapbox(
                    lat=bank_data['latitude'],
                    lon=bank_data['longitude'],
                    mode='markers',
                    marker=dict(size=8, opacity=0.6),
                    name=bank,
                    text=bank_data['address'],
                    hovertemplate=f'<b>{bank}</b><br>%{{text}}<extra></extra>'
                ))

    if show_retail:
        fig.add_trace(go.Scattermapbox(
            lat=retail_locations['latitude'],
            lon=retail_locations['longitude'],
            mode='markers',
            marker=dict(size=6, color='green', symbol='circle'),
            name='Retail Locations',
            text=retail_locations.apply(
                lambda x: f"{get_display_name(x['source'])}<br>{x['address']}", axis=1
            ),
            hovertemplate='%{text}<extra></extra>'
        ))

    # Calculate center
    center_lat = data['latitude'].mean()
    center_lon = data['longitude'].mean()

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10
        ),
        height=700,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Location statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("BOB ATMs Visible", len(bob_atms) if show_bob else 0)
    with col2:
        competitor_count = len(competitor_atms[competitor_atms['source'].isin(selected_banks)])
        st.metric("Competitor ATMs Visible", competitor_count if show_competitors else 0)
    with col3:
        st.metric("Retail Locations Visible", len(retail_locations) if show_retail else 0)
    with col4:
        total_visible = (
            (len(bob_atms) if show_bob else 0) +
            (competitor_count if show_competitors else 0) +
            (len(retail_locations) if show_retail else 0)
        )
        st.metric("Total Locations Visible", total_visible)

elif page == "🎯 Coverage Gaps":
    st.markdown('<div class="main-header">Coverage Gap Analysis</div>', unsafe_allow_html=True)
    st.markdown(f"Identifying competitor locations with no BOB ATM within {radius_km}km")
    st.markdown("---")

    gaps_df = calculate_coverage_gaps(data, bob_atms, radius_km)

    if len(gaps_df) == 0:
        st.success("No coverage gaps found! BOB has excellent market coverage.")
    else:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Gaps", len(gaps_df))
        with col2:
            st.metric("Avg Distance to BOB", f"{gaps_df['distance_to_bob'].mean():.1f} km")
        with col3:
            st.metric("Max Distance to BOB", f"{gaps_df['distance_to_bob'].max():.1f} km")
        with col4:
            st.metric("Avg Competitor Density", f"{gaps_df['competitor_density'].mean():.1f}")

        st.markdown("---")

        # Map of coverage gaps
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Coverage Gap Map")

            fig = go.Figure()

            # Add BOB ATMs
            fig.add_trace(go.Scattermapbox(
                lat=bob_atms['latitude'],
                lon=bob_atms['longitude'],
                mode='markers',
                marker=dict(size=12, color='blue'),
                name='BOB ATMs',
                text=bob_atms['address'],
                hovertemplate='<b>BOB ATM</b><br>%{text}<extra></extra>'
            ))

            # Add coverage gaps
            fig.add_trace(go.Scattermapbox(
                lat=gaps_df['latitude'],
                lon=gaps_df['longitude'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=gaps_df['distance_to_bob'],
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Distance<br>to BOB (km)")
                ),
                name='Coverage Gaps',
                text=gaps_df.apply(
                    lambda x: f"{x['source']}<br>{x['address']}<br>Distance: {x['distance_to_bob']:.1f}km<br>Competitors nearby: {x['competitor_density']}",
                    axis=1
                ),
                hovertemplate='%{text}<extra></extra>'
            ))

            center_lat = gaps_df['latitude'].mean()
            center_lon = gaps_df['longitude'].mean()

            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=10
                ),
                height=600,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Gap Distribution")

            # Distance distribution
            fig = px.histogram(
                gaps_df,
                x='distance_to_bob',
                nbins=20,
                title='Distance to Nearest BOB ATM',
                labels={'distance_to_bob': 'Distance (km)', 'count': 'Frequency'}
            )
            fig.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Competitor density distribution
            fig = px.histogram(
                gaps_df,
                x='competitor_density',
                nbins=15,
                title='Competitor Density at Gaps',
                labels={'competitor_density': 'Competitors within 1km', 'count': 'Frequency'}
            )
            fig.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Top gaps by source
        st.markdown("---")
        st.subheader("Coverage Gaps by Competitor Bank")

        gaps_by_source = gaps_df['source'].value_counts().reset_index()
        gaps_by_source.columns = ['Bank', 'Gap Count']

        fig = px.bar(
            gaps_by_source,
            x='Gap Count',
            y='Bank',
            orientation='h',
            color='Gap Count',
            color_continuous_scale='Reds',
            title='Number of Unserved Competitor Locations by Bank'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Detailed table
        st.markdown("---")
        st.subheader("Top 20 Coverage Gaps")

        top_gaps = gaps_df.nlargest(20, 'competitor_density')[
            ['source', 'address', 'distance_to_bob', 'competitor_density']
        ].copy()
        top_gaps.columns = ['Competitor Bank', 'Address', 'Distance to BOB (km)', 'Competitors Nearby']
        top_gaps['Distance to BOB (km)'] = top_gaps['Distance to BOB (km)'].round(2)

        st.dataframe(top_gaps, use_container_width=True, height=400)

elif page == "🏪 Retail Opportunities":
    st.markdown('<div class="main-header">Retail Partnership Opportunities</div>', unsafe_allow_html=True)
    st.markdown("High foot-traffic retail locations for ATM placement")
    st.markdown("---")

    # Calculate retail opportunities (retail locations far from BOB)
    retail_opps = []
    for _, retail in retail_locations.iterrows():
        distances_to_bob = bob_atms.apply(
            lambda bob: haversine_distance(
                retail['latitude'], retail['longitude'],
                bob['latitude'], bob['longitude']
            ), axis=1
        )
        min_distance = distances_to_bob.min() if len(distances_to_bob) > 0 else float('inf')

        # Count nearby competitors
        competitor_count = len(competitor_atms[
            competitor_atms.apply(
                lambda x: haversine_distance(
                    retail['latitude'], retail['longitude'],
                    x['latitude'], x['longitude']
                ) <= 0.5, axis=1
            )
        ])

        if min_distance > 1.0:  # More than 1km from BOB
            retail_opps.append({
                'source': retail['source'],
                'address': retail['address'],
                'latitude': retail['latitude'],
                'longitude': retail['longitude'],
                'distance_to_bob': min_distance,
                'competitor_density': competitor_count,
                'opportunity_score': (min_distance / 10) * 50 + (competitor_count / 10) * 50
            })

    retail_opps_df = pd.DataFrame(retail_opps)

    if len(retail_opps_df) == 0:
        st.success("All retail locations are well-covered by BOB ATMs!")
    else:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Opportunities", len(retail_opps_df))
        with col2:
            oba_count = len(retail_opps_df[retail_opps_df['source'] == 'OBA Bank'])
            st.metric("OBA Supermarkets", oba_count)
        with col3:
            bravo_count = len(retail_opps_df[retail_opps_df['source'] == 'Bravo Supermarket'])
            st.metric("Bravo Supermarkets", bravo_count)
        with col4:
            bazar_count = len(retail_opps_df[retail_opps_df['source'] == 'Bazarstore'])
            st.metric("Bazarstores", bazar_count)

        st.markdown("---")

        # Map and distribution
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Retail Opportunity Map")

            top_20 = retail_opps_df.nlargest(20, 'opportunity_score')

            fig = go.Figure()

            # Add BOB ATMs
            fig.add_trace(go.Scattermapbox(
                lat=bob_atms['latitude'],
                lon=bob_atms['longitude'],
                mode='markers',
                marker=dict(size=10, color='blue'),
                name='BOB ATMs',
                text=bob_atms['address'],
                hovertemplate='<b>BOB ATM</b><br>%{text}<extra></extra>'
            ))

            # Add retail opportunities
            fig.add_trace(go.Scattermapbox(
                lat=top_20['latitude'],
                lon=top_20['longitude'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=top_20['opportunity_score'],
                    colorscale='Greens',
                    showscale=True,
                    colorbar=dict(title="Opportunity<br>Score")
                ),
                name='Retail Opportunities',
                text=top_20.apply(
                    lambda x: f"{get_display_name(x['source'])}<br>{x['address']}<br>Distance: {x['distance_to_bob']:.1f}km<br>Competitors: {x['competitor_density']}<br>Score: {x['opportunity_score']:.0f}",
                    axis=1
                ),
                hovertemplate='%{text}<extra></extra>'
            ))

            center_lat = top_20['latitude'].mean()
            center_lon = top_20['longitude'].mean()

            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=10
                ),
                height=600,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Opportunities by Chain")

            opps_by_chain = retail_opps_df.groupby('source').agg({
                'opportunity_score': 'mean',
                'source': 'count'
            }).reset_index(drop=True)
            opps_by_chain.columns = ['Chain', 'Avg Score', 'Count']
            opps_by_chain['Chain'] = retail_opps_df.groupby('source').groups.keys()
            opps_by_chain['Chain'] = opps_by_chain['Chain'].apply(get_display_name)

            fig = px.bar(
                opps_by_chain,
                x='Count',
                y='Chain',
                orientation='h',
                color='Avg Score',
                color_continuous_scale='Greens',
                title='Opportunities by Retail Chain'
            )
            fig.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Top 20 opportunities table
        st.markdown("---")
        st.subheader("Top 20 Retail Partnership Opportunities")

        top_20_display = retail_opps_df.nlargest(20, 'opportunity_score')[
            ['source', 'address', 'distance_to_bob', 'competitor_density', 'opportunity_score']
        ].copy()
        top_20_display['source'] = top_20_display['source'].apply(get_display_name)
        top_20_display.columns = ['Retail Chain', 'Address', 'Distance to BOB (km)',
                                   'Competitors Nearby', 'Opportunity Score']
        top_20_display['Distance to BOB (km)'] = top_20_display['Distance to BOB (km)'].round(2)
        top_20_display['Opportunity Score'] = top_20_display['Opportunity Score'].round(1)

        st.dataframe(top_20_display, use_container_width=True, height=400)

elif page == "📈 Competitor Analysis":
    st.markdown('<div class="main-header">Competitor Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Market share comparison
    st.subheader("Market Position Analysis")

    bank_stats = bank_atms.groupby('source').agg({
        'source': 'count',
        'latitude': lambda x: x.count(),
        'longitude': lambda x: x.count()
    }).reset_index()
    bank_stats.columns = ['Bank', 'ATM Count', 'lat_count', 'lon_count']
    bank_stats = bank_stats[['Bank', 'ATM Count']].sort_values('ATM Count', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            bank_stats,
            x='ATM Count',
            y='Bank',
            orientation='h',
            color='ATM Count',
            color_continuous_scale='Blues',
            title='ATM Market Share by Bank'
        )
        fig.update_layout(height=500, showlegend=False)
        fig.add_vline(x=len(bob_atms), line_dash="dash", line_color="red",
                     annotation_text="BOB Current Position")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Market share pie
        fig = px.pie(
            bank_stats,
            values='ATM Count',
            names='Bank',
            title='Market Share Distribution',
            hole=0.4
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Geographic density analysis
    st.subheader("Geographic Density Heatmap")

    # Select bank for comparison
    comparison_bank = st.selectbox(
        "Compare BOB with:",
        options=[b for b in bank_atms['source'].unique() if b != 'Bank of Baku']
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Bank of Baku** ({len(bob_atms)} ATMs)")
        fig = px.density_mapbox(
            bob_atms,
            lat='latitude',
            lon='longitude',
            radius=15,
            zoom=10,
            mapbox_style="open-street-map",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        comparison_data = bank_atms[bank_atms['source'] == comparison_bank]
        st.markdown(f"**{comparison_bank}** ({len(comparison_data)} ATMs)")
        fig = px.density_mapbox(
            comparison_data,
            lat='latitude',
            lon='longitude',
            radius=15,
            zoom=10,
            mapbox_style="open-street-map",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Co-location analysis
    st.subheader("Competitor Co-location Analysis")
    st.markdown("How many competitor ATMs are within 500m of each other?")

    banks = sorted([b for b in bank_atms['source'].unique() if b != 'Bank of Baku'])
    co_location_matrix = pd.DataFrame(index=banks, columns=banks, data=0)

    for bank1 in banks:
        bank1_atms = bank_atms[bank_atms['source'] == bank1]
        for bank2 in banks:
            bank2_atms = bank_atms[bank_atms['source'] == bank2]
            count = 0
            for _, atm1 in bank1_atms.iterrows():
                nearby = bank2_atms.apply(
                    lambda atm2: haversine_distance(
                        atm1['latitude'], atm1['longitude'],
                        atm2['latitude'], atm2['longitude']
                    ) <= 0.5, axis=1
                ).sum()
                count += nearby
            co_location_matrix.loc[bank1, bank2] = count

    co_location_matrix = co_location_matrix.astype(int)

    fig = px.imshow(
        co_location_matrix,
        labels=dict(x="Bank", y="Bank", color="Co-locations"),
        x=banks,
        y=banks,
        color_continuous_scale='YlOrRd',
        title="Co-location Matrix (within 500m)"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Market penetration efficiency
    st.markdown("---")
    st.subheader("Market Penetration Efficiency")
    st.markdown("Average distance between ATMs (lower = denser network)")

    efficiency_data = []
    for bank in bank_atms['source'].unique():
        bank_data = bank_atms[bank_atms['source'] == bank]
        if len(bank_data) > 1:
            distances = []
            for i, atm1 in bank_data.iterrows():
                for j, atm2 in bank_data.iterrows():
                    if i < j:
                        dist = haversine_distance(
                            atm1['latitude'], atm1['longitude'],
                            atm2['latitude'], atm2['longitude']
                        )
                        distances.append(dist)
            avg_distance = np.mean(distances) if distances else 0
            efficiency_data.append({
                'Bank': bank,
                'ATM Count': len(bank_data),
                'Avg Spacing (km)': avg_distance,
                'Efficiency': len(bank_data) / avg_distance if avg_distance > 0 else 0
            })

    efficiency_df = pd.DataFrame(efficiency_data).sort_values('ATM Count', ascending=False)

    fig = px.scatter(
        efficiency_df,
        x='ATM Count',
        y='Avg Spacing (km)',
        size='Efficiency',
        color='Bank',
        hover_data=['Efficiency'],
        title='Network Efficiency: ATM Count vs Spacing',
        labels={'Avg Spacing (km)': 'Average Distance Between ATMs (km)'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

else:  # ROI Rankings page
    st.markdown('<div class="main-header">ROI-Ranked Expansion Locations</div>', unsafe_allow_html=True)
    st.markdown("Strategic ATM placement recommendations based on multi-factor analysis")
    st.markdown("---")

    # Calculate comprehensive ROI scores
    gaps_df = calculate_coverage_gaps(data, bob_atms, radius_km)

    if len(gaps_df) > 0:
        gaps_df['roi_score'] = gaps_df.apply(
            lambda row: calculate_roi_score(row, retail_locations), axis=1
        )
        gaps_df = gaps_df.sort_values('roi_score', ascending=False)

        # Scoring explanation
        with st.expander("ℹ️ How ROI Score is Calculated"):
            st.markdown("""
            **ROI Score Components:**
            - **Coverage Gap (30%)**: Distance to nearest BOB ATM (farther = higher score)
            - **Market Demand (40%)**: Number of competitor ATMs within 1km (more = higher score)
            - **Retail Proximity (30%)**: Distance to nearest retail location (closer = higher score)

            **Score Range**: 0-100 points
            - **90-100**: Excellent opportunity
            - **70-89**: Good opportunity
            - **50-69**: Fair opportunity
            - **Below 50**: Low priority
            """)

        # Top metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            top_score = gaps_df['roi_score'].max()
            st.metric("Top ROI Score", f"{top_score:.1f}")
        with col2:
            excellent_count = len(gaps_df[gaps_df['roi_score'] >= 90])
            st.metric("Excellent Opportunities", excellent_count)
        with col3:
            good_count = len(gaps_df[(gaps_df['roi_score'] >= 70) & (gaps_df['roi_score'] < 90)])
            st.metric("Good Opportunities", good_count)
        with col4:
            avg_score = gaps_df['roi_score'].mean()
            st.metric("Average ROI Score", f"{avg_score:.1f}")

        st.markdown("---")

        # Interactive selection
        st.subheader("Top Expansion Locations")

        num_locations = st.slider(
            "Number of locations to show",
            min_value=10,
            max_value=min(100, len(gaps_df)),
            value=30,
            step=10
        )

        top_locations = gaps_df.head(num_locations)

        # Map
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = go.Figure()

            # Add BOB ATMs
            fig.add_trace(go.Scattermapbox(
                lat=bob_atms['latitude'],
                lon=bob_atms['longitude'],
                mode='markers',
                marker=dict(size=10, color='blue'),
                name='Existing BOB ATMs',
                text=bob_atms['address'],
                hovertemplate='<b>BOB ATM</b><br>%{text}<extra></extra>'
            ))

            # Add top opportunities with color gradient
            fig.add_trace(go.Scattermapbox(
                lat=top_locations['latitude'],
                lon=top_locations['longitude'],
                mode='markers',
                marker=dict(
                    size=14,
                    color=top_locations['roi_score'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="ROI<br>Score"),
                    cmin=50,
                    cmax=100
                ),
                name='Expansion Opportunities',
                text=top_locations.apply(
                    lambda x: f"<b>ROI Score: {x['roi_score']:.1f}</b><br>{x['source']}<br>{x['address']}<br>Distance to BOB: {x['distance_to_bob']:.1f}km<br>Competitors: {x['competitor_density']}",
                    axis=1
                ),
                hovertemplate='%{text}<extra></extra>'
            ))

            center_lat = top_locations['latitude'].mean()
            center_lon = top_locations['longitude'].mean()

            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=10
                ),
                height=600,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Score Distribution**")

            # Create score categories
            top_locations['Category'] = pd.cut(
                top_locations['roi_score'],
                bins=[0, 50, 70, 90, 100],
                labels=['Low', 'Fair', 'Good', 'Excellent']
            )

            category_counts = top_locations['Category'].value_counts().sort_index(ascending=False)

            fig = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                color=category_counts.index,
                color_discrete_map={
                    'Excellent': '#2ca02c',
                    'Good': '#98df8a',
                    'Fair': '#ffbb78',
                    'Low': '#ff7f0e'
                },
                title='Opportunities by Category'
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.markdown("**Investment Estimate**")

            avg_cost_azn = 30000
            total_cost = num_locations * avg_cost_azn

            st.metric("Total Investment", f"₼{total_cost:,} AZN")
            st.caption(f"Based on ₼{avg_cost_azn:,} per ATM average")

            # Phase breakdown
            st.markdown("**Suggested Phasing:**")
            st.markdown(f"- Phase 1: {min(20, num_locations)} ATMs")
            st.markdown(f"- Phase 2: {max(0, min(30, num_locations-20))} ATMs")
            st.markdown(f"- Phase 3: {max(0, num_locations-50)} ATMs")

        # Detailed ranking table
        st.markdown("---")
        st.subheader(f"Top {num_locations} Locations (Ranked by ROI)")

        # Add ranking column
        display_df = top_locations.reset_index(drop=True)
        display_df.index = display_df.index + 1
        display_df.index.name = 'Rank'

        display_table = display_df[[
            'address', 'source', 'roi_score', 'distance_to_bob',
            'competitor_density', 'latitude', 'longitude'
        ]].copy()

        display_table.columns = [
            'Address', 'Competitor Bank', 'ROI Score',
            'Distance to BOB (km)', 'Competitors Nearby', 'Latitude', 'Longitude'
        ]

        display_table['ROI Score'] = display_table['ROI Score'].round(1)
        display_table['Distance to BOB (km)'] = display_table['Distance to BOB (km)'].round(2)

        # Color code by score
        def highlight_score(val):
            if val >= 90:
                return 'background-color: #d4edda'
            elif val >= 70:
                return 'background-color: #fff3cd'
            elif val >= 50:
                return 'background-color: #f8d7da'
            return ''

        styled_table = display_table.style.applymap(
            highlight_score,
            subset=['ROI Score']
        )

        st.dataframe(styled_table, use_container_width=True, height=600)

        # Download button
        csv = display_table.to_csv()
        st.download_button(
            label="📥 Download Full Rankings (CSV)",
            data=csv,
            file_name=f"bob_expansion_rankings_top_{num_locations}.csv",
            mime="text/csv"
        )

    else:
        st.info("No expansion opportunities found with current criteria. Try adjusting the coverage radius.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
    <p><b>Bank of Baku ATM Strategy Dashboard</b></p>
    <p>Data sources: 7 Banks • 3 Retail Chains • 4,377 Total Locations</p>
    <p>Analysis based on geographic clustering and competitive intelligence</p>
    </div>
    """,
    unsafe_allow_html=True
)
