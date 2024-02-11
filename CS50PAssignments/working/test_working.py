from working import convert
import pytest

def main():
    test_convert()
    test_other()

def test_convert():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("9:30 AM to 5:30 PM") == "09:30 to 17:30"

def test_other():
    with pytest.raises(ValueError):
        convert("9 AM 10 PM")
    with pytest.raises(ValueError):
        convert("24 AM to 24 PM")



if __name__ == "__main__":
    main()