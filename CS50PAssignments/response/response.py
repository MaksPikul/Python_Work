import validators

def main():

    if validators.email(input("Email: ")):
        print("Valid")
    else:
        print("Invalid")

if __name__ == "__main__":
    main()