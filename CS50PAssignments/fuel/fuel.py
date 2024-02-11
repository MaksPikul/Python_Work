def main():

    while True:
        try:
            inp = input("Fraction: ")
            a, b = inp.split('/')
            a = int(a)
            b = int(b)
            percent = (a / b) * 100

            if 100 < percent:
                continue
            elif 1 >= percent:
                print("E")
                break
            elif 99 <= percent:
                print("F")
                break
            else:
                print(str(round(percent)) + "%")
                break
        except (ValueError, ZeroDivisionError):
            pass
main()
