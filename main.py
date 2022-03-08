import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


def read_column(n):
    with open("emg.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return [float(line[n]) for line in csv_reader]


# def calc_disp(values, window):
#     mat1, mat2 = 0, 0
#     for j in range(0, window):
#         mat1 += values[j]
#         mat2 += values[j] ** 2
#     disp = [mat2 / window - (mat1 / window) ** 2] * window
#     for i in range(window, len(values)):
#         mat1 = mat1 - values[i - 1] + values[i]
#         mat2 = mat2 - values[i - 1] ** 2 + values[i] ** 2
#         d = mat2 / window - (mat1 / window) ** 2
#         if d > disp[i - 1]:
#             for j in range(i - 1, i - window, -1):
#                 disp[j] = d
#         disp.append(d)
#     return disp

def calc_disp(values, window):
    disp = []
    for i in range(window, len(values) - window, window):
        mat1, mat2 = 0, 0
        for j in range(i, i + window):
            mat1 += values[j]
            mat2 += values[j] ** 2
        disp.append(mat2 / window - (mat1 / window) ** 2)
    return disp


def rfft(values, window):
    freq = []
    for i in range(0, len(values) - window, window):
        spectrum = np.fft.rfft(values[i:i + window])
        abs_spec = np.abs(spectrum)
        freq.append(sum(abs_spec[len(abs_spec) // 2:len(abs_spec)]))
    return freq


def plot(dots, disp, lim_disp, freq, window, lim_freq):
    fig, ax = plt.subplots(2)
    for i in range(2):
        ax[i].yaxis.set_major_locator(MaxNLocator(20))
        ax[i].plot(dots)
    fig.set_size_inches(16, 9)
    ax[0].set_title('По дисперсии:')
    ax[1].set_title('По частотному спектру:')
    for i in range(len(disp)):
        if disp[i] > lim_disp:
            ax[0].axvspan(i * window, (i + 1) * window, alpha=0.5, color='red')
    for i in range(len(freq)):
        if freq[i] > lim_freq:
            ax[1].axvspan(i * window, (i + 1) * window, alpha=0.5, color='red')
    plt.show()


def main():
    window = 40
    lim_disp = 0.0008
    lim_freq = 1.2
    column = read_column(1)
    disp = calc_disp(column, window)
    freq = rfft(column, window)
    plot(column, disp, lim_disp, freq, window, lim_freq)


if __name__ == '__main__':
    main()
