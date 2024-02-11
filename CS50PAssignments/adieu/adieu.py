import inflect

p = inflect.engine()

def main():
    names = list()
    while True:
        try:
            inp = input("")
            names.append(inp)
        except EOFError:
            joinAndPrint(names)
            break



def joinAndPrint(names):
    combined = p.join(names)
    print("Adieu, adieu, to " + combined)


main()