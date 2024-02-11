from numb3rs import validate

def main():
    test_validate()


def test_validate():
    assert validate("123.256.256.256") == False
    assert validate("123.123.123.123.123") == False
    assert validate("cat") == False