import random
import sys

def main():

    while True:
        try:
            level = int(input("level: "))
            if level > 0:
                break
            else:
                pass
        except ValueError:
            pass

    chosen = random.randint(1,int(level))

    while True:
        try:
            guess = int(input("Guess: "))
            if guess > 0:
                if guess == chosen:
                    print("Just right!")
                    sys.exit()
                elif guess < chosen:
                    print("Too small!")

                elif guess > chosen:
                    print("Too large!")
            else:
                pass
        except ValueError:
            pass


main()