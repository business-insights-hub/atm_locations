# Bank of Baku ATM Strategy Dashboard 🏦

**Interactive data analytics dashboard for strategic ATM network expansion planning**

Combining competitive intelligence, geographic analysis, and retail partnership opportunities across Azerbaijan's banking landscape.

---

## 🎯 Project Overview

This dashboard helps Bank of Baku make data-driven decisions for ATM network expansion by analyzing **4,377 locations** including 2,500+ bank ATMs from 7 competing banks and 1,875 retail locations from 3 major supermarket chains.

### Key Capabilities

- ✅ **Coverage gap analysis** - Identify competitor-dense areas with no BOB presence
- ✅ **Retail partnership opportunities** - Find high-traffic supermarket locations for ATM placement
- ✅ **ROI-ranked expansion locations** - Multi-factor scoring algorithm for strategic placement
- ✅ **Competitive intelligence** - Market share, co-location, and efficiency analysis
- ✅ **Interactive mapping** - Readable coordinates, toggleable layers, real-time filtering
- ✅ **Chain performance analysis** - Compare OBA, Bravo, and Bazarstore opportunities

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| **BOB ATMs** | 35 locations |
| **Total Market ATMs** | 2,500+ |
| **BOB Market Share** | 1.4% |
| **Market Leader** | Kapital Bank (1,130 ATMs) |
| **Coverage Gaps** | 1,549 opportunities |
| **Retail Partnership Sites** | 1,875 locations |

---

## ✨ Dashboard Features

### 📊 **Overview Page**
- Market share analysis with BOB highlighted in blue
- Geographic distribution map
- Coverage gap preview metrics
- Gap-to-leader tracking

### 🗺️ **Interactive Map**
- **Filterable visualization** - Toggle BOB ATMs, competitors, retail locations
- **Readable coordinates** - 5-decimal precision on hover
- **Visual differentiation**:
  - 🔵 Blue circles - BOB ATMs (16px)
  - 🔴 Red circles - Competitor ATMs (12px)
  - 🟢 Green squares - Potential ATM sites (14px)
- **Smart sampling** - Performance-optimized for large datasets
- **Zoom level 11** - Detailed street-level view

### 🎯 **Coverage Gaps Analysis**
- Identifies competitor locations >2km from BOB ATMs
- Heat maps showing gap severity
- Distance and competitor density histograms
- Top gaps ranked by strategic value
- Interactive map with coordinates

### 🏪 **Retail Opportunities**
**NEW: Comprehensive chain analysis including:**
- **Performance comparison** - Average scores by chain
- **Quality distribution** - Excellent/Good/Fair locations per chain
- **Best location cards** - Top site from each chain with metrics
- **Top 10 analysis** - Cross-chain comparison scatter plot
- **Chain distribution** - Pie chart showing which chains dominate
- **Detailed metrics table** - All statistics in one view

**Key Charts:**
- Average Opportunity Score by Chain (bar chart)
- Location Quality Distribution (stacked bar)
- Top 10 Locations: Distance vs Competition (scatter)
- Chain Distribution in Top 10 (donut chart)

### 📈 **Competitor Analysis**
- Market position comparison
- Geographic density heatmaps
- Co-location matrix (within 500m)
- Network efficiency scatter plot
- Side-by-side density comparison

### 💰 **ROI Rankings**
- **Multi-factor scoring**:
  - Coverage Gap (30%) - Distance to nearest BOB ATM
  - Market Demand (40%) - Competitor density
  - Retail Proximity (30%) - Distance to retail sites
- Score categories: Excellent (90-100), Good (70-89), Fair (50-69)
- Investment estimates (₼30,000 per ATM average)
- Phased deployment recommendations
- **Downloadable CSV** rankings

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Make scripts executable
chmod +x start.sh stop.sh

# Start the dashboard
./start.sh

# Access at http://localhost:8501
```

**Stop the dashboard:**
```bash
./stop.sh
```

### Option 2: Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py

# Access at http://localhost:8501
```

---

## 📁 Project Structure

```
atm_locations/
├── app.py                      # Main dashboard (1,500+ lines)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Docker orchestration
├── .dockerignore              # Build exclusions
│
├── data/                       # Location datasets
│   ├── combined_locations.csv # All 4,377 locations
│   ├── bob_atm_locations.csv # BOB ATMs (35)
│   ├── kapital_locations.csv # Kapital Bank ATMs
│   ├── abb_locations.csv     # ABB Bank ATMs
│   ├── oba_locations.csv     # OBA Supermarkets (1,640)
│   ├── bravo_locations.csv   # Bravo Supermarkets (138)
│   └── bazarstore_locations.csv # Bazarstore (97)
│
├── charts/                     # Static exports (optional)
│   └── README.md              # Chart documentation
│
├── scripts/                    # Data processing
│   ├── scrape_bob.py
│   ├── scrape_competitors.py
│   ├── scrape_retail.py
│   └── combine_datasets.py
│
├── .streamlit/                 # Configuration
│   ├── config.toml            # Theme & settings
│   └── credentials.toml       # Auth (if needed)
│
├── start.sh                    # Docker quick start
├── stop.sh                     # Docker stop
├── start-local.sh             # Local dev start
├── DEPLOYMENT.md              # Deployment guide
└── README.md                  # This file
```

