def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


#could have made functions for different checks

def is_valid(s):

#comparision variables being set

    size = len(s)
    if size>1:
        first2 = s[:2]
        third = s[2]
        last = s[2:size]
        punc = [",", ".", " "]
        notInPunc = False
        first3 = False
        returnV = True
        nolonger = False
    else:
        return False

#checks for punctuation
    for letter in s:
        if letter not in punc:
            notInPunc = True
#check for word size, if word starts with 0 and if there are ints in first 2 varaibles
    if 2<= size <=6 and third != "0" and first2.isalpha():
        first3 = True
#if there is a digit, the next string will flag the word as invlaid
    for i in last:
        if i.isdigit():
            nolonger = True
        elif isinstance(i,str) and nolonger:
            returnV = False

#checks if all criteria is met and returns coresponding value
    if notInPunc and first3 and returnV:
        return True
    else:
        return False


main()