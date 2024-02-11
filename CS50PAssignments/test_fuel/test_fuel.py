import fuel
import pytest

def main():
    print(fuel.convert("c/t"))
    testcon()
    testgauge()




def testcon():
    assert fuel.convert("2/3") == 67
    with pytest.raises(ValueError):
        fuel.convert("c/t")
    with pytest.raises(ZeroDivisionError):
        fuel.convert("2/0")


def testgauge():
    assert fuel.gauge(67) == "67%"
    assert fuel.gauge(1) == "E"
    assert fuel.gauge(99) == "F"





if __name__ == "__main__":
    main()