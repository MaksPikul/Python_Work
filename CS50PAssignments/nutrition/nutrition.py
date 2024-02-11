def main():

    fruits = {
        "apple" : "130",
        "avocado" : "50",
        "kiwifruit" : "90",
        "pear" : "100",
        "sweet cherries" : "100"
    }

    inp = input("Fruit: ").casefold().strip()

    for fruit in fruits:
        if fruit == inp:
            print("Calories: " + fruits[fruit])


main()