def main():
    dic = dict()
    lis = list()
    while True:
        try:
            inp = input().upper()
            if inp in dic:
                dic[inp] += 1
            else:
                dic[inp] = 1
        except EOFError:


            for item in dic:
                lis.append((str(dic[item]) + " " + item))

            sortedL = sorted(lis)

            for i in sortedL:
                print(i)
            break

main()