import re



def main():
    print(count(input("Text: ")))


def count(s):
    caseList = re.findall(r'\b(um)\b', s, re.IGNORECASE)
    if caseList:
        counter = len(caseList)
    else:
        counter = 0
    return counter



if __name__ == "__main__":
    main()