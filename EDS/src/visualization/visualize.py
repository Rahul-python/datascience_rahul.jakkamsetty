# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 01:33:05 2020

@author: Rahul Jakkamsetty
"""

import pandas as pd
import numpy as np

import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import plotly.graph_objects as go



df_input_large=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')
df_SIR_data = pd.read_csv('data/processed/SIR_fitted_parameters.csv',sep=';')
df_analyse = pd.read_csv('data/processed/COVID_total_flat_table.csv',sep=';')
fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Applied Data Science on COVID-19 data
    In this project, First the COVID-19 data especially the confirmed cases are collected, processed and prepared for modelling and simulation.
    The simulation model used is SIR.

    '''),

    dcc.Markdown('''
    ## Use Dropdown for choosing multiple countries.
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
        value=['US', 'Germany','Italy'], # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select Timeline of confirmed COVID-19 cases or the approximated doubling time
        '''),


    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Timeline of Confirmed cases ', 'value': 'confirmed'},
        {'label': 'Timeline of Confirmed cases (Filtered)', 'value': 'confirmed_filtered'},
        {'label': 'Timeline of Doubling Rate', 'value': 'confirmed_DR'},
        {'label': 'Timeline of Doubling Rate (Filtered)', 'value': 'confirmed_filtered_DR'},
    ],
    value='confirmed',
    multi=False
    ),

    dcc.Graph(figure=fig, id='main_window_slope'),


    dcc.Markdown('''
    ## SIR Visualisation. We used SIR model for simulation of confirmed cases or infected people with COVID-19.
    Please use the drop down for choosing multiple countires.
    ''',style={'text-align':'left'}),


    dcc.Dropdown(
    id='country_drop_down_sir',
            options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
            value=['US','India'], # which are pre-selected
            multi=True,
            style=dict(
                        width='60%',
                        verticalAlign="middle"
                    ),
        ),


        
       
    
      dcc.Graph(figure=fig, id='sir_chart'),
    
        ])



@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])
def update_figure(country_list,show_doubling):


    if 'doubling_rate' in show_doubling:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days (larger numbers are better #stayathome)'
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
              }


    traces = []
    for each in country_list:

        df_plot=df_input_large[df_input_large['country']==each]

        if show_doubling=='doubling_rate_filtered':
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()
       #print(show_doubling)


        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis=my_yaxis
        )
    }
@app.callback(
    Output('sir_chart', 'figure'),
    [Input('country_drop_down_sir', 'value')])
def update_figure(country_list):
    traces = []
    fig =go.Figure()
    if(len(country_list) > 0):
        for each in country_list:
            country_data = df_analyse[each][35:100]
            ydata = np.array(country_data)
            t = np.arange(len(ydata))
            fitted = np.array(df_SIR_data[each])
            #t, ydata, fitted = Handle_SIR_Modelling(ydata)
            fig.add_trace(go.Scatter(
                x = t,
                y = ydata,
                mode = 'markers+lines',
                name = each+str('_Ground_Truth'),
                opacity = 0.9
            ))
            fig.add_trace(go.Scatter(
                x = t,
                y = fitted,
                mode = 'markers+lines',
                name = each+str('_Simulated_data'),
                opacity = 0.9
            ))

    fig.update_layout(dict(
            width = 1280,
            height = 720,
            title = 'Fit of SIR model for: '+', '.join(country_list),
            xaxis = {
                'title': 'Days', #'Fit of SIR model for '+str(each)+' cases',
                'tickangle': -45,
                'nticks' : 20,
                'tickfont' : dict(size = 14, color = '#7F7F7F')
            },
            yaxis = { 'type': 'log',
                'title': 'Infected people (log scale)'
               
            },
            template="ggplot2",
        ))        
    return fig
if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)