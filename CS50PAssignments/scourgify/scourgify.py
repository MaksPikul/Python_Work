import sys
import csv

def main():

        if len(sys.argv) == 3:
            change(sys.argv[1], sys.argv[2])

        else:
            sys.exit("Invalid Prompt")


def change(before, after):

    data = []
    with open(before, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            house = row["house"]
            last, first = row["name"].split(",")

            data.append([first, last, house])

    with open(after, "w") as file:
        writer = csv.DictWriter(file, fieldnames =["first", "last", "house"])
        size = len(data)
        counter = 0
        writer.writeheader()
        while counter < size:
             writer.writerow({"first" : data[counter][0].strip(), "last": data[counter][1].strip(), "house": data[counter][2].strip()})
             counter += 1


main()
