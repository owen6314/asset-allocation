from datetime import datetime
import yfinance as yt
import os

# possible choice: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
time_period = '60d'
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# default = '1d'
interval = '5m'


if __name__ == '__main__':
	stock = 'A'
	try:
		print("geting stock data of: %s"  % (stock))
		st = yt.Ticker(stock)
		df = st.history(period=time_period, interval=interval)
		output_name = stock + '_data.csv'
		df.to_csv(output_name)
	except Exception as e:
		print(e)
	
