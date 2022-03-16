import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


def read_column(n):
    with open("emg.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return [float(line[n]) for line in csv_reader]


def analyse_freq(values, window, med):
    activity_list = []
    for i in range(0, len(values) - window, window):
        avg = np.average(values[i:i + window])
        activity_list.append(avg > med)
    return activity_list


def plot(dots, med, activity_list, window):
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(20))
    ax.plot(dots)
    ax.plot(med)
    fig.set_size_inches(15, 7)
    for i in range(len(activity_list)):
        if activity_list[i]:
            ax.axvspan(i * window, (i + 1) * window, alpha=0.5, color='red')
    plt.show()


def main():
    column = read_column(0)
    window = 200
    med = np.median(column)
    meds = [med for _ in range(len(column))]
    activity_list = analyse_freq(column, window, med)
    plot(column, meds, activity_list, window)


if __name__ == '__main__':
    main()
