import data_processing as dp
import matplotlib.pyplot as plt
import indicators_subsidiary_functions as isf
import numpy


def sma(n, data):
    """
    Calculates Simple Moving Average (SMA)
    Formula:
    SMA(data_x, n) = (data_x + ... + data_(x + n)) / n, O(n^2)
    :param n: SMA Period
    :param data: list of values (usually: opening or closing prices)
    :return: list of SMA(n) for given data for len(data - n) points
    """
    smalist = []
    n = int(n)

    for i in range(len(data) - n + 1):
        sum = 0
        for j in range(i, i + n):
            sum += data[j]
        smalist.append(sum / n)
    return smalist


def ema(n, data):
    """
    Calculates Exponential Moving Average (EMA)
    Formula:
    EMA(data_x, n, alpha) = ((1 - alpha)^0*data_x + (1 - alpha)^1*data_(x + 1) + ... + (1 - alpha)^n*data_(x + n)) /
    ((1 - alpha)^0 + ... + (1 - alpha)^n), O(n^2)
    :param n: EMA period
    :param data: list of values (usually: opening or closing prices)
    :return: list of EMA(n) for given data for len(data - n) points
    """
    emalist = []
    n = int(n)
    alpha = 2.0 / (n + 1)
    for i in range(len(data) - n + 1):
        numerator = 0
        denominator = 0
        for j in range(i, i + n):
            numerator += (1 - alpha) ** (j-i) * data[j]
            denominator += (1 - alpha) ** (j-i)
        emalist.append(numerator / denominator)

    return emalist


def dema(n, data):
    """
    Calculates Double Exponential Moving Average (DEMA)
    Formula:
    DEMA(n) = 2*EMA(n) - EMA(EMA(n)), O(n^3)
    :param n: DEMA period
    :param data: list of values (usually: opening or closing prices)
    :return: list of DEMA(n) for given data for len(data - 2n) points
    """
    n = int(n)
    demalist = []
    list_1 = ema(n, data)
    list_2 = ema(n, ema(n, data))
    for i in range(len(list_2)):
        demalist.append(2 * list_1[i] - list_2[i])

    return demalist


def frama(n, data, w=-4.6):
    """
    Calculates Fractal Adaptive Moving Average (FRAMA)
    Formula:
    FRAMA(n) = EMA(n), where alpha is the variable returned by fractal_alpha() function
    :param n: FRAMA period
    :param data: list of values (usually: opening or closing prices)
    :param w: W constant in alpha variable calculation in fractal_alpha(), default = -4.6
    :return: list of FRAMA(n) for given data for len(data - 2n) points
    """
    emalist = []
    n = int(n)

    for i in range(len(data) - n + 1):
        numerator = 0
        denominator = 0
        alpha = isf.fractal_alpha(n, data, i, w)
        for j in range(i, i + n):
            numerator += (1 - alpha) ** (j-i) * data[j]
            denominator += (1 - alpha) ** (j-i)
        emalist.append(numerator / denominator)

    return emalist


def macd(n1, n2, data):
    """
    Calculates MACD (Moving Average Convergence Divergence) from two EMAs.

    :param n1: EMA1 period
    :param n2: EMA2 period
    :param data: list of values (usually: opening or closing prices)
    :return: list of MACD for given data for len(data - (len(longer EMA) - len(shorter EMA))) points
    """
    macd = []
    ema1 = ema(n1, data)
    ema2 = ema(n2, data)
    if len(ema1) > len(ema2):
        ema1 = ema1[n2-n1:]
        for i in range(len(ema1)):
            macd.append(ema2[i] - ema1[i])
    if len(ema2) > len(ema1):
        ema2 = ema2[n1-n2:]
        for i in range(len(ema1)):
            macd.append(ema1[i] - ema2[i])

    return macd


def rsi(n, data):
    """
    Calculates Relative Strength Index (RSI)
    Formula:
    RSI = 100 - 100 / (1 + RS)
    RS = Average Gain / Average Loss
    :param n: RSI period
    :param data: list of values (usually: opening or closing prices)
    :return: list of RSI(n) for given data for len(data - n) points
    """
    n = int(n)
    alpha = 2.0 / (n + 1)
    rsilist = []

    for i in range(len(data) - n):
        denom_ups = 0
        denom_downs = 0
        enum_ups = 0
        enum_downs = 0

        for j in range(0, n):
            if numpy.sign(data[i + j + 1] - data[i + j]) > 0:
                enum_ups += (1 - alpha) ** j * (data[i + j + 1] - data[i + j])
                denom_ups += (1 - alpha) ** j

            else:
                enum_downs += (1 - alpha) ** j * (data[i + j + 1] - data[i + j])
                denom_downs += (1 - alpha) ** j

        if denom_ups == 0:
            denom_ups = 0.000000000000001
        if denom_downs == 0:
            denom_downs = 0.000000000000001

        downs = enum_downs / denom_downs
        ups = enum_ups / denom_ups

        if ups == 0:
            ups = 0.000000000000001
        if downs == 0:
            downs = 0.000000000000001

        rs = abs(ups / downs)
        rsi = 100 - (100 / (1 + rs))
        rsilist.append(rsi)

    return rsilist


def testing():
    company = raw_input('Enter company name: ')
    data = dp.data_processing(dp.data_download(company))
    datalist = []
    for i in range(1000):
        datalist.append(data[i][4])

    smaa = sma(50, datalist)
    emalist = ema(50, datalist)
    demaa = dema(50, datalist)
    framaa = frama(50, datalist, w=-4.5)
    rsii = rsi(14, datalist)
    macdd = macd(12, 26, datalist)
    print(len(dema(50, datalist)))
    print len(emalist)
    print (len(smaa))
    print (len(framaa))
    print(len(rsii))
    print(len(macdd))
    print(macdd)
    print(len(macdd) == len(ema(26, datalist)))

    plt.style.use('ggplot')
    plt.plot(datalist)
    plt.plot(framaa)
    plt.plot(smaa)
    plt.plot(emalist)
    plt.plot(demaa)
    plt.plot(macdd)
    plt.show()


testing()