import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['8min5K', '2min5K', '8min10K', '2min10K']
bar1 = [17.5, 25, 35, 50]
bar2 = [25, 32, 34, 30]
bar3 = [25, 32, 34, 30]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - 3 * width/2, bar1, width, label='S&L', color='black')
rects2 = ax.bar(x - width/2, bar2, width, label='T=4 I=4', color='grey')
rects3 = ax.bar(x + width/2, bar3, width, label='T=8 I=8', color='lightgrey')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Trading Cost')
ax.set_title('000009')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.show()