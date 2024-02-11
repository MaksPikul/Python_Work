from tabulate import tabulate
import re


class Project:
    def __init__(self):
        self.exercises = list()
        menu = list()

        menu.append(["New exercise", "N"])
        menu.append(["Update exercise", "U"])
        menu.append(["Delete exercise", "D"])
        menu.append(["View file", "V"])
        menu.append(["Save and Exit", "S"])
        self.menu = tabulate(menu[0:], tablefmt="grid")

    def action(self, choice):
        loop = True
        if choice in ["N", "U", "D", "V", "S"]:
            match choice:
                case "N":
                    self.addExercise(self.exercises, 1)
                case "U":
                    self.updateExercise(self.exercises)
                case "D":
                    self.deleteExercise(self.exercises)
                case "V":
                    self.printExercises(self.exercises)
                case "S":
                    saveFile(self.exercises)
                    loop = False
        else:
            print("wrong input")
        return loop

    def addExercise(self, exercises, type):
        if type == 1:
            while True:
                plan = re.search(
                    r"^(.*\-([0-9]|[0-9][0-9]|[0-9][0-9][0-9])\-([0-9]|[0-3][0-9])\-([0-9]|[0-3][0-9]))$", input("Enter without units (Name-weight(999 max)-reps(39 max)-sets(39 max)")
                )
                if plan:
                    plan = plan.group(1)
                    exe, weight, reps, sets = plan.split("-")
                    exercises.append(
                        exe
                        + ": "
                        + reps
                        + " reps of "
                        + weight
                        + "kg, for "
                        + sets
                        + " sets\n\n"
                    )
                    self.printMenu()
                    break
                else:
                    print("Wrong input")
        else:
            while True:
                plan = re.search(
                    r"^(.*\-([0-9]|[0-9][0-9]|[0-9][0-9][0-9])\-([0-9]|[0-3][0-9])\-([0-9]|[0-3][0-9]))$", input("Enter without units (Name-weight(999 max)-reps(39 max)-sets(39 max)"))
                if plan:
                    print(type)
                    plan = plan.group(1)
                    exe, weight, reps, sets = plan.split("-")
                    exercises[type] = (
                        exe
                        + ": "
                        + reps
                        + " reps of "
                        + weight
                        + "kg, for "
                        + sets
                        + " sets\n\n"
                    )
                    break
        print("added")



    def printExercises(self, exercises):
        if len(exercises) != 0:
            print("\nExercises numbered 1 - " + str(len(exercises)) + "\n")
            for exercise in exercises:
                print(exercise)
        else:
            print("\nlist is empty\n")

    def deleteExercise(self, exercises):
        self.printExercises(exercises)
        while True:
            try:
                choice = int(input("Type in exercise number (press 0 to exit): "))
                if 1 <= choice <= len(exercises):
                    exercises.remove(exercises[choice - 1])
                    break
                elif choice == 0:
                    break
                else:
                    print("Exercise number is invalid or list is empty")
            except ValueError:
                print("Input is invalid (not an integer)")
        printMenu(self)

    def updateExercise(self, exercises):
        self.printExercises(exercises)
        while True:
            try:
                choice = int(input("Type in exercise number (press 0 to exit): "))
                if 1 <= choice <= len(exercises):
                    self.addExercise(self.exercises, choice - 1)
                    break
                elif choice == 0:
                    break
                else:
                    print("Exercise number is invalid or list is empty")
            except ValueError:
                print("Input is invalid (not an integer)")
        print("Exercise changed to: ")
        self.printExercises(exercises)
        printMenu(self)

    @property
    def exercises(self):
        return self._exercises

    @exercises.setter
    def exercises(self, exercises):
        self._exercises = exercises


def printMenu(p):
        print(p.menu)

def saveFile(exercises):
        fileName = input("Enter a file name to save Plan (will be saved in a .txt file)")

        with open(fileName + ".txt", "w") as file:
            for exercise in exercises:
                file.write(exercise + "\n")
        print("Plan file saved as " + fileName + ".txt" )
        file.close()

def start(p):
    printMenu(p)
    loop = True
    while loop:
        choice = input("Choose action from above: ").strip().capitalize()
        loop = p.action(choice)

def main():
    p = Project()
    start(p)

if __name__ == "__main__":
    main()