from datetime import datetime
from concurrent import futures
import yfinance as yf
import os
import pandas as pd
import requests 
from bs4 import BeautifulSoup

# possible choice: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
time_period = 'max'

def download_stock(stock):
	""" try to query the iex for a stock, if failed note with print """
	try:
		print("geting stock data of: %s"  % (stock))
		stock_df = yf.Ticker(stock).history(period=time_period)
		stock_df['Name'] = stock
		output_name = stock + '_data.csv'
		stock_df.to_csv(output_name)
	except:
		bad_names.append(stock)
		print('bad: %s' % (stock))

def get_top_symbols():
	names=[]

	CryptoCurrenciesUrl = "https://finance.yahoo.com/etfs"
	r= requests.get(CryptoCurrenciesUrl)
	data=r.text
	soup = BeautifulSoup(data, features="html.parser")
	allList = soup.find_all('tr', attrs={'class':'simpTblRow'})

	count = 0
	for listing in allList:
	   # print (listing)
	   for symbols in soup.find_all('td', attrs = {'aria-label':'Symbol'}):
	      if count < 15:
	         names.append(symbols.text)
	         count += 1
	      else:
	         break

	print (names)
	return names

if __name__ == '__main__':

	now_time = datetime.now()
	
	# df = pd.read_csv('etf_list.csv')
	
	# etfs = df['Symbol'].tolist()
	etfs = get_top_symbols()
		
	bad_names =[] #to keep track of failed queries

	"""here we use the concurrent.futures module's ThreadPoolExecutor
		to speed up the downloads buy doing them in parallel 
		as opposed to sequentially """

	#set the maximum thread number
	max_workers = 50

	workers = min(max_workers, len(etfs)) #in case a smaller number of stocks than threads was passed in
	with futures.ThreadPoolExecutor(workers) as executor:
		res = executor.map(download_stock, etfs)

	
	""" Save failed queries to a text file to retry """
	if len(bad_names) > 0:
		with open('failed_queries.txt','w') as outfile:
			for name in bad_names:
				outfile.write(name+'\n')

	# timing:
	finish_time = datetime.now()
	duration = finish_time - now_time
	minutes, seconds = divmod(duration.seconds, 60)
	print(f'The threaded script took {minutes} minutes and {seconds} seconds to run.')
