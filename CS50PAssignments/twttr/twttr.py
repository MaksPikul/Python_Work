def main():

    word = input("give word: ")
    vowels = {"a", "e", "i", "o", "u"}
    vowelC ={"A", "E", "I", "O", "U"}
    returnWord = ""

    for letter in word:
        if letter not in vowels and letter not in vowelC:
            returnWord += letter
    print(returnWord)

main()

