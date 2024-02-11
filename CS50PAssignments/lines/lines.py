import sys

def main():
    if len(sys.argv) == 2 and sys.argv[1].endswith(".py"):
        lines = countLines(sys.argv[1])
        print(lines)

    else:
        sys.exit("Invalid prompt")

def countLines(fileName):
    counter = 0
    with open(fileName, "r") as file:
        lines = file.readlines()

    for line in lines:
        if "#" in line:
            line1 = line.lstrip()
            if line1[0] != "#":
                counter += 1
        else:
            if line != "\n":
                counter += 1
    return counter

'''
lol
'''

main()