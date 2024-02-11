def main():

    #input
    inp = input()

    #method which does replacing
    returned = replaced(inp)

    print(returned)

def replaced(inp):

    #does replacing
    inp = inp.replace(":)", "🙂")
    inp = inp.replace(":(", "🙁")

    #returns new string
    return inp

main()