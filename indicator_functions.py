import data_processing as dp


def simple_ema(n, a, data):
    """Returns EMA(N) for a days back"""
    i = 0
    numerator = 0
    denominator = 0.00000001
    n = int(n)
    alpha = 2.0 / (n + 1)
    for row in data[a - 1:n + a - 1]:
        numerator += (1 - alpha) ** i * row[4]
        denominator += (1 - alpha) ** i
        i += 1
    ema = numerator / denominator
    return ema


def ema(n, b1, b2, list):
    """Returns EMA(N) of a list for a given [b1,b2] interval"""
    emalist = []
    numerator = 0
    denominator = 0
    n = int(n)
    alpha = 2.0 / (n + 1)
    for i in range(0, b2 - b1):
        numerator += (1 - alpha) ** i * list[i + b1]
        denominator += (1 - alpha) ** i
        EMA = numerator / denominator
        emalist.append(EMA)

    emalist = emalist[::-1]
    return emalist


def testing():
    company = raw_input('Enter company name: ')
    data = dp.data_processing(dp.data_download(company))
    datalist = []
    for i in range(1000):
        datalist.append(data[i][4])
    dane_nieodwr = datalist[::-1]
    emalist = ema(50, 1, 50, dane_nieodwr)
    print (emalist)


testing()

