import plates

def main():
    test()

def test():
    assert plates.is_valid("50113") == False
    assert plates.is_valid("abcdefg") == False
    assert plates.is_valid("aa50aa") == False
    assert plates.is_valid("CS05") == False
    assert plates.is_valid("Cs,50") == False

if __name__ == "__main__":
    main()