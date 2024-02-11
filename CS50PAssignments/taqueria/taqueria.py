def main():
    items = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
    }

    total = 0
    while True:
        try:
            inp = input("Item: ").casefold().title()

            if inp in items:
                total += items[inp]
                print("Total: $" + str(format(total, '.2f')))
            else:
                pass
        except EOFError:
            break

main()