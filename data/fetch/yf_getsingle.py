from datetime import datetime
from concurrent import futures
import yfinance as yt
import os

if __name__ == '__main__':
	stock = 'HEX-USD'
	try:
		print("geting stock data of: %s"  % (stock))
		st = yt.Ticker(stock)
		df = st.history(period='5y')
		output_name = stock + '_data.csv'
		df.to_csv(output_name)
	except Exception as e:
		print(e)
	
