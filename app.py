import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input
import plotly.express as px
df = pd.read_csv('spacex.csv')

max_value = df['Payload Mass (kg)'].max()
min_value = df['Payload Mass (kg)'].min()

# Initialize the app
app=Dash(__name__)

app.layout = html.Div([html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),   
                         dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    searchable=True
                                    ),
                         dcc.Graph(id = "site_graph", figure={}),
                         dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        value=[min_value, max_value]),
                         dcc.Graph(id = "success-payload-scatter-chart", figure={}),
                      ])

@callback(
    [Output(component_id="site_graph", component_property="figure"),
    Output(component_id="success-payload-scatter-chart", component_property="figure")],
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)
def updatePie(selected_site,range):   
    min=range[0]
    max=range[1]
    df_scatter=df
    df_scatter = df[df["Payload Mass (kg)"]>=min]
    df_scatter = df_scatter[df["Payload Mass (kg)"]<=max]

    if selected_site == "ALL":
        scatter = px.scatter(df_scatter,x="Payload Mass (kg)",y="class", color="Booster Version Category")
        
    else:
        df_scatter = df_scatter[df_scatter["Launch Site"]==selected_site]

        scatter = px.scatter(df_scatter, x="Payload Mass (kg)", y="class", color="Booster Version Category")


    if selected_site == "ALL":
        title = "All Sites Success Launches"
        filtered_df = df
        pie_chart = px.pie(df, names="Launch Site", values="class", title=title)   
        return pie_chart, scatter
    else:
        title = f"{selected_site} Success Launches"
        filtered_df = df[df["Launch Site"] == selected_site]

        success_counts = filtered_df.groupby("class").size()
        labels = success_counts.index.tolist()
        values = success_counts.values.tolist()

        pie_chart = px.pie(names=labels, values=values, title=title)    


        return pie_chart, scatter
    
#run the app
if __name__=="__main__":
    app.run(debug=True)
