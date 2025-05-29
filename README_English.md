# US Health States Visualization Dashboard (Python Shiny)

This is an interactive data visualization application built with Python Shiny for analyzing health indicators across US states.

## Features

- **Interactive Data Visualization**: Bar charts, trend charts, and data tables
- **Multi-State Selection**: Compare single or multiple states
- **Time Series Analysis**: View health indicator trends over time
- **Health Indicators**: 
  - Obesity Rate (Adult Obesity Rate)
  - Smoking Rate (Adult Smoking Rate)
  - Physically Unhealthy Days
  - Mentally Unhealthy Days
- **Search Functionality**: Quick search and filter state names
- **Data Export**: View and filter data tables
- **Responsive Design**: Works on different screen sizes

## Requirements

### Python Version
- Python 3.8 or higher

### Dependencies
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Clone or Download Project**
   ```bash
   # Ensure you have these files:
   # - app.py (main application file)
   # - us_health_states.csv (data file)
   # - requirements.txt (dependencies file)
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   python app.py
   ```

4. **Access Application**
   - Open the displayed URL in your browser (usually http://127.0.0.1:8000)

## Usage Guide

### Control Panel
- **Search States**: Enter state name in search box for quick filtering
- **Select States**: Choose one or multiple states for comparison
- **Select All States**: One-click to select or clear all states
- **Select Year**: View data for specific year
- **Select Health Indicator**: Switch between different health metrics

### Visualization Tabs
1. **Bar Chart**: Horizontal bar chart showing indicator comparison for selected states in specific year
2. **Trend Chart**: Line chart showing indicator trends over time for selected states
3. **Data Table**: Tabular view of detailed data with column selection and sorting

### Data Table Features
- Select which columns to display (State, Year, Value, Region, Rank)
- Data sorted by value in descending order
- Support for multi-column data comparison

## Project Structure

```
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── us_health_states.csv   # Health data
└── README_English.md      # Usage instructions
```

## Data Description

The data contains health indicators for US states from 2014 to 2020:
- **Obesity Rate**: Adult obesity percentage (%)
- **Smoking Rate**: Adult smoking percentage (%)
- **Physically Unhealthy Days**: Average physically unhealthy days
- **Mentally Unhealthy Days**: Average mentally unhealthy days

Data source: Centers for Disease Control and Prevention (CDC)

## Technology Stack

- **Frontend Framework**: Shiny for Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **UI Components**: HTML/CSS, Bootstrap

## Development Notes

### Main Components

1. **Data Loading and Preprocessing** (`load_data()`)
   - CSV file reading
   - Data type conversion
   - Missing value handling

2. **UI Components** (`app_ui`)
   - Responsive layout
   - Sidebar control panel
   - Main content area
   - Custom CSS styling

3. **Server Logic** (`server()`)
   - Reactive data processing
   - Chart generation
   - User interaction handling

### Custom Features

- **Region Mapping**: Assign states to four major US geographic regions
- **Search Filtering**: Real-time state name search functionality
- **Data Validation**: Input validation and error handling
- **Reactive Updates**: Dynamic chart and data updates based on user selections

## Troubleshooting

### Common Issues

1. **Dependency Installation Failed**
   ```bash
   # Upgrade pip
   pip install --upgrade pip
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Data File Not Found**
   - Ensure `us_health_states.csv` file is in the application root directory
   - Check file path and name are correct

3. **Port Already in Use**
   ```bash
   # Modify port in app.py
   app.run(port=8080)  # Use different port
   ```

## Performance Optimization

- Use reactive calculations to cache data processing results
- Lazy loading for large datasets
- Optimize chart rendering performance

## Contributing

Feel free to submit Issues and Pull Requests to improve this project.

## License

This project is licensed under the MIT License.

## Comparison with R Shiny Version

This Python version offers:
- **Faster Performance**: Better startup time and data processing
- **Modern Interactivity**: Enhanced user experience with Plotly charts
- **Easier Deployment**: Simpler deployment options
- **Python Ecosystem**: Easy integration with ML libraries

The functionality is equivalent to the R Shiny version (`app.R`) but implemented using Python's data science stack for improved performance and modern user experience. 