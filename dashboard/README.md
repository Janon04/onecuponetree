# Dashboard Backend API

The dashboard has been converted to a backend-only service that provides data processing without frontend rendering.

## Endpoints

### Main Dashboard Endpoint
- **URL**: `/dashboard/`
- **Method**: GET
- **Authentication**: Required (staff users only)

#### Default Behavior
- Redirects to home page (no frontend interface)

#### API Access
- **URL**: `/dashboard/?format=json`
- **Returns**: JSON response with dashboard data

### Public Dashboard
- **URL**: `/dashboard/public/`
- **Shows**: Information page about the dashboard changes

## API Response Format

When accessing `/dashboard/?format=json`, you'll receive:

```json
{
    "stats": {
        "trees_planted": 1250,
        "youth_trained": 45,
        "coffee_cups_sold": 3200,
        "farmers_supported": 78,
        "total_donations": 125000.50,
        "total_success_stories": 12
    },
    "charts": {
        "month_labels": ["Jan", "Feb", "Mar", ...],
        "trees_month_data": [10, 25, 30, ...],
        "donations_month_data": [5000, 7500, 12000, ...],
        "district_labels": ["Kigali", "Musanze", ...],
        "district_data": [150, 120, 90, ...]
    },
    "map_trees": [
        {
            "tree_id": "TREE001",
            "species": "Coffee Arabica",
            "planted_date": "2025-01-15",
            "latitude": -1.9441,
            "longitude": 30.0619
        }
    ],
    "selected_year": 2025,
    "all_years": [2025, 2024, 2023]
}
```

## Query Parameters

- `year`: Filter data by specific year (e.g., `?year=2024`)
- `format`: Set to `json` for API response (e.g., `?format=json`)

## Features

- **Data Processing**: Calculates impact statistics from database
- **Year Filtering**: Filter charts by specific year
- **District Analysis**: Top 10 districts by tree count
- **API Format**: Clean JSON response for external integrations
- **Authentication**: Staff-only access for sensitive data

## Usage Examples

```bash
# Get current year data as JSON
curl -H "Authorization: ..." http://localhost:8000/dashboard/?format=json

# Get specific year data
curl -H "Authorization: ..." http://localhost:8000/dashboard/?year=2024&format=json
```

## Migration Notes

- Frontend template moved to `impact.html.bak`
- Navigation links updated to point to public dashboard
- All chart and visualization logic preserved in backend
- Data processing functions remain fully functional