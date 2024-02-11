def  main():
    inp = input("Expression: ").strip()

    x, y, z = inp.split(" ")

    x = float(x)
    z = float(z)

    match y:
        case "+":
            print(x + z)
        case "-":
            print(x - z)
        case "*":
            print(x * z)
        case "/":
            print(x / z)
        

main()