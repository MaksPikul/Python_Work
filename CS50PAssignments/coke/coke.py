def main():

    sum = 0
    end = True

    while end:
        coin = int(input("Enter a coin (5 / 10 / 25): "))

        if coin == 10 or coin == 25 or coin == 5:
            sum = sum + coin

        if sum < 50:
            print("Amount Due: " + str(50-sum))
        else:
            print("Change Owed: " + str((sum-50)))
            end = False

main()