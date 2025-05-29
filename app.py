import pandas as pd
import numpy as np
from shiny import App, ui, render, reactive, req
from shiny.types import FileInfo
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from shinywidgets import output_widget, render_widget
import shinyswatch

# Load data
def load_data():
    """Load and preprocess health data"""
    health_data = pd.read_csv("us_health_states.csv", sep=";")
    
    # Rename columns
    health_data = health_data.rename(columns={
        "Adult obesity [in %]": "Adult.obesity..in...",
        "Adult smoking [in %]": "Adult.smoking..in...",
        "Physically Unhealthy Days": "Physical.unhealthy.days",
        "Mentally Unhealthy Days": "Mental.unhealthy.days"
    })
    
    # Data cleaning and transformation
    def clean_numeric_column(col):
        """Clean numeric columns"""
        # Convert to string
        col_str = col.astype(str)
        # Replace comma with decimal point
        col_str = col_str.str.replace(",", ".")
        # Remove non-numeric characters (keep decimal point)
        col_str = col_str.str.replace(r"[^0-9.]", "", regex=True)
        # Convert to numeric, errors become NaN
        return pd.to_numeric(col_str, errors='coerce')
    
    # Clean numeric columns
    health_data["Adult.obesity..in..."] = clean_numeric_column(health_data["Adult.obesity..in..."])
    health_data["Adult.smoking..in..."] = clean_numeric_column(health_data["Adult.smoking..in..."])
    health_data["Physical.unhealthy.days"] = clean_numeric_column(health_data["Physical.unhealthy.days"])
    health_data["Mental.unhealthy.days"] = clean_numeric_column(health_data["Mental.unhealthy.days"])
    
    return health_data

# Load data
health_data = load_data()

# Define region mapping
def get_region(state):
    """Return region based on state name"""
    northeast = ["Connecticut", "Maine", "Massachusetts", "New Hampshire",
                "Rhode Island", "Vermont", "New York", "New Jersey", "Pennsylvania"]
    midwest = ["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin",
              "Iowa", "Kansas", "Minnesota", "Missouri", "Nebraska",
              "North Dakota", "South Dakota"]
    south = ["Delaware", "Florida", "Georgia", "Maryland", "North Carolina",
            "South Carolina", "Virginia", "West Virginia", "Alabama",
            "Kentucky", "Mississippi", "Tennessee", "Arkansas",
            "Louisiana", "Oklahoma", "Texas"]
    
    if state in northeast:
        return "Northeast"
    elif state in midwest:
        return "Midwest"
    elif state in south:
        return "South"
    else:
        return "West"

