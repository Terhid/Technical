import data_processing as dp
import matplotlib.pyplot as plt
import indicators_subsidiary_functions as isf


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


def frama(n, data):
    """
    Calculates Fractal Adaptive Moving Average (FRAMA)

    Formula:
    FRAMA(n) = EMA(n), where alpha is the variable returned by fractal_alpha() function

    :param n: FRAMA period
    :param data: list of values (usually: opening or closing prices)
    :return: list of FRAMA(n) for given data for len(data - 2n) points
    """
    emalist = []
    n = int(n)

    for i in range(len(data) - n + 1):
        numerator = 0
        denominator = 0
        alpha = isf.fractal_alpha(n, data, i)
        for j in range(i, i + n):
            numerator += (1 - alpha) ** (j-i) * data[j]
            denominator += (1 - alpha) ** (j-i)
        emalist.append(numerator / denominator)

    return emalist


def testing():
    company = raw_input('Enter company name: ')
    data = dp.data_processing(dp.data_download(company))
    datalist = []
    for i in range(1000):
        datalist.append(data[i][4])

    smaa = sma(50, datalist)
    emalist = ema(50, datalist)
    demaa = dema(50, datalist)
    framaa = frama(50, datalist)
    print(len(dema(50, datalist)))
    print len(emalist)
    print (len(smaa))
    print (len(framaa))

    plt.plot(datalist)
    plt.plot(framaa)
    plt.plot(smaa, color='red')
    plt.plot(emalist, color='orange')
    plt.plot(demaa, color='black')
    plt.show()


testing()
