def main():

#casefold makes it case-insensitive
    inp = input("What is the Answer to the Great Question of Life, the Universe, and Everything?").casefold()

    if inp == "42" or inp == "forty-two" or inp == "forty two":
        print("Yes")
    else:
        print("No")


main()