# UI definition
app_ui = ui.page_fluid(
    # Add custom JavaScript for zoom functionality
    ui.head_content(
        ui.tags.script("""
        $(document).ready(function() {
            // Initialize zoom
            let currentZoom = 100;
            
            // Function to apply zoom
            function applyZoom(zoomLevel) {
                const zoomValue = zoomLevel / 100;
                document.body.style.transform = `scale(${zoomValue})`;
                document.body.style.transformOrigin = 'top left';
                document.body.style.width = `${100 / zoomValue}%`;
                document.body.style.height = `${100 / zoomValue}%`;
            }
            
            // Listen for zoom slider changes
            $(document).on('input', '#zoom_slider', function() {
                const zoomLevel = parseInt($(this).val());
                applyZoom(zoomLevel);
                
                // Update zoom display
                $('#zoom_display').text(zoomLevel + '%');
            });
        });
        """)
    ),
    
    # Control bar with theme picker, dark mode, and zoom
    ui.div(
        {"class": "d-flex justify-content-between align-items-center p-2 border-bottom"},
        ui.div(
            {"class": "d-flex align-items-center gap-3"},
            shinyswatch.theme_picker_ui(),
            ui.input_dark_mode()
        ),
        ui.div(
            {"class": "d-flex align-items-center gap-2"},
            ui.tags.label("Zoom:", {"class": "mb-0 fw-bold"}),
            ui.input_slider(
                "zoom_slider",
                label=None,
                min=50,
                max=150,
                value=100,
                step=10,
                post="%",
                width="150px"
            ),
            ui.tags.span("100%", id="zoom_display", class_="badge bg-secondary")
        )
    ),

    # Application header
    ui.div(
        {"class": "mb-4 mt-3"},
        ui.h1("US Health States Visualization Dashboard", 
              {"class": "text-center text-primary mb-2"}),
        ui.p("Interactive Health Indicators Analysis", 
             {"class": "text-center text-muted"})
    ),
    
    # Main layout
    ui.layout_sidebar(
        # Sidebar
        ui.sidebar(
            ui.h4("Control Panel", {"class": "text-primary"}),
            
            # State search
            ui.input_text("state_search", "Search States:", 
                         placeholder="Enter state name to search..."),
            
            # Select all states button
            ui.input_action_button("select_all_states", "Select All States", 
                                 class_="btn btn-outline-primary btn-sm w-100 my-2"),
            
            # State selection
            ui.input_selectize(
                "state", 
                "Select States:",
                choices={state: state for state in sorted(health_data['State'].unique())},
                selected=["Alabama"],
                multiple=True
            ),
            
            ui.hr(),
            
            # Year selection
            ui.input_selectize(
                "year",
                "Select Year:",
                choices={str(year): str(year) for year in sorted(health_data['year'].unique())},
                selected=str(health_data['year'].max())
            ),
            
            ui.hr(),
            
            # Health indicator selection
            ui.input_selectize(
                "primary_var",
                "Select Health Indicator:",
                choices={
                    "Adult.obesity..in...": "Obesity Rate",
                    "Adult.smoking..in...": "Smoking Rate",
                    "Physical.unhealthy.days": "Physically Unhealthy Days",
                    "Mental.unhealthy.days": "Mentally Unhealthy Days"
                },
                selected="Adult.obesity..in..."
            )
        ),
        
        # Main content area
        ui.div(
            # Status cards using Bootstrap cards
            ui.div(
                {"class": "row mb-4"},
                ui.div(
                    {"class": "col-md-4"},
                    ui.div(
                        {"class": "card bg-primary text-white"},
                        ui.div(
                            {"class": "card-body text-center"},
                            ui.h3(ui.output_text("state_count"), {"class": "card-title"}),
                            ui.p("Selected States", {"class": "card-text"})
                        )
                    )
                ),
                ui.div(
                    {"class": "col-md-4"},
                    ui.div(
                        {"class": "card bg-primary text-white"},
                        ui.div(
                            {"class": "card-body text-center"},
                            ui.h3(ui.output_text("selected_year"), {"class": "card-title"}),
                            ui.p("Year", {"class": "card-text"})
                        )
                    )
                ),
                ui.div(
                    {"class": "col-md-4"},
                    ui.div(
                        {"class": "card bg-primary text-white"},
                        ui.div(
                            {"class": "card-body text-center"},
                            ui.h3(ui.output_text("selected_indicator"), {"class": "card-title"}),
                            ui.p("Health Indicator", {"class": "card-text"})
                        )
                    )
                )
            ),
            
            # Chart tabs
            ui.navset_card_tab(
                ui.nav_panel(
                    "Bar Chart",
                    output_widget("bar_plot", height="500px")
                ),
                ui.nav_panel(
                    "Trend Chart",
                    output_widget("trend_plot", height="500px")
                ),
                ui.nav_panel(
                    "Data Table",
                    ui.div(
                        {"class": "mb-3"},
                        ui.input_checkbox_group(
                            "table_columns",
                            "Select Columns to Display:",
                            choices={
                                "State": "State",
                                "Year": "Year", 
                                "Value": "Value",
                                "Region": "Region",
                                "Rank": "Rank"
                            },
                            selected=["State", "Year", "Value"],
                            inline=True
                        )
                    ),
                    ui.output_data_frame("data_table")
                )
            )
        )
    )
)

