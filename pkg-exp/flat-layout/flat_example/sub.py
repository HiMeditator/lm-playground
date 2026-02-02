import plotext as plt

def plot_example():
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.show()

def plot_seq(seq: list):
    plt.plot(list(range(len(seq))), seq)
    plt.show()
