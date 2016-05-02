import urllib2 as ur
import csv


def data_download(company):
    """Returns downloaded .csv data for a given company"""
    response = ur.urlopen('http://stooq.com/q/d/l/?s='+company+'&i=d')
    downloaded_data = csv.reader(response)
    return downloaded_data


def data_processing(downloaded_data):
    """

    :param downloaded_data:
    :return: [date, opening price, max, min, closing price, volume] for all data points.
    """
    downloaded_data.next()  # removes row with column names
    data = list(downloaded_data)
    for row in data:
        for i in range(1, len(row)):
            row[i] = float(row[i])
    processed_data = data[::-1]  # list inversion
    return processed_data

def closing_prices(processed_data):
    """

    :param processed_data:
    :return: list of closing prices
    """
    closing_prices_list = []
    for i in range(len(processed_data)):
        closing_prices_list.append(processed_data[i][4])
    return closing_prices_list
#print (data_processing(data_download('pkn')))