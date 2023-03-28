import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num", type=int)
    args = parser.parse_args()

    if args.num > 0:
        oddlist = []
        for i in range(args.num):
            if (i % 2) == 1:
                oddlist.append(i)
    else:
        print("The number has to be positive")
    print("odds numbers: ", oddlist)


if __name__ == "__main__":
    main()
