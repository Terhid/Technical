import math


def fractal_alpha(n, data, i):
    """
    Calculates the value of a variable alpha, used to calculate FRAMA

    Formula:
    alpha = exp(W*(D - 1))
    W = -4.6 constant (can be changed)
    D = (ln(HL1 + HL2) - ln(HL)) / ln(2)
    HL = (max(n) - min(n)) / n
    HL1 = (max([0, 1/2n]) - min([0, 1/2n])) / 1/2n
    HL2 = (max([1/2n, n]) - min([1/2n, n])) / 1/2n

    alpha < 0.01 => alpha = 0.01
    alpha > 1 => alpha = 1

    :param n: FRAMA period
    :param data: list of values (usually: opening or closing prices)
    :param i: int of day, on which we calculate FRAMA
    :return: the value of fractal dimension for a given day
    """
    w = -4.6
    first_half_extrema = maxmin(data[i + n // 2:i + n])
    second_half_extrema = maxmin(data[i:i + n // 2])
    extrema = maxmin(data[i:i + n])
    hl_1 = (first_half_extrema[0] - first_half_extrema[1]) / (0.5 * n)
    hl_2 = (second_half_extrema[0] - second_half_extrema[1]) / (0.5 * n)
    hl = (extrema[0] - extrema[1]) / n
    d = (math.log(hl_1 + hl_2, math.e) - math.log(hl, math.e)) / math.log(2, math.e)
    alpha = math.exp(w * (d - 1))
    if alpha > 1:
        alpha = 1
    if alpha < 0.01:
        alpha = 0.01
    return alpha


def maxmin(list):
    """
    Calculates maximum and minimum of a list

    :param list: list of values
    :return: tuple (max,min) containing max and min value for a given list
    """
    max = list[0]
    min = list[0]
    for i in range(len(list)):
        if list[i] > max:
            max = list[i]
        if list[i] < min:
            min = list[i]
    return (max, min)
