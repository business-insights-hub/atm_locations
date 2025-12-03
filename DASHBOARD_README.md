# 🏦 Bank of Baku ATM Strategy Dashboard

Interactive fullstack web application for strategic ATM placement analysis and competitive intelligence.

![Dashboard](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
./start.sh
```

Access at: **http://localhost:8501**

### Local Development

```bash
./start-local.sh
```

### Stop Dashboard

```bash
./stop.sh
```

## 📊 Dashboard Features

### 1️⃣ Overview Page
**Real-time market intelligence**
- Key Performance Indicators (KPIs)
  - Total BOB ATMs vs Market
  - Market Share Percentage
  - Gap to Market Leader
- Interactive market share comparison
- Geographic distribution map
- Coverage gap summary

### 2️⃣ Interactive Map
**Dynamic location visualization**
- Toggle layers independently:
  - ✅ BOB ATMs (blue markers)
  - ✅ Competitor ATMs (colored by bank)
  - ✅ Retail Locations (green markers)
- Multi-bank filtering
- Hover for detailed information
- Real-time location statistics

### 3️⃣ Coverage Gaps Analysis
**Identify underserved markets**
- Visualize areas >2km from BOB ATMs
- Heatmap colored by distance
- Competitor density analysis
- Distribution histograms
- Top 20 priority gaps table
- Filter by coverage radius (0.5-5km)

**Metrics Displayed:**
- Total coverage gaps
- Average distance to nearest BOB ATM
- Maximum distance
- Average competitor density

### 4️⃣ Retail Opportunities
**Strategic partnership locations**
- High foot-traffic retail sites:
  - OBA Supermarkets (1,640 locations)
  - Bravo Supermarkets (138 locations)
  - Bazarstores (97 locations)
- Opportunity scoring algorithm
- Interactive map of top opportunities
- Breakdown by retail chain
- Detailed top 20 locations table

**Scoring Factors:**
- Distance from BOB ATMs (50%)
- Nearby competitor density (50%)

### 5️⃣ Competitor Analysis
**Competitive intelligence dashboard**

**Market Position:**
- Side-by-side market share comparison
- Pie chart of market distribution
- BOB position indicator

**Geographic Density:**
- Dual heatmaps comparing BOB vs any competitor
- Select competitor for comparison
- Identify saturation vs opportunity zones

**Co-location Matrix:**
- How many competitor ATMs are within 500m of each other
- Heatmap visualization
- Identifies high-competition areas

**Network Efficiency:**
- Average spacing between ATMs by bank
- Scatter plot: ATM count vs spacing
- Bubble size = efficiency score
- Identifies over/under-saturated networks

### 6️⃣ ROI Rankings
**Data-driven expansion recommendations**

**Multi-Factor ROI Scoring:**
- Coverage Gap (30%): Distance to nearest BOB ATM
- Market Demand (40%): Competitor density within 1km
- Retail Proximity (30%): Distance to retail locations

**Score Tiers:**
- 🟢 Excellent (90-100): Immediate priority
- 🟡 Good (70-89): Strong opportunity
- 🟠 Fair (50-69): Consider for Phase 2
- 🔴 Low (<50): Low priority

**Interactive Features:**
- Slider to select top N locations (10-100)
- Color-coded map by ROI score
- Score distribution by category
- Investment calculator (AZN)
- Phased rollout recommendations
- Downloadable CSV export

**Investment Estimates:**
- Standalone ATM: ~₼42,000 AZN
- Retail partnership: ~₼25,000 AZN
- Average: ~₼30,000 AZN per location

## 🎯 Use Cases

### Strategic Planning
1. **Market Entry**: Identify high-priority expansion zones
2. **Competitive Response**: See where competitors are clustering
3. **Partnership Strategy**: Find optimal retail partnerships
4. **Budget Allocation**: ROI-ranked investment priorities

### Tactical Decisions
1. **Site Selection**: Compare multiple potential locations
2. **Coverage Analysis**: Ensure adequate service area coverage
3. **Competitive Positioning**: Avoid over-saturation
4. **Performance Tracking**: Monitor market share changes

### Executive Reporting
1. **KPI Dashboard**: Real-time metrics for board meetings
2. **Visual Storytelling**: Interactive maps for presentations
3. **Data Export**: Download rankings for detailed analysis
4. **Scenario Planning**: Adjust parameters to test strategies

## 📈 Data Sources

| Source | Type | Count | Purpose |
|--------|------|-------|---------|
| Kapital Bank | ATM | 1,130 | Competitor analysis |
| ABB Bank | ATM | 971 | Competitor analysis |
| Xalq Bank | ATM | 133 | Competitor analysis |
| Bank Respublika | ATM | 109 | Competitor analysis |
| Rabita Bank | ATM | 74 | Competitor analysis |
| Yelo Bank | ATM | 48 | Competitor analysis |
| **Bank of Baku** | **ATM** | **35** | **Strategic planning** |
| OBA Supermarket | Branch | 1,640 | Retail partnerships |
| Bravo Supermarket | Store | 138 | Retail partnerships |
| Bazarstore | Store | 97 | Retail partnerships |
| **Total** | | **4,377** | |

## 🔧 Configuration

### Coverage Radius
Adjust in sidebar: 0.5km - 5.0km (default: 2km)
- Standard ATM service area = 2km
- Urban areas may use 1km
- Rural areas may use 3-5km

### Bank Filters
Select/deselect banks in sidebar to:
- Focus on specific competitors
- Reduce map clutter
- Compare market positions

### Investment Parameters
Default costs (customizable in code):
- Standalone ATM: ₼42,000 AZN
- Retail partnership: ₼25,000 AZN
- Weighted average: ₼30,000 AZN

## 🌐 Deployment Options

### 1. Docker (Recommended)
```bash
./start.sh
# or
docker-compose up -d
```

### 2. Streamlit Cloud (Free)
1. Push to GitHub
2. Connect at [streamlit.io/cloud](https://streamlit.io/cloud)
3. Deploy `app.py`

### 3. Heroku
```bash
heroku create bob-atm-dashboard
git push heroku main
```

### 4. AWS EC2 / DigitalOcean
```bash
# SSH into server
git clone <repo>
cd atm_locations
./start.sh
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Technical Architecture

```
┌─────────────────────────────────────────┐
│         User Browser (Port 8501)        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Streamlit Web Server             │
│  ┌──────────────────────────────────┐   │
│  │  app.py (Multi-page Dashboard)   │   │
│  └──────────────┬───────────────────┘   │
│                 │                        │
│  ┌──────────────▼───────────────────┐   │
│  │  Plotly (Interactive Charts)     │   │
│  │  Folium (Maps)                   │   │
│  │  Pandas (Data Processing)        │   │
│  └──────────────┬───────────────────┘   │
└─────────────────┼───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Data Layer (CSV Files)          │
│  • combined_locations.csv (4,377 rows)  │
│  • Individual bank CSVs                 │
│  • Retail location CSVs                 │
└─────────────────────────────────────────┘
```

## 🔒 Security Notes

- Dashboard uses HTTP by default (local deployment)
- For production: Use reverse proxy (nginx) with HTTPS
- Data files mounted as read-only in Docker
- No database credentials required
- Consider VPN/IP whitelisting for sensitive deployments

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8501
lsof -i :8501
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8080:8501"
```

### Data Not Loading
```bash
# Verify data file exists
ls -lh data/combined_locations.csv

# Check file has content
wc -l data/combined_locations.csv
# Should show: 4377

# Restart dashboard
./stop.sh && ./start.sh
```

### Docker Issues
```bash
# Check Docker is running
docker info

# View logs
docker-compose logs -f

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Performance Issues
```bash
# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory (4GB+)

# Or limit data in sidebar filters
# Deselect some banks to reduce render load
```

## 📚 Documentation

- **DEPLOYMENT.md** - Comprehensive deployment guide
- **README.md** - Strategic analysis presentation
- **charts/INSIGHTS_REPORT.txt** - Key findings summary

## 🎨 Customization

### Modify Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"  # Change to your brand color
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

### Update Data
```bash
cd scripts
python scrape_kapital.py
python scrape_abb.py
# ... other scrapers
python combine_datasets.py
```

### Add New Page
1. Add new page section in `app.py`
2. Add to sidebar navigation
3. Implement page logic in main content area

## 🚦 Status

| Component | Status | Version |
|-----------|--------|---------|
| Dashboard | ✅ Production | 1.0.0 |
| Docker | ✅ Ready | - |
| Data | ✅ Complete | 2025-12-03 |
| Documentation | ✅ Complete | - |

## 📞 Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Verify data: `ls data/`
3. Review [DEPLOYMENT.md](DEPLOYMENT.md)
4. Check Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

## 📄 License

Internal use only - Bank of Baku Strategic Analysis

---

**Built with ❤️ using Streamlit, Plotly, and Python**

**Dashboard URL**: http://localhost:8501

**Last Updated**: 2025-12-03
