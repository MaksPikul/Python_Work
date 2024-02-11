from twttr import shorten

def main():
    test_shorten()

def test_shorten():
    assert shorten("twitter") == "twttr"
    assert shorten("TwItter") == "Twttr"
    assert shorten("Tw1tt4r") == "Tw1tt4r"
    assert shorten("Twitter.") == "Twttr."

if __name__ == "__main__":
    main()