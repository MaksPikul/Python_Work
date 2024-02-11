   # Project Title - Gym Planner
    #### Video Demo:  https://www.youtube.com/watch?v=pjAzoGw4RJw
    #### Description: I made a gym planner which can; add exercises, update exercises, delete exercises view saved exercises and save exercises to a txt file. I used an object-oriented approach to code the functions of my application since i have small java background and is easier to navigate, a main is called which creates a project object and calls the object start function. In my project i wanted to use what ive learnt to create something, hence why i used regular expressions, file I/O, libraries, exceptions and made unit tests since theyre relatively new to me in terms of pythonic programming. I think i made good use of the content offered by cs50, however if i were to program something similar again, i would use a saving and retrieving data method for exercise plans and use a library such as  pyqt5 to create an app instead of using terminal (pyqt5 didnt work when i installed it), also adding options to exit choice.

    #### I believe my program is user friendly, appart from update and delete which might confuse some, exercises arent numbered, to choose you would have to count the exercise placement (1 to exercise amount). once you choose an option you have to do option

    #### When program opens, you are given a menu to chose 5 options, add exercises, update, delete, view and save + exit, each time a wrong input is given, user is reprompted

    #### when add exercise is chosen, you enter exercise details as requested, name-weight-reps-sets. program uses regualr expresions to check input, i used regex and not if statements because i wanted to use what ive learnt in the course, checking if a match is made is easier compared to if statements or exemption handeling. adding an exercise adds it to the object exercises list variable which can be later used to print it out or delete/update it.

    #### updating and deleting exercises work similarly, prints out list of saved exercises, and allows you to choose either 0 or a number corresponding to exercises, choosing an exercises will either delete it and notify user or allow for adding a new exercise.

    #### viewing exercise method is simple, simply uses for loop to print out the exercise list, put it into method to simply call method where ever.

    ####saving file method which is outside of class creates a new file or uses existing to write the exercise list onto the txt file.

    #### I used tabulate and re libraries.