import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="indicate the file to count the number of words and lines", type=str)
    parser.add_argument("-a", "--average", help="print the average length of words in the file", action="store_true")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as file:
            lines = file.readlines()
            words = 0
            total_word_length = 0
            for line in lines:
                words_in_line = line.split()
                words += len(words_in_line)
                if args.average:
                    total_word_length += sum(len(word) for word in words_in_line)
            print("The file has {} lines and {} words".format(len(lines), words))
            if args.average:
                average_word_length = total_word_length / words
                print("The average length of words in the file is {:.2f}".format(average_word_length))
    except FileNotFoundError:
        with open("errors.log", "a") as error_file:
            error_file.write("The file {} does not exist\n".format(args.file))
        sys.stderr.write("The file {} does not exist\n".format(args.file))
        sys.exit(1)


if __name__ == "__main__":
    main()