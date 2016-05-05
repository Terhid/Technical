import urllib2 as ur
import csv


def data_download(company):
    """
    Downloads .csv data for a given company from http://stooq.com

    :param company: string of 3-letter company stock abbreviation
    :return: downloaded data in .csv format with column names
    """
    response = ur.urlopen('http://stooq.com/q/d/l/?s='+company+'&i=d')
    downloaded_data = csv.reader(response)
    return downloaded_data


def data_processing(downloaded_data):
    """
    Processes a .csv data for further use

    :param downloaded_data: data in .csv format with column names
    :return: list of lists [date, opening price, max, min, closing price, volume] for all data points.
    """
    downloaded_data.next()  # removes row with column names
    data = list(downloaded_data)
    for row in data:
        for i in range(1, len(row)):
            row[i] = float(row[i])
    processed_data = data[::-1]  # list inversion
    return processed_data


def opening_prices(processed_data):
    """
    Extracts opening prices from processed data

    :param processed_data: data without column names processed by data_processing() function
    :return: list of opening prices
    """
    opening_prices_list = []
    for i in range(len(processed_data)):
        opening_prices_list.append(processed_data[i][1])
    return opening_prices_list


def closing_prices(processed_data):
    """
    Extracts closing prices from processed data

    :param processed_data: data without column names processed by data_processing() function
    :return: list of closing prices
    """
    closing_prices_list = []
    for i in range(len(processed_data)):
        closing_prices_list.append(processed_data[i][4])
    return closing_prices_list


def max_prices(processed_data):
    """
    Extracts max prices from processed data

    :param processed_data: data without column names processed by data_processing() function
    :return: list of max prices
    """
    max_prices_list = []
    for i in range(len(processed_data)):
        max_prices_list.append(processed_data[i][2])
    return max_prices_list


def min_prices(processed_data):
    """
    Extracts min prices from processed data

    :param processed_data: data without column names processed by data_processing() function
    :return: list of min prices
    """
    min_prices_list = []
    for i in range(len(processed_data)):
        min_prices_list.append(processed_data[i][3])
    return min_prices_list


def volume(processed_data):
    """
    Extracts volume values from processed data

    :param processed_data: data without column names processed by data_processing() function
    :return: list of volume values
    """
    volume_list = []
    for i in range(len(processed_data)):
        volume_list.append(processed_data[i][5])
    return volume_list
