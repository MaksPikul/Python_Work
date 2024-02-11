def main():
    while True:
        try:
            inp = input("Fraction: ")
            a, b = inp.split('/')
            a = int(a)
            b = int(b)
            if a/b > 1:
                continue
            else:
                break
        except(ValueError, ZeroDivisionError):
            pass
    value = convert(inp)
    print(gauge(value))


def convert(fraction):
    try:
        a, b = fraction.split('/')
        a = int(a)
        b = int(b)
    except ValueError:
        raise ValueError

    return round((a / b) * 100)




def gauge(percentage):
            if 1 >= percentage:
                return("E")
            elif 99 <= percentage:
                return("F")
            else:
                return(str(round(percentage)) + "%")



if __name__ == "__main__":
    main()