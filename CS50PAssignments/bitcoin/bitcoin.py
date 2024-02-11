import requests
import sys
import json

def main():
    try:
        if len(sys.argv) != 2:
            sys.exit("missing arguments")
        else:

            coins = float(sys.argv[1])
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
        rate = response["bpi"]["USD"]["rate"]
        rate = rate.replace(",", "")
        rate = float(rate)
        value = rate * coins
        print(f"${value:,.4f}")

    except ValueError:
        sys.exit("Input is not a number")


main()