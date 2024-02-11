def main():
    word = input("give word: ")
    word = shorten(word)
    print(word)

def shorten(word):
    vowels = {"a", "e", "i", "o", "u"}
    vowelC ={"A", "E", "I", "O", "U"}
    returnWord = ""

    for letter in word:
        if letter not in vowels and letter not in vowelC:
            returnWord += letter
    return returnWord


if __name__ == "__main__":
    main()