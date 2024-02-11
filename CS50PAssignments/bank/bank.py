def main():
    inp = input("Greeting: ").casefold().strip()

    if inp[0:5] == "hello":
        print("$0")
    elif inp[0] == "h":
        print("$20")
    else:
        print("$100")

main()