import urllib2 as ur
import csv
import time

def data_download(company):
    """Returns downloaded .csv data for a given company"""
    response = ur.urlopen('http://stooq.com/q/d/l/?s='+company+'&i=d')
    downloaded_data = csv.reader(response)
    return downloaded_data

def data_processing(downloaded_data):
    """Returns processed data"""
    downloaded_data.next() #removes row with column names
    data = list(downloaded_data)

    for row in data:
        for i in range(1,len(row)):
            row[i] = float(row[i])
        data = time.strptime(row[0], '%Y-%m-%d')
    print(type(data))
    processed_data = data[::-1] #list inversion
    return processed_data

# company = raw_input('Enter company name: ')
# data = data_download(company)
# data = data_processing(data)

