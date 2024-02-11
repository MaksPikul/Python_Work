from project import Project

def main():
    test_choice()

#only function that has a return value
def test_action():
    p = Project()
    assert p.action("S") == False


if __name__ == "__main__":
    main()