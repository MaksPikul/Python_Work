from tabulate import tabulate
import sys
import csv


def main():
    if len(sys.argv) == 2 and sys.argv[1].endswith(".csv"):
        table(sys.argv[1])
    else:
        sys.exit("Invalid Prompt")

def table(fileName):

    data = []
    with open(fileName, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([row[0], row[1], row[2]])



    file.close()
    print(tabulate(data[1:], data[0], tablefmt="grid"))

main()