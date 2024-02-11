from seasons import thing

def main():
    test_thing()

def test_thing():
    assert thing("2022-07-05") == "Five hundred twenty-five thousand, six hundred minutes"


if __name__ == "__main__":
    main()