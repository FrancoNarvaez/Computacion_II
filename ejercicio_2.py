import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="write the text you want to repeat", type=str)
    parser.add_argument("num", help="number of times you want to repeat the text", type=int)
    arguments = parser.parse_args()
    print((arguments.text + " ")*arguments.num)


if __name__ == "__main__":
    main()