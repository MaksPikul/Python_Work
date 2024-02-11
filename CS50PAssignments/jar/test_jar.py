from jar import Jar

def main():
    test_str()
    test_deposit()
    test_withdraw()
    test_all()

def test_all():
    jar = Jar()
    jar.deposit(2)
    jar.withdraw(1)
    assert str(jar) == "🍪"

def test_str():
    jar = Jar()

    jar.deposit(2)
    assert str(jar) == "🍪🍪"

def test_deposit():
    jar1 = Jar()

    jar1.deposit(1)
    assert str(jar1) == "🍪"

def test_withdraw():
    jar2 = Jar()
    jar2.deposit(10)
    jar2.withdraw(7)
    assert str(jar2) == "🍪🍪🍪"



if __name__ == "__main__":
    main()