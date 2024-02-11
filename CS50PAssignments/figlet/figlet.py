from pyfiglet import Figlet
import random
import sys

figlet = Figlet()

def main():
    if len(sys.argv) == 3:
        if sys.argv[1] == "-f" or sys.argv[1] == "--font":
            printFont(sys.argv[1], sys.argv[2])
        else:
            sys.exit("Invalid usage")
    elif len(sys.argv) == 1:
        printFont("none", "")
    else:
        sys.exit("Invalid usage")

def printFont(first, second):

    fontlist = figlet.getFonts()
    if first == "none":
        inp = input("Input: ")
        size = len(fontlist)
        fonter = fontlist[random.randint(0, size)]
        figlet.setFont(font=fonter)
        print(figlet.renderText(inp))
    elif second in fontlist:
        inp = input("Input: ")
        fonter = second
        figlet.setFont(font=fonter)
        print(figlet.renderText(inp))
    else:
        sys.exit("Invalid usage")


main()