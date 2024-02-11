def main():

    word = input("camel case: ")
    finalWord = ""

#for each letter in the word, casefold added to return word, capital adds _ followed by casefolded capital
#this continues for the rest of the word
    for letter in word:
        if letter.isupper():
            finalWord += "_" + letter.casefold()

        else:
            finalWord += letter

    print("snake case: " + finalWord)

main()