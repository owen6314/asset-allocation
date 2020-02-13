import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('ADBE_data.csv')

fig = go.Figure(data=go.Ohlc(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']))

fig.show()