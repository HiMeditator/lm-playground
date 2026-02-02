import sys
from .sub import plot_seq


def plot_main():
    lst = []
    try:
        for val in sys.argv[1:]:
            lst.append(int(val))
    except ValueError:
        print("All arguments must be integers")
    plot_seq(lst)


def main():
    print("Flat layout example main")


if __name__ == "__main__":
    main()