---

## 🛠️ Technology Stack

### Core
- **Streamlit 1.29.0** - Interactive web framework
- **Python 3.11+** - Programming language

### Data & Analysis
- **Pandas 2.1.4** - Data manipulation
- **NumPy 1.26.2** - Vectorized operations (10-100x faster)

### Visualization
- **Plotly 5.18.0** - Interactive charts & maps
- **Plotly Express** - High-level plotting

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Orchestration

### Geospatial
- **Haversine Formula** - Distance calculations
- **OpenStreetMap** - Map tiles

---

## 📈 Key Algorithms

### 1. Coverage Gap Detection

```python
for each competitor_atm:
    distance = haversine(competitor_atm, nearest_bob_atm)
    if distance > threshold:  # Default: 2km
        competitor_density = count_nearby_competitors(1km)
        mark_as_gap(distance, competitor_density)
```

### 2. ROI Scoring Formula

```
ROI Score = Coverage_Gap×0.30 + Market_Demand×0.40 + Retail_Proximity×0.30

Where:
- Coverage_Gap = min(distance_to_bob / 10, 1.0) × 30
- Market_Demand = min(competitor_density / 10, 1.0) × 40
- Retail_Proximity = max(0, (2.0 - retail_dist) / 2.0) × 30

Range: 0-100 points
```

### 3. Retail Chain Scoring

```python
Opportunity Score = (distance_to_bob / 10) × 50 + (competitor_count / 10) × 50

Quality Categories:
- Excellent: Score > 40
- Good: 30 ≤ Score ≤ 40
- Fair: Score < 30
```

### 4. Performance Optimization

- **Vectorized NumPy operations** - 10-100x faster than pandas loops
- **@st.cache_data decorators** - Cache expensive calculations
- **Smart sampling** - Max 500 points per map layer
- **Haversine vectorization** - Calculate 1M+ distances in <1 second

---

## 🎨 Visual Design

