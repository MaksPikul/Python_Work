from datetime import date
import inflect
import sys

def main():
    inp = input("Date: ")
    print(thing(inp))


    #split input
    #asign into method,
    #multiply days to minutes
    #change to words
    #print

def thing(inp):
    p = inflect.engine()

    try:
        year, month, day = inp.split("-")

        date1 = date(int(year), int(month), int(day))
        delta = date.today() - date1
        minutes = delta.days * 24 * 60
        string = p.number_to_words(minutes, andword="")
        return string.capitalize() + " minutes"
    except ValueError:
        sys.exit("Invalid Input")

if __name__ == "__main__":
    main()