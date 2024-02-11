- Function I have created for the class (explanation of how they work in code file through comments):
  - Count() - Counts the number of a certain string saved in tree
  - Max() - Finds the largest string in alphabetical order
  - Pred(String arg) - Finds the largest string which is smaller than a given input String
  - Remove(String arg) - Removes input string from the tree
<br>

From the full testing script, The functions recieved 93.5 out of 100 marks. 
<br>

contains 5 files 
StringTree.py - class file with functions
<br>

Tree.png - Image which shows below names added in order as visual of tree
{TALEN, NAIMA , NAJLA , MOISE, TANHA ,BUFFY , AISA, OBY, NAHIA, AGATA}
<br>

TreeFucntionExplaination.pdf - PDF file which explains how the string tree data structure works
<br>

TestingScriptMac.py & TestingScriptWindows.py - testing scripts for each OS, running the script should output:
Imported and will test
Testing ...
[0]: test [count 00]...............success, awarded: 1
[1]: test [count 01]...............success, awarded: 1
[2]: test [count 10]...............success, awarded: 1
[3]: test [count 11]...............success, awarded: 1
[4]: test [count 30]...............success, awarded: 1
[5]: test [max 01].................success, awarded: 1
[6]: test [max 11].................success, awarded: 1
[7]: test [max 11m]................success, awarded: 1
[8]: test [max 12].................success, awarded: 1
[9]: test [max 12l]................success, awarded: 1
[10]: test [max 30]................success, awarded: 1
[11]: test [max 51]................success, awarded: 1
[12]: test [pred 01]...............partial success [], awarded: 0.6666666666666666 of 2
[13]: test [pred 02]...............partial success [], awarded: 1.3333333333333333 of 2
[14]: test [pred 03]...............success, awarded: 2
[15]: test [pred 2]................partial success [], awarded: 1.6 of 2
[16]: test [pred 5]................success, awarded: 3
[17]: test [remove 00].............success, awarded: 1
[18]: test [remove 01].............success, awarded: 1
[19]: test [remove 02].............success, awarded: 1
[20]: test [remove 03].............success, awarded: 2
[21]: test [remove 04].............success, awarded: 1
[22]: test [remove 30].............success, awarded: 1
<br>

-> count : 5.0 [5]
-> max : 7 [7]
-> pred : 8.6 [11]
-> remove: 7.0 [7]
-> *Total: 27.6 [30]
