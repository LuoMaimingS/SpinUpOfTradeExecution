import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_bars():
    labels = ['8min5K', '2min5K', '8min10K', '2min10K']
    bar1 = [14.13, 15.04, 14.66, 15.76]
    bar2 = [4.61, 7.08, 6.44, 7.44]
    bar3 = [7.76, 8.44, 8.4, 8.8]
    bar4 = [7.72, 8.48, 8.37, 8.84]

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 2 * width, bar1, width, label='S&L', color='#f8cb7f')
    rects2 = ax.bar(x - width, bar2, width, label='SAC', color='#76da91')
    rects3 = ax.bar(x, bar3, width, label='DDPG', color='#63b2ee')
    rects4 = ax.bar(x + width, bar4, width, label='TD3', color='#7cd6cf')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Trading Cost')
    ax.set_title('000012(T = 4)')
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
    autolabel(rects4)

    fig.tight_layout()

    plt.show()


def plot_trends():
    with open('sac.txt', 'r') as f:
        lines = f.readlines()[1:]
        loss_q = []
        loss_pi = []
        for line in lines:
            loss_q.append(eval(line.split()[-2]))
            loss_pi.append(eval(line.split()[-3]))
        print(loss_q)
        x = np.arange(len(loss_q))
        print(x)
        plt.plot(x, loss_q)

        plt.show()

        plt.plot(x, loss_pi)

        plt.show()


if __name__ == '__main__':
    plot_bars()
