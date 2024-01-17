#SQIT 3073 BUSINESS ANALYTIC PROGRAMMING (A)
#GROUP PROJECT

#CHEOK YOKE BOON 286000
#WONG XIANG YI 286267
#LAI YING QI 286482
#KEE LOO SIANG 287312
#LOH MAN PIN 287504

#import the libraries 
import pandas as pd                 #for data manipulation and analysis
import numpy as np                  #perform numerical computing like arrays
import dash                         #for building interactive web applications.
from dash import dcc, html          #for layout construction    
import dash_bootstrap_components as dbc #for enhance styling of webpage
from flask import Flask             #for web server functionality
import plotly.graph_objects as go   #for creating interactive data visualization
from sklearn.linear_model import LinearRegression # for predictive modelling

# ìnitiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# read the data files
df1 = pd.read_csv('data.csv')
df2 = pd.read_csv('hies_state.csv')

# build the header component
header = html.H1('Profit and Spending of Startup of a company')


# Component 1
spendingfig = go.FigureWidget()
spendingfig.add_scatter(name="R&D Spend", x=df1["Year"], y=df1["R&D Spend"])
spendingfig.add_scatter(name="Administration", x=df1["Year"], y=df1["Administration"])
spendingfig.add_scatter(name="Marketing Spend", x=df1["Year"], y=df1["Marketing Spend"])

# Time series forecasting using Linear Regression for "R&D Spend" column
X = df1[["Year"]].values
y = df1["R&D Spend"].values

model = LinearRegression()
model.fit(X, y)

forecast_years = np.arange(df1["Year"].max() , df1["Year"].max() + 12)
forecast = model.predict(forecast_years.reshape(-1, 1))

spendingfig.add_scatter(name="R&D Spend Forecast", x=forecast_years, y=forecast)

# Time series forecasting using Linear Regression for "Administration" column
X = df1[["Year"]].values
y = df1["Administration"].values

model = LinearRegression()
model.fit(X, y)

forecast_years = np.arange(df1["Year"].max() , df1["Year"].max() + 12)
forecast = model.predict(forecast_years.reshape(-1, 1))

spendingfig.add_scatter(name="Administration Forecast", x=forecast_years, y=forecast)

# Time series forecasting using Linear Regression for "Marketing Spend" column
X = df1[["Year"]].values
y = df1["Marketing Spend"].values

model = LinearRegression()
model.fit(X, y)

forecast_years = np.arange(df1["Year"].max() , df1["Year"].max() + 12)
forecast = model.predict(forecast_years.reshape(-1, 1))

spendingfig.add_scatter(name="Marketing Spend Forecast", x=forecast_years, y=forecast)

spendingfig.update_layout(title="Spending of Each Department of company in Years")


#Component 2
profitfig = go.FigureWidget()
profitfig.add_scatter(name="Profit of company", x=df1["Year"], y=df1["Profit"])
profitfig.add_scatter(name="Sales of company(pieces)", x=df1["Year"], y=df1["Sales (pieces)"])

# Time series forecasting using Linear Regression for "Profit" column
X = df1[["Year"]].values
y = df1["Profit"].values

model = LinearRegression()
model.fit(X, y)

forecast_years = np.arange(df1["Year"].max() , df1["Year"].max() + 12)
forecast = model.predict(forecast_years.reshape(-1, 1))

profitfig.add_scatter(name="Profit of company Forecast", x=forecast_years, y=forecast)

# Time series forecasting using Linear Regression for "Sales (pieces)" column
X = df1[["Year"]].values
y = df1["Sales (pieces)"].values

model = LinearRegression()
model.fit(X, y)

forecast_years = np.arange(df1["Year"].max() , df1["Year"].max() + 12)
forecast = model.predict(forecast_years.reshape(-1, 1))

profitfig.add_scatter(name="Sales of company(pieces) Forecast", x=forecast_years, y=forecast)

profitfig.update_layout(title="Profit and Sales of the company in Years")


#Component 3
statefig = go.FigureWidget()
statefig.add_trace(go.Bar(x=df2["state"], y=df2["income_mean"], name="Income Mean (RM)"))
statefig.add_trace(go.Bar(x=df2["state"], y=df2["expenditure_mean"], name="Expenditure Mean (RM)"))

statefig.update_layout(title="Mean of Income and Expenditure of States in 2023")
# design the app layout
app.layout = html.Div(
    [
        dbc.Row([
            header
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=profitfig)  
            ), 
            dbc.Col(
                dcc.Graph(figure=spendingfig)
            )
        ]),
        dbc.Row([
             dcc.Graph(figure=statefig)
        ])
])

# run the app
app.run_server(debug=True)
