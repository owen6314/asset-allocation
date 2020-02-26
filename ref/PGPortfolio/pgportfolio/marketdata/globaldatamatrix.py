from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pandas as pd
from pgportfolio.tools.data import panel_fillna
from pgportfolio.constants import *
import sqlite3
from datetime import datetime
import logging


class HistoryManager:
    # if offline ,the coin_list could be None
    # NOTE: return of the sqlite results is a list of tuples, each tuple is a row
    def __init__(self, coin_number, end):
        self.__storage_period = DAY
        self._coin_number = coin_number
        self.__coins = None

    @property
    def coins(self):
        return self.__coins

    def get_global_data_matrix(self, start, end, period, features):
        """
        :return a numpy ndarray whose axis is [feature, coin, time]
        """
        return self.get_global_panel(start, end, period, features).values

    def get_global_panel(self, start, end, period, features):
        """
        :param start/end: linux timestamp in seconds
        :param period: time interval of each data access point
        :param features: tuple or list of the feature names
        :return a panel, [feature, coin, time]
        """
        start = int(start)
        end = int(end)
        coins = self.select_coins(start=start, end=end)
        self.__coins = coins
        for coin in coins:
            self.update_data(start, end, coin)

        if len(coins)!=self._coin_number:
            raise ValueError("the length of selected coins %d is not equal to expected %d"
                             % (len(coins), self._coin_number))

        logging.info("feature type list is %s" % str(features))
        self.__checkperiod(period)
        connection = sqlite3.connect(DATABASE_DIR)

        time_index = pd.to_datetime(list(range(start, end+1, period)), unit='s')
        time_index = time_index.normalize()
        panel = pd.Panel(items=features, major_axis=coins, minor_axis=time_index, dtype=np.float32)

        try:
            for row_number, coin in enumerate(coins):
                for feature in features:
                    # NOTE: transform the start date to end date
                    if feature == "close":
                        sql = ("SELECT date as date_norm, close FROM History WHERE"
                               " date_norm>={start} and date_norm<={end}" 
                               " and name=\"{coin}\"".format(
                               start=start, end=end, coin=coin))
                    elif feature == "open":
                        sql = ("SELECT date+{period} AS date_norm, open FROM History WHERE"
                               " date_norm>={start} and date_norm<={end}" 
                               " and name=\"{coin}\"".format(
                               start=start, end=end, period=period, coin=coin))
                    elif feature == "high":
                        sql = ("SELECT date_norm, MAX(high)" +
                               " FROM (SELECT date+{period}"
                               " AS date_norm, high, name FROM History)"
                               " WHERE date_norm>={start} and date_norm<={end} and name=\"{coin}\""
                               " GROUP BY date_norm".format(
                                    period=period,start=start,end=end,coin=coin))

                    elif feature == "low":
                        sql = ("SELECT date_norm, MIN(low)" +
                                " FROM (SELECT date+{period}"
                                " AS date_norm, low, name FROM History)"
                                " WHERE date_norm>={start} and date_norm<={end} and name=\"{coin}\""
                                " GROUP BY date_norm".format(
                                    period=period,start=start,end=end,coin=coin))
                    else:
                        msg = ("The feature %s is not supported" % feature)
                        logging.error(msg)
                        raise ValueError(msg)
                    serial_data = pd.read_sql_query(sql, con=connection,
                                                    parse_dates=["date_norm"])
                    temp = serial_data["date_norm"].dt.normalize()
                    del serial_data['date_norm']
                    serial_data.index = temp
                    squeezed_data = serial_data.squeeze()
                    panel.loc[feature, coin, serial_data.index] = squeezed_data
                    panel = panel_fillna(panel, "both")
        finally:
            connection.commit()
            connection.close()
        return panel

    # select all available coins database
    def select_coins(self, start, end):
        logging.info("select coins offline from %s to %s" % (datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M'),
                                                                datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M')))
        connection = sqlite3.connect(DATABASE_DIR)
        try:
            cursor=connection.cursor()
            cursor.execute('SELECT name FROM History WHERE date>=? and date<=? GROUP BY name;',
                           (int(start), int(end)))
            coins_tuples = cursor.fetchall()

            if len(coins_tuples) != self._coin_number:
                logging.error("the sqlite error happend")
        finally:
            connection.commit()
            connection.close()
        coins = []
        for tuple in coins_tuples:
            coins.append(tuple[0])
        logging.debug("Selected coins are: "+str(coins))
        return coins

    def __checkperiod(self, period):
        if period == FIVE_MINUTES:
            return
        elif period == FIFTEEN_MINUTES:
            return
        elif period == HALF_HOUR:
            return
        elif period == TWO_HOUR:
            return
        elif period == FOUR_HOUR:
            return
        elif period == DAY:
            return
        else:
            raise ValueError('peroid has to be 5min, 15min, 30min, 2hr, 4hr, or a day')

    # add new history data into the database
    def update_data(self, start, end, coin):
        connection = sqlite3.connect(DATABASE_DIR)
        try:
            cursor = connection.cursor()
            min_date = cursor.execute('SELECT MIN(date) FROM History WHERE name=?;', (coin,)).fetchall()[0][0]
            max_date = cursor.execute('SELECT MAX(date) FROM History WHERE name=?;', (coin,)).fetchall()[0][0]

            if min_date==None or max_date==None:
                self.__fill_data(start, end, coin, cursor)

        finally:
            connection.commit()
            connection.close()