import sys
from .sub import process


def process_main():
    t = 0
    try:
        t = int(sys.argv[1])    
    except ValueError:
        print("Usage: src_process <t>\n t must be an integer")
        return
    process(t)


def main():
    print("Src layout example main")


if __name__ == "__main__":
    main()
