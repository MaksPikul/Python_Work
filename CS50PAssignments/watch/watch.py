import re

def main():
    print(parse(input("HTML: ")))


def parse(s):


    url = re.search(r'<iframe.*src="([^"]*)".*></iframe>', s)
    if url:
        code = re.search(r'.*youtube.*/(.*)', url.group(1))
        if code:
            return "https://youtu.be/" + code.group(1)
        else:
            return None
    else:
        return None












if __name__ == "__main__":
    main()