def main():
    months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
    ]



    convertedDate = convert(months)

    print(convertedDate)






def convert(months):

    while True:
        inp = input("Date: ").strip()
        try:
            if "/" in inp:
                M1, D1, Y1 = inp.split("/")
                M1 = int(M1)
                if int(D1) <= 31 and M1 <= 12:

                    return stringDate(D1,M1,Y1)
                else:
                    continue
        except ValueError:
            pass


        else:
            try:
                M, DY = inp.split(" ", 1)
                M = M.casefold().capitalize()

                D, Y = DY.split(", ")

                #test if D is int
                if int(D) >= 31:
                    print("wrong")
                    test = "String" - 2

                #allocate month number to month

                if str(M.casefold().capitalize()) in months:
                    index = (months.index(M) + 1)
                    index = int(index)

                return stringDate(D,index,Y)

            except ValueError:
                pass
            except TypeError:
                pass

def stringDate(D,M,Y):
    D = f"{int(D):02}"
    M = f"{int(M):02}"
    Y = f"{int(Y):02}"


    date = Y+"-"+M+"-"+D

    return date



main()