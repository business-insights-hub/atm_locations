# Charts Directory

This folder is designated for static chart exports from the interactive dashboard.

## Purpose

While the main dashboard (`app.py`) provides interactive visualizations, this folder can store:

1. **Static image exports** - PNG/SVG charts for presentations
2. **Report graphics** - Charts for PDF reports and documents
3. **Snapshot comparisons** - Historical analysis charts
4. **Executive summaries** - Key visuals for stakeholder meetings

## Exporting Charts from Dashboard

### Method 1: Screenshot from Browser
1. Open dashboard at `http://localhost:8501`
2. Navigate to desired chart
3. Use Plotly's built-in camera icon (top-right of chart)
4. Save as PNG to this folder

### Method 2: Python Script Export

```python
import plotly.graph_objects as go
import plotly.express as px

# Create chart
fig = px.bar(data, x='bank', y='count', title='Market Share')

# Export
fig.write_image('charts/market_share.png', width=1200, height=600)
fig.write_html('charts/market_share.html')
```

### Method 3: Programmatic Export

Add export functionality to `app.py`:

```python
# At end of chart creation
if st.button("Export Chart"):
    fig.write_image("charts/exported_chart.png")
    st.success("Chart exported to charts/ folder!")
```

## Recommended Chart Exports

### For Executive Presentations

1. **market_overview.png** - Market share comparison (Page 1: Overview)
2. **geographic_map.png** - ATM distribution map (Page 2: Interactive Map)
3. **coverage_gaps.png** - Gap analysis visualization (Page 3: Coverage Gaps)
4. **chain_comparison.png** - Retail chain performance (Page 4: Retail Opportunities)
5. **roi_rankings.png** - Top 30 expansion locations (Page 6: ROI Rankings)

### For Detailed Analysis

6. **competitor_density.png** - Density heatmap (Page 5: Competitor Analysis)
7. **co_location_matrix.png** - Bank co-location heatmap
8. **efficiency_scatter.png** - Network efficiency comparison
9. **quality_distribution.png** - Chain quality breakdown (Page 4)
10. **top10_scatter.png** - Distance vs competition analysis (Page 4)

## File Naming Convention

Use descriptive names with underscores:

- `{page}_{chart_type}_{date}.png`
- Example: `retail_chain_comparison_2025-12-04.png`
- Example: `roi_top30_locations_2025-12-04.png`

## Chart Specifications

### For Presentations (PowerPoint/Google Slides)
- **Format**: PNG with transparent background
- **Size**: 1920×1080 px (16:9 ratio)
- **DPI**: 300 for print quality

### For Reports (PDF Documents)
- **Format**: PNG or SVG
- **Size**: 1200×800 px
- **DPI**: 300

### For Web/Email
- **Format**: PNG
- **Size**: 800×600 px
- **DPI**: 72-96

## Color Scheme Reference

Maintain consistency with dashboard:

```
BOB_BLUE = '#1f77b4'
COMPETITOR_RED = '#ff6b6b'
RETAIL_GREEN = '#51cf66'
EXCELLENT_GREEN = '#2ca02c'
GOOD_LIGHT_GREEN = '#98df8a'
FAIR_ORANGE = '#ffbb78'
WARNING_RED = '#ff7f0e'
```

## Interactive HTML Exports

For interactive sharing:

```python
fig.write_html('charts/interactive_map.html')
```

Recipients can open HTML files in browser for full interactivity (zoom, pan, hover).

## Version Control

When exporting for comparison:

```
charts/
├── 2025-12/
│   ├── market_share_2025-12-04.png
│   ├── roi_rankings_2025-12-04.png
│   └── chain_comparison_2025-12-04.png
├── 2025-11/
│   └── ...
└── latest/
    ├── market_share.png (symlink to latest)
    └── roi_rankings.png (symlink to latest)
```

## Usage in Reports

### Markdown Reports

```markdown
![Market Share Analysis](charts/market_share.png)

*Figure 1: BOB holds 1.4% market share with significant growth opportunity*
```

### LaTeX Documents

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{charts/market_share.png}
    \caption{ATM Market Share Distribution}
    \label{fig:market_share}
\end{figure}
```

### PowerPoint

1. Insert > Pictures
2. Navigate to `charts/` folder
3. Select desired PNG
4. Resize and position

## Automated Export Script

Create `scripts/export_charts.py`:

```python
"""
Export all key dashboard charts to charts/ folder
Run after data updates to refresh visuals
"""

import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data
data = pd.read_csv('data/combined_locations.csv')

# Export market share
fig = px.bar(...)
fig.write_image(f'charts/market_share_{datetime.now():%Y-%m-%d}.png')

# Export other key charts
# ... add more exports
```

Run: `python scripts/export_charts.py`

## .gitignore Recommendations

If using version control:

```gitignore
# Ignore temporary exports
charts/temp_*
charts/*.tmp

# Keep directory structure
!charts/README.md
!charts/.gitkeep

# Ignore large files (optional)
charts/*.psd
charts/*.ai
```

## Notes

- This folder is **optional** - The dashboard itself provides all visualizations
- Use for **offline presentations** when dashboard access isn't available
- **Refresh exports** after data updates to maintain accuracy
- Consider **date-stamping** files to track analysis evolution
- Store **high-resolution versions** for print materials

## Current Status

📂 **charts/** - Ready for exports
- No default charts included
- Create exports as needed from dashboard
- Recommended: Export top 5 charts monthly for stakeholder reports

---

For questions about chart exports or custom visualization requests, contact: analytics@bankofbaku.az
