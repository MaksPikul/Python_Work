import bank


def main():
    test_bank()

def test_bank():
    assert bank.value("hello") == 0
    assert bank.value("Hell") == 20
    assert bank.value("warf ello") == 100


if __name__ == "__main__":
    main()