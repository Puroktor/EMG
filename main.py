import csv
import math
import scipy.fft
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def read_column(n):
    with open("emg.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return [float(line[n]) for line in csv_reader]


def fft(values, window, starting):
    freq_list = []
    for i in range(0, len(values) - window, window):
        freq = scipy.fft.fft(values[i:i + window])[starting:window // 2]
        freq = np.abs(freq)
        freq_list.append(freq)
    return freq_list


def analyse_freq(freq_list, starting):
    activity_list = []
    for freq in freq_list:
        max_freq = np.max(freq)
        i_freq = np.where(freq == max_freq)[0]
        mx = np.sum(freq) / len(freq)
        mx2 = np.sum(freq ** 2) / len(freq)
        disp = mx2 - mx ** 2
        activity_list.append(30 <= i_freq + starting <= 50
                             and max_freq >= mx + math.sqrt(disp))
    return activity_list


def plot(dots, activity_list, window):
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(20))
    ax.plot(dots)
    fig.set_size_inches(16, 9)
    for i in range(len(activity_list)):
        if activity_list[i]:
            ax.axvspan(i * window, (i + 1) * window, alpha=0.5, color='red')
    plt.show()


def main():
    column = read_column(0)
    window = 200
    starting = 20
    freq_list = fft(column, window, starting)
    activity_list = analyse_freq(freq_list, starting)
    plot(column, activity_list, window)


if __name__ == '__main__':
    main()
