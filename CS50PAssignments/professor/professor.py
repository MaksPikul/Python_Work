import random


def main():
    counter = 0
    attempts = 2
    score = 0
    level = get_level()

    while counter < 10:
        # collect random ints, form into function, use if  statement to check and give point,
        # after each correct you up the counter at the end a score given
        num1 = generate_integer(level)
        num2 = generate_integer(level)
        correctAns = num1 + num2
        while True:
            try:
                answer = int(input(str(num1) + " + " + str(num2) + " = "))
                if answer == correctAns:
                    score += 1
                    break
                elif attempts == 0:
                    print("EEE")
                    print(str(num1) + " + " + str(num2) + " = " + str(correctAns))
                    attempts = 3
                    break
                else:
                    print("EEE")
                    attempts -= 1
            except ValueError:
                pass
        counter += 1
    print("Score: " + str(score))



def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if 0 < level < 4:
                return level
            else:
                pass
        except ValueError:
            pass


def generate_integer(level):
    zero = 1
    if level == 1:
        zero = 0
    bottom = (10**(level-1))*zero
    top = (10**level)-1
    return random.randint(bottom, top)


if __name__ == "__main__":
    main()