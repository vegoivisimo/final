import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


url ="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
try:
    spacex_df = pd.read_csv(url)
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)


required_columns = ['Launch Site', 'Payload Mass (kg)', 'class', 'Booster Version']
if not all(col in spacex_df.columns for col in required_columns):
    print(f"Dataset missing required columns. Found: {list(spacex_df.columns)}")
    exit(1)

app = dash.Dash(__name__)


launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
]


app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'fontSize': '24px'}  # corrected camelCase and px
    ),
    
  
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites,
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True,
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
    
   
    html.Br(),
    html.P("Payload range (kg):", style={'textAlign': 'center'}),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[0, 10000],
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
   
    html.Br(),
    dcc.Graph(id='success-payload-scatter-chart')
])


@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    try:
        if selected_site == 'ALL':
          
            success_df = spacex_df[spacex_df['class'] == 1]
            fig = px.pie(
                success_df,
                values='class',           
                names='Launch Site',      
                title='Total Successful Launches by Site'
            )
            fig.update_traces(textinfo='label+percent')
        else:
          
            filtered = spacex_df[spacex_df['Launch Site'] == selected_site]
            counts = (
                filtered['class']
                .value_counts()
                .reset_index()
                .rename(columns={'index': 'class', 'class': 'count'})
            )
            counts['outcome'] = counts['class'].map({0: 'Failed', 1: 'Success'})

            fig = px.pie(
                counts,
                values='count',
                names='outcome',
                title=f'Success vs. Failure for {selected_site}',
            )
            fig.update_traces(textinfo='label+percent')
        return fig
    except Exception as e:
        print(f"Error in pie chart callback: {e}")
        return px.pie(title='Error rendering chart')


@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    try:
      
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]
        if selected_site != 'ALL':
            filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            title=(
                'Payload vs. Launch Outcome for All Sites'
                if selected_site == 'ALL' else
                f'Payload vs. Launch Outcome for {selected_site}'
            ),
            labels={'class': 'Launch Outcome (0=Failed, 1=Success)'},
            hover_data=['Flight Number', 'Launch Site']
        )
        fig.update_yaxes(tickvals=[0, 1], ticktext=['Failed (0)', 'Success (1)'])
        return fig
    except Exception as e:
        print(f"Error in scatter chart callback: {e}")
        return px.scatter(title='Error rendering chart')


if __name__ == '__main__':
    print("Starting Dash server. Open http://127.0.0.1:8051 in your browser.")
    app.run(debug=True, port=8051)