# Server logic
def server(input, output, session):
    # Initialize theme picker
    shinyswatch.theme_picker_server()
    
    # Handle zoom changes
    @reactive.effect
    def handle_zoom():
        # The zoom functionality is handled by JavaScript
        # This reactive effect ensures the server stays responsive to zoom changes
        if input.zoom_slider():
            pass  # JavaScript handles the actual zoom implementation
    
    # Filtered states list
    @reactive.calc
    def filtered_states():
        search_term = input.state_search().lower() if input.state_search() else ""
        all_states = sorted(health_data['State'].unique())
        
        if search_term:
            # Filter states containing search term
            filtered = [state for state in all_states if search_term in state.lower()]
            return filtered if filtered else all_states
        return all_states
    
    # Select all states functionality
    @reactive.effect
    @reactive.event(input.select_all_states)
    def select_all_states():
        all_states = list(health_data['State'].unique())
        current_selected = input.state() if input.state() else []
        
        if len(current_selected) == len(all_states):
            # If all selected, clear selection
            ui.update_selectize("state", selected=["Alabama"])
        else:
            # Otherwise select all states
            ui.update_selectize("state", selected=all_states)
    
    # Get current data
    @reactive.calc
    def current_data():
        req(input.state, input.year, input.primary_var)
        
        data = health_data[
            (health_data['State'].isin(input.state())) &
            (health_data['year'] == int(input.year()))
        ][['State', 'year', input.primary_var()]].copy()
        
        data = data.rename(columns={input.primary_var(): 'value'})
        data = data.dropna(subset=['value'])
        
        # Add region and ranking
        data['Region'] = data['State'].apply(get_region)
        data['Rank'] = data['value'].rank(ascending=False, method='min').astype(int)
        data = data.rename(columns={'year': 'Year'})
        
        return data
    
    # Get trend data
    @reactive.calc
    def trend_data():
        req(input.state, input.primary_var)
        
        data = health_data[
            health_data['State'].isin(input.state())
        ][['State', 'year', input.primary_var()]].copy()
        
        data = data.rename(columns={input.primary_var(): 'value'})
        data = data.dropna(subset=['value'])
        
        return data
    
    # Status box outputs
    @render.text
    def state_count():
        count = len(input.state()) if input.state() else 0
        return f"{count}"
    
    @render.text  
    def selected_year():
        return input.year() if input.year() else "Not selected"
    
    @render.text
    def selected_indicator():
        if not input.primary_var():
            return "Not selected"
        
        indicator_names = {
            "Adult.obesity..in...": "Obesity Rate",
            "Adult.smoking..in...": "Smoking Rate", 
            "Physical.unhealthy.days": "Physically Unhealthy Days",
            "Mental.unhealthy.days": "Mentally Unhealthy Days"
        }
        return indicator_names.get(input.primary_var(), "Unknown Indicator")
    
    # Bar chart
    @render_widget
    def bar_plot():
        data = current_data()
        if data.empty:
            return None
        
        # Get indicator name
        indicator_names = {
            "Adult.obesity..in...": "Obesity Rate (%)",
            "Adult.smoking..in...": "Smoking Rate (%)",
            "Physical.unhealthy.days": "Physically Unhealthy Days",
            "Mental.unhealthy.days": "Mentally Unhealthy Days"
        }
        y_label = indicator_names.get(input.primary_var(), "Value")
        
        # Create bar chart
        fig = px.bar(
            data.sort_values('value', ascending=True),
            x='value',
            y='State',
            orientation='h',
            title=f"{y_label} Comparison - {input.year()}",
            labels={'value': y_label, 'State': 'State'},
            color='value',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    # Trend chart
    @render_widget
    def trend_plot():
        data = trend_data()
        if data.empty:
            return None
        
        # Get indicator name
        indicator_names = {
            "Adult.obesity..in...": "Obesity Rate (%)",
            "Adult.smoking..in...": "Smoking Rate (%)", 
            "Physical.unhealthy.days": "Physically Unhealthy Days",
            "Mental.unhealthy.days": "Mentally Unhealthy Days"
        }
        y_label = indicator_names.get(input.primary_var(), "Value")
        
        # Create trend chart
        fig = px.line(
            data,
            x='year',
            y='value',
            color='State',
            title=f"{y_label} Trends Over Time",
            labels={'year': 'Year', 'value': y_label, 'State': 'State'},
            markers=True
        )
        
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    # Data table
    @render.data_frame
    def data_table():
        data = current_data()
        if data.empty:
            return pd.DataFrame()
        
        # Filter data based on selected columns
        selected_cols = input.table_columns() if input.table_columns() else ["State", "Year", "Value"]
        
        # Column mapping
        col_mapping = {
            "State": "State",
            "Year": "Year", 
            "Value": "value",
            "Region": "Region",
            "Rank": "Rank"
        }
        
        display_data = data[[col_mapping[col] for col in selected_cols if col in col_mapping]].copy()
        
        # Keep column names in English
        rename_mapping = {
            "State": "State",
            "Year": "Year",
            "value": "Value", 
            "Region": "Region",
            "Rank": "Rank"
        }
        
        final_cols = []
        for col in selected_cols:
            if col in col_mapping:
                original_col = col_mapping[col]
                if original_col in display_data.columns:
                    final_cols.append(rename_mapping.get(original_col, original_col))
        
        display_data.columns = final_cols
        
        # Format numeric columns
        if "Value" in display_data.columns:
            display_data["Value"] = display_data["Value"].round(2)
        
        return display_data.sort_values("Value", ascending=False) if "Value" in display_data.columns else display_data

# Create application
app = App(app_ui, server)

if __name__ == "__main__":
    app.run() 