### Color Coding
- 🔵 **Blue (#1f77b4)** - Bank of Baku (primary brand color)
- 🔴 **Red (#ff6b6b)** - Competitors / Gaps
- 🟢 **Green (#51cf66)** - Retail / Opportunities
- 🟡 **Orange/Yellow** - Fair/Medium priority
- 🔴 **Dark Red** - Urgent/High priority

### Symbol Differentiation
- ⭕ **Circles** - ATM locations (existing infrastructure)
- ⬜ **Squares** - Retail/Potential sites (opportunities)

### Marker Sizes
- **16px** - BOB ATMs (most visible)
- **14-16px** - Opportunities/Potential sites
- **12px** - Competitor ATMs

### Data Precision
- **Coordinates**: 5 decimal places (~1 meter accuracy)
- **Distances**: 2 decimal places in km
- **Scores**: 1 decimal place

---

## 📊 Dashboard Pages Explained

### Page 1: Overview
**Purpose**: Executive summary of market position
**Key Metrics**: Market share, gap to leader, total opportunities
**Visualizations**: Bar charts, geographic overview map

### Page 2: Interactive Map
**Purpose**: Explore all locations with precise coordinates
**Controls**: Toggle BOB/Competitors/Retail, bank filters
**Features**: Hover for full details, zoom/pan, coordinate display

### Page 3: Coverage Gaps
**Purpose**: Find competitor locations BOB doesn't serve
**Analysis**: Distance-based gap detection, density heatmaps
**Output**: Ranked list of 1,549 opportunities

### Page 4: Retail Opportunities ⭐ **NEW FEATURES**
**Purpose**: Identify best supermarket chains for partnerships
**Analysis**:
- Chain performance comparison (OBA vs Bravo vs Bazarstore)
- Quality distribution (Excellent/Good/Fair per chain)
- Best single location from each chain
- Top 10 cross-chain comparison
**Output**: Strategic partnership recommendations

### Page 5: Competitor Analysis
**Purpose**: Understand competitive landscape
**Analysis**: Market share, co-location, efficiency
**Tools**: Density heatmaps, co-location matrix

### Page 6: ROI Rankings
**Purpose**: Prioritize deployment with data-driven scores
**Algorithm**: Multi-factor weighted scoring
**Output**: Ranked expansion list with investment estimates

---

## 🔧 Configuration

### Streamlit Theme
Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"      # BOB brand blue
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
enableCORS = false
maxUploadSize = 200
```

### Docker Port
Edit `docker-compose.yml`:

```yaml
ports:
  - "8501:8501"  # Change to "8080:8501" for port 8080
```

### Coverage Radius
Adjust in sidebar: 0.5 - 5.0 km (default: 2.0 km)

---

## 📊 Use Cases

### 1. Strategic Planning
- **Scenario**: Plan next 50 ATM deployments
- **How**: Use ROI Rankings page, filter by score >70
- **Output**: Prioritized list with investment estimates

### 2. Partnership Negotiations
- **Scenario**: Which retail chain to approach first?
- **How**: Use Retail Opportunities chain comparison
- **Output**: Best chain identified with top locations

### 3. Competitive Intelligence
- **Scenario**: How does BOB compare to Kapital Bank?
- **How**: Use Competitor Analysis density comparison
- **Output**: Side-by-side heatmaps showing gaps

### 4. Regional Expansion
- **Scenario**: Enter new city/region
- **How**: Use Interactive Map, filter by area
- **Output**: Competitor density, retail sites, gaps

### 5. Budget Planning
- **Scenario**: Estimate Phase 1 costs (20 ATMs)
- **How**: ROI Rankings investment calculator
- **Output**: ₼600,000 AZN (20 × ₼30,000)

---

## 🐛 Troubleshooting

### Dashboard Won't Start

```bash
# Check Docker status
docker info

# Check port availability
lsof -i :8501

# View logs
docker-compose logs -f
```

### Data Not Loading

```bash
# Verify file exists
ls -la data/combined_locations.csv

# Check file format
head data/combined_locations.csv

# Rebuild cache
# Press 'C' in dashboard to clear cache
```

### Performance Issues

**Symptoms**: Slow loading, charts hanging
**Solutions**:
1. Reduce coverage radius (fewer gaps to calculate)
2. Use fewer bank filters
3. Clear cache (Press 'C')
4. Restart dashboard

### Map Not Showing

**Check**:
- Data has valid lat/lon coordinates
- Browser allows geolocation
- Internet connection (for OpenStreetMap tiles)

---

## 🔄 Data Updates

### Updating Location Data

```bash
# 1. Run scrapers to get latest data
cd scripts
python scrape_competitors.py
python scrape_retail.py

# 2. Combine datasets
python combine_datasets.py

# 3. Restart dashboard
cd ..
docker-compose restart
```

### Adding New Banks

1. Create scraper: `scripts/scrape_newbank.py`
2. Save to: `data/newbank_locations.csv`
3. Update: `scripts/combine_datasets.py`
4. Regenerate: `data/combined_locations.csv`

### Adding New Retail Chains

1. Follow same process as banks
2. Ensure `type` column = "Branch" or "Store"
3. Update `get_display_name()` function in `app.py`

---

## 📄 License

**Proprietary - Bank of Baku Internal Use Only**

This dashboard and associated data are confidential and intended exclusively for Bank of Baku strategic planning purposes.

---

## 👥 Support

### Internal Contacts
- **Strategy Team**: strategy@bankofbaku.az
- **Technical Support**: analytics@bankofbaku.az
- **Data Updates**: dataops@bankofbaku.az

### Documentation
- **Deployment Guide**: `DEPLOYMENT.md`
- **Dashboard Guide**: `DASHBOARD_README.md`
- **Chart Documentation**: `charts/README.md`

---

## 🎯 Roadmap

### Current Version (v1.0)
✅ Interactive mapping with coordinates
✅ Retail chain performance analysis
✅ ROI-based ranking system
✅ Docker deployment
✅ 6-page comprehensive dashboard

### Planned Features (v2.0)
- [ ] Real-time data API integration
- [ ] Mobile-responsive design
- [ ] Historical trend analysis
- [ ] Predictive foot traffic modeling
- [ ] Transaction data integration
- [ ] Automated email reports
- [ ] User authentication
- [ ] Multi-language support (AZ/EN/RU)

---

## 📚 Additional Resources

### Related Files
- **Static Analysis**: See original README for 12-chart static analysis
- **Chart Exports**: `charts/` folder for presentation graphics
- **Raw Data**: `data/` folder with all source CSVs

### External Links
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python/)
- [Docker Documentation](https://docs.docker.com)

---

## 🏆 Key Achievements

- ✅ **4,377 locations analyzed** across 7 banks + 3 retail chains
- ✅ **1,549 coverage gaps identified** for strategic expansion
- ✅ **1,875 retail partnership sites** evaluated
- ✅ **Multi-factor ROI algorithm** for data-driven prioritization
- ✅ **Interactive visualization** with readable coordinates
- ✅ **Performance optimized** using NumPy vectorization
- ✅ **Docker containerized** for easy deployment

---

**Dashboard Version**: 1.0
**Last Updated**: December 2025
**Data Coverage**: 4,377 locations across Azerbaijan
**Banks Analyzed**: 7 major banks
**Retail Chains**: 3 supermarket chains

---

*Built with ❤️ for Bank of Baku's Strategic Growth*
