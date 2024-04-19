# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import yfinance as yf
import datetime as dt
import streamlit as st
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error as mse
from prophet.plot import  plot_components_plotly #plot_plotly,

from sklearn.metrics import mean_squared_error
from math import sqrt


st.image("0_dtiuqS8kNB66Mp5P.png", use_column_width=True)
st.header("\n         STOCK PRICE FORECASTING       ")
stock_name = st.text_input("Enter the stock name you want to forecast:")
st.subheader("Here is the Forecasting of ", stock_name )

symbol = 'stock_name'

# Calculate the start and end dates
end_date = dt.datetime.now() - dt.timedelta(days=15)
start_date = end_date - dt.timedelta(days=(5*365))

end_date_real = dt.datetime.now()
start_date_real = end_date_real - dt.timedelta(days=15)


# Download the stock data
stock_data = yf.download(symbol, start=start_date, end=end_date, interval="1d").reset_index()
stock_data_real = yf.download(symbol, start=start_date_real, end=end_date_real, interval="1d").reset_index()
# stock_data=pd.read_csv('stock_data.csv')
# stock_data_real=pd.read_csv('stock_data_real.csv')
# Print the first few rows of the data
print(stock_data.head())
# -

# stock_data_real = yf.download(symbol, start=start_date_real, end=end_date_real, interval="1d").reset_index()
st.write(stock_data_real.tail())
#******************************* ARIMA MODEL FORECAST ******************************************************

#******************************* ARIMA MODEL FORECAST ******************************************************

#******************************* PROPHET MODEL FORECAST ******************************************************
df_real=stock_data_real[['Date','Adj Close']]
df_real.rename(columns={'Date': 'ds', 'Adj Close':'y'}, inplace=True)

df=stock_data[['Date','Adj Close']]


df.info()

import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
fig=plt.plot(df['Date'],df['Adj Close'])
st.line_chart(data=df, x='Date', y='Adj Close')
# st.line_chart(x=df['Date'], y=df['Adj Close'])

df.rename(columns={'Date': 'ds', 'Adj Close':'y'}, inplace=True)


from prophet import Prophet
model=Prophet()

model.fit(df)

# -

import pandas as pd
future = pd.DataFrame(df_real['ds'])
y_actual=df_real['y']


forecast=model.predict(future)

# print(forecast.head())

merged_df=(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper','trend']]).join(y_actual).tail()
print(merged_df)


# Calculate the percentage change in the forecasted price


# from sklearn.metrics import mean_squared_error as mse

#
actual_val= df['y'].tail(1).iloc[0]
forecasted_val=merged_df['yhat'].iloc[0]
change = ((forecasted_val-actual_val)/100)
st.subheader('Components used for Forecast :')
fig = model.plot_components(forecast)  # Use correct function and adjust figsize

# Display the plot in Streamlit
st.pyplot(fig)

st.subheader('Prophet Forecast :')
print(change, actual_val ,forecasted_val)
st.write("\t\tChange in next 15 days :",change)
plt.figure(figsize=(15,7))
plot=model.plot(forecast)

st.write(plot)
mse=mse(y_actual,forecast['yhat'])

st.write("MSE of Forecasted Price  : ",mse)


# plt.show()
# import plotly.graph_objs as go
# # +
# from prophet.plot import plot_plotly, plot_components_plotly
from prophet.plot import plot_plotly, plot_components_plotly
fig=plot_plotly(model, forecast)



figure=plot_components_plotly(model, forecast)
st.plotly_chart(fig)
#******************************* PROPHET MODEL FORECAST ******************************************************