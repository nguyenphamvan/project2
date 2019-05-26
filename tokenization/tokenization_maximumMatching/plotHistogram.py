import matplotlib.pyplot as plt
import numpy as np

def PlotHistogram(dict):
    f = open(dict, 'r', encoding="utf8")
    label = []
    countWord = []
    for x in range(40):
        (word, count) = next(f).split(" : ")
        label.append(word)
        countWord.append(int(count))

    index = np.arange(len(label))

    plt.bar(index, countWord)
    plt.ylabel("Cumulative Counts")
    plt.xticks(index, label, rotation= 90, fontsize=8)
    plt.show()
