import sys
from PIL import Image, ImageOps
import os

def main():
    #two arguments
    #if in triple category
    #if theyre the same

    try:
        if len(sys.argv) != 3:
            sys.exit("Invalid arguments")

        name1, extension1 = os.path.splitext(sys.argv[1])
        name2, extension2 = os.path.splitext(sys.argv[2])

        fileTypes = [".png", ".jpeg", ".jpg"]
        if extension1 not in fileTypes and extension2 not in fileTypes:
            sys.exit("Invalid file type.")
        elif extension1 != extension2:
            sys.exit("Different file extensions.")
        else:
            makeImage(sys.argv[1], sys.argv[2])
    except FileNotFoundError:
        sys.exit("File not found.")

def makeImage(first, second):
    try:
        before = Image.open(first)
        shirt = Image.open("shirt.png")
    except FileNotFoundError:
        sys.exit("File not found.")

    size = shirt.size
    before = ImageOps.fit(before, size)
    before.paste(shirt, mask=shirt)
    print("saving")
    before.save(second)



main()