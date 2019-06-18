import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)

    #solution
    regex = re.compile("(^[a-zA-Z]+)|([0-9]+$)")
    output_file = open("task_1_7_result.txt", "w+")

    with open(args.file, "r") as file:
        for line in file:
            matches = regex.finditer(line)
            if matches:
                for match in matches:
                    output_file.write(match.group() + "\n")