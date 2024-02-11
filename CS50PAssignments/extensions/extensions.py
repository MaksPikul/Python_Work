def main():

    inp = input("File name: ").casefold().strip()

    if ".jpeg" in inp or ".jpg" in inp:
        print("image/jpeg")

    elif ".pdf" in inp:
        print("application/pdf")

    elif ".gif" in inp:
        print("image/gif")

    elif ".png" in inp:
        print("image/png")

    elif ".txt" in inp:
        print("text/plain")

    elif ".zip" in inp:
        print("application/zip")

    else:
        print("application/octet-stream")

main()

#could have used match