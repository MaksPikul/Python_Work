## Testing script ##
####################

## in case python package import-ipynb is not installed, comment out next line
## BUT then the solution needs to be in file stringtree.py in plain text
import import_ipynb

import os,import_ipynb,importlib,signal

######################################################################
# initialisations 
######################################################################

sid = 123456789             # your student ID here!
module = "stringtree.ipynb" # you solutions file here!

# penalty 10% if count/max/succ/pred changes the tree
ifChanged = 0.9 
changeError = "tree changed "

# remove function needs to preserve the size, string rep, and structure
sizeMark = 0.05
printMark = 0.65
structMark = 0.3
sizeError = "size mismatch; "
printError = "print mismatch; "
structError = "tree structure error "

exceptionError = " E: "
sanityChecking = True

def justError(i):
    return str(i)+"! "
res = ""
nameST = "test"

######################################################################
# code for handling timeouts (for infinite loops)
# main function for running a list of tests
# helper function for converting test results into string
######################################################################
    
def timeoutHandler(s,f):
    raise Exception("timeout")

signal.signal(signal.SIGALRM, timeoutHandler)
timeout = 2

def tryWithTimeout(thunk):
    (res,error) = (None,"")
    signal.alarm(timeout)
    try: res = thunk()
    except BaseException as e: error = exceptionError + str(e)
    signal.alarm(0)
    return (res,error)

def runTests(tests):
    awarded, total, res = 0, 0, ""
    for (UID,test) in tests:
        (name,mark,msg,grade) = test() # grade: max; mark: awarded
        s = "["+str(UID)+"]: "+name
        dots = ''.join(map(str, ['.' for i in range(35-len(s))]))
        res += s+dots
        awarded += grade*mark
        if round(mark,2) == 0:
            res += "error ["+msg+"], awarded: 0 of "+str(grade)
        elif round(mark,2) == 1: 
            res += "success, awarded: "+str(grade)
        else:
            res += "partial success ["+msg+"], awarded: "+str(mark*grade)+" of "+str(grade)
        res += "\n"
        total += grade
    (awarded, total) = (round(awarded,2), round(total,2))
    # res += "\nTotal testing marks [57]: "+str(awarded)
    return (awarded,total,res)

######################################################################
# Tree comparison
######################################################################
def equalSTrees(t1,t2):
    def equalTrees(t1,t2,par1,par2,m2): # here t1,t2 are STNodes, and par1,par2 their parents
        if t1==t2==None: return True
        if t1==None or t2==None: return False
        if t1.parent != par1 or t2.parent != par2: return False
        if t1.mult != t2.mult: return False
        x = t1.mult==0 or (t1.dlistPtr,t2.dlistPtr) in m2  
        return x and t1.data==t2.data and equalTrees(t1.left,t2.left,t1,t2,m2) and equalTrees(t1.mid,t2.mid,t1,t2,m2) and equalTrees(t1.right,t2.right,t1,t2,m2)
    
    def equalLists(l1,l2,memo):
        def equalLR(t1,t2,memo): # here t1,t2 are DNodes
            if t1==t2==None: return True
            if t1==None or t2==None: return False        
            x = t1.data==t2.data and equalLR(t1.next,t2.next,memo) 
            if not x: return False
            memo.add((t1,t2))
            return True
        
        if not equalLR(l1.head,l2.head,memo): return False
        ptr1, ptr2 = l1.tail, l2.tail
        while ptr1 != None:
            if (ptr1,ptr2) not in memo: return False
            ptr1, ptr2 = ptr1.prev, ptr2.prev
        return True

    flag = 1 # 1: equal, -1: unequal lists, -2: unequal trees 
    memo = set([(None,None)])
    if not equalLists(t1.dlist,t2.dlist,memo): flag = -1
    elif not equalTrees(t1.root,t2.root,None,None,memo): flag = -2
    return flag

def checkChange(tree,clone):
    (same, error) = tryWithTimeout(lambda : equalSTrees(tree,clone))
    if same == 1: return ""
    if same == -1: return changeError+"(dlist); "
    if same == -2: return changeError+"(stree); "
    return structError+error

######################################################################
# Parsing and sanity checks
######################################################################

def getStrs(node, sndict, strings):
    if node == None: return
    getStrs(node.left,sndict,strings)
    if node.mult > 0: 
        strings.append(node.strFromTop())
        sndict[node.strFromTop()] = node
    getStrs(node.mid,sndict,strings)
    getStrs(node.right,sndict,strings)

def parseST(st):
    if st == "empty": return StringTree()
    A = st.replace(" -> ","-").replace("[",",").replace("]","").replace("(","").replace(")","").replace(" ","").replace(",,",",").split(",")
    t = StringTree()
    (t.root,t.size,A) = parseSTSubtree(A,0)

    # add words to the dlist
    sndict = {}
    strings = []
    getStrs(t.root,sndict,strings)
    for s in sorted(strings): 
        t.dlist.append(s)
        sndict.get(s).dlistPtr = t.dlist.tail
    return t

def parseSTSubtree(A,size):
    if A[0] == "□": return (None,size,A[1:])
    ptr = STNode(A[0])
    if A[1][-1] == "-":
        ptr.mult = int(A[1][:-1])
        (ptr.left,size,A) = parseSTSubtree(A[2:],size)
        if ptr.left: ptr.left.parent = ptr
        (ptr.mid,size,A) = parseSTSubtree(A,size)
        if ptr.mid: ptr.mid.parent = ptr
        (ptr.right,size,A) = parseSTSubtree(A,size)
        if ptr.right: ptr.right.parent = ptr
    else:
        ptr.mult = int(A[1])
        return (ptr, size+ptr.mult, A[2:])
    return (ptr,size+ptr.mult,A)

def sanity(words,model,testname):
    t = StringTree()
    for w in words: t.add(w)
    if str(t) != model: print("something is wrong! "+testname)
        
def sanity2(words,tree,testname):
    t = StringTree()
    for w in words: t.add(w)
    f = equalSTrees(t,tree)
    if f==-1: print("something is wrong (list)!! "+testname)
    elif f==-2: print("something is wrong (tree)!! "+testname)

# what: short description of the test (what function does it test)
# nm: number of cases (sub-tests)
# words: the words in the input tree
# model: a string description of the input tree
# grade: max total marks for test
# helperFun: function that runs the actual test
# helperArgs: arguments to be used with helperFun

def mainTest(what,nm,words,model,grade,helperFun,helperArgs):
    testName = nameST+" ["+what+" "+nm+"]"
    if sanityChecking: sanity(words,model,testName)
    tree = parseST(model)
    clone = parseST(model)
    if sanityChecking: sanity2(words,tree,testName)
    (mark,msg) = helperFun(tree,clone,helperArgs)        
    return (testName,mark,msg,grade)

###################################
# tests for count (mark out of 15)
###################################

def countTestST(nm,words,model,cases,sols,grade):
    if len(cases)!=len(sols): print("test size mismatch! "+nm)
    return mainTest("count",nm,words,model,grade,countTestSTHelper,(cases,sols))

# returns a mark as % of total marks, and a message
def countTestSTHelper(tree,clone,args):
    cases, sols = args
    (mark,msg) = (0,"")
    minimark = 1/len(sols)
    for i in range(len(cases)):
        (toCount,sol) = (cases[i],sols[i])
        (counted,error) = tryWithTimeout(lambda : tree.count(toCount))
        if error != "": msg += error
        elif counted != sol: msg += justError(i)
        else: # check if there was change
            changed = checkChange(tree,clone)
            if changed != "": mark += minimark*ifChanged
            else: mark += minimark
            msg += changed
    return (mark,msg)

def testST_C_00(): # counting on empty tree [sample]
    tenNotIn = ["sake", "umith", "daltha", "jy", "spith"]
    words = []
    model = "empty"
    sol = [0 for i in range(5)]
    return countTestST("00",words,model,tenNotIn,sol,1)

def testST_C_01(): # count element of singleton tree [sample]
    oneIn = ["a"]
    words = ["a"]
    model = "(a, 1)"
    sol = [1]
    return countTestST("01",words,model,oneIn,sol,1)

def testST_C_10(): # count strings doubly in tree of size 30 [sample]
    cases = ["hit", "zath", "dunt", "cofsod", "olne", "sargu", "tam", "wesk", "cats", "gos"]
    words = words30
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 2), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 2), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 2), □], (u, 0) -> [□, (n, 0) -> [□, (t, 2), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 2), □], □]], (i, 0) -> [□, (t, 2), □], □], (e, 0) -> [□, (n, 2), (o, 0) -> [□, (f, 2), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 2), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 2), □], □], □], (c, 0) -> [□, (a, 2), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 2), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 2), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 2), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 2), □], □], □]]"
    sol = [2 for i in range(10)]
    return countTestST("10",words,model,cases,sol,1)

def testST_C_11(): # count non-elements in 50 random words [sample]
    tenNotIn = ["rot", "cas", "stolb", "ada", "lend", "sake", "umith", "daltha", "jy", "spith"]
    words = words50_1
    model = "(r, 0) -> [(a, 0) -> [□, (r, 1) -> [(i, 0) -> [□, (x, 1), □], (t, 1) -> [(o, 0) -> [□, (b, 1), □], □, □], (s, 0) -> [□, (n, 0) -> [□, (u, 1), (t, 0) -> [□, (l, 0) -> [□, (e, 0) -> [□, (t, 0) -> [□, (w, 0) -> [□, (o, 1), □], □], □], □], □]], □]], (h, 0) -> [(c, 0) -> [(b, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (r, 1) -> [(c, 0) -> [□, (k, 1), □], □, □], □], (b, 0) -> [□, (d, 1), (f, 1)], □], □], (u, 0) -> [(a, 0) -> [□, (s, 0) -> [□, (t, 1), □], (h, 0) -> [□, (o, 1), □]], (s, 0) -> [□, (r, 0) -> [□, (e, 1), □], □], □], (g, 0) -> [(d, 0) -> [□, (r, 0) -> [(e, 0) -> [□, (n, 0) -> [□, (t, 1), □], (i, 0) -> [□, (s, 0) -> [□, (p, 0) -> [□, (a, 1), □], □], □]], (o, 0) -> [□, (u, 0) -> [□, (b, 0) -> [□, (i, 0) -> [□, (c, 0) -> [□, (a, 1), □], □], □], □], □], (u, 1) -> [□, □, (y, 1)]], (e, 0) -> [□, (d, 0) -> [□, (e, 0) -> [□, (n, 0) -> [□, (t, 1), □], □], (h, 0) -> [□, (i, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (e, 0) -> [□, (m, 1), □], □], □], □], (l, 0) -> [□, (s, 1), □]]], (f, 0) -> [□, (o, 0) -> [□, (c, 0) -> [□, (l, 0) -> [□, (o, 0) -> [□, (t, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (h, 1), □], □], □], □], □], □], □], □]]], (u, 0) -> [(o, 0) -> [□, (d, 1) -> [(c, 0) -> [□, (l, 1), □], □, □], □], (g, 1), □], □]], (a, 0) -> [□, (r, 1), □], (k, 0) -> [(j, 0) -> [□, (a, 0) -> [□, (t, 1), □], □], (n, 0) -> [□, (a, 0) -> [□, (t, 1), □], □], (l, 0) -> [□, (i, 0) -> [□, (r, 0) -> [□, (v, 0) -> [□, (i, 0) -> [□, (n, 0) -> [□, (n, 0) -> [□, (u, 0) -> [□, (n, 1), □], □], □], □], □], □], □], (p, 0) -> [(m, 0) -> [□, (u, 0) -> [□, (t, 0) -> [□, (l, 0) -> [□, (u, 0) -> [□, (n, 0) -> [□, (t, 1), □], □], □], □], □], (o, 0) -> [□, (n, 1), □]], (l, 0) -> [(a, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (a, 1), (t, 1)], □], (e, 0) -> [□, (j, 0) -> [□, (o, 0) -> [□, (r, 1), □], □], (i, 0) -> [□, (m, 1), □]]], (i, 1), (o, 0) -> [□, (n, 0) -> [□, (g, 1), □], (r, 0) -> [□, (a, 0) -> [□, (l, 0) -> [□, (i, 0) -> [□, (v, 0) -> [□, (e, 0) -> [□, (a, 0) -> [□, (r, 1), □], □], □], □], □], □], □]]], □]]]]], (u, 0) -> [(i, 0) -> [(a, 0) -> [□, (s, 0) -> [□, (s, 1) -> [□, □, (u, 0) -> [□, (i, 0) -> [□, (m, 0) -> [□, (u, 1), □], □], □]], (t, 0) -> [□, (c, 0) -> [□, (h, 1), □], □]], (e, 0) -> [□, (g, 1), □]], (p, 0) -> [□, (l, 0) -> [□, (y, 1), □], □], □], (o, 0) -> [□, (t, 0) -> [□, (c, 0) -> [□, (h, 1), □], □], □], □], (t, 0) -> [(s, 0) -> [□, (i, 0) -> [(c, 0) -> [□, (a, 0) -> [□, (n, 0) -> [□, (n, 0) -> [□, (a, 1), □], □], □], (h, 0) -> [□, (i, 0) -> [□, (f, 0) -> [□, (f, 0) -> [□, (o, 1), □], □], □], □]], (m, 0) -> [□, (m, 0) -> [□, (o, 1), □], □], (u, 0) -> [□, (t, 0) -> [□, (u, 0) -> [□, (r, 1), □], □], □]], □], (a, 0) -> [□, (l, 0) -> [□, (c, 0) -> [□, (r, 0) -> [□, (u, 1), □], □], □], (r, 0) -> [□, (a, 0) -> [□, (n, 0) -> [□, (g, 0) -> [□, (r, 0) -> [□, (e, 0) -> [□, (d, 0) -> [□, (l, 0) -> [□, (u, 1), □], □], □], □], □], □], □], □]], □]]"
    sol = [0 for i in range(10)]
    return countTestST("11",words,model,tenNotIn,sol,1)

def testST_C_30(): # similar strings [sample]
    cases = ["hello", "hell"]
    words = ["he", "hello", "hex", "hexagon", "hell", "hell"]
    model = "(h, 0) -> [□, (e, 1) -> [□, (l, 0) -> [□, (l, 2) -> [□, (o, 1), □], (x, 1) -> [□, (a, 0) -> [□, (g, 0) -> [□, (o, 0) -> [□, (n, 1), □], □], □], □]], □], □]"
    sol = [1,2]
    return countTestST("30",words,model,cases,sol,1)

countTestsST = [testST_C_00,testST_C_01,testST_C_10,testST_C_11,testST_C_30]

###########################################################################
# max tests (mark out of 15)
###########################################################################

def maxTestST(nm,words,model,node,sol,grade):
    return mainTest("max",nm,words,model,grade,maxTestSTHelper,(node,sol))

def maxTestSTHelper(tree,clone,args):
    node, sol = args
    if node == 0: node = tree.root.left
    elif node == 1: node = tree.root.right
    elif node == 2: node = tree.root.mid
    else: node = tree.root
    mark, msg = 0, ""
    (ret,error) = tryWithTimeout(lambda : tree._max(node))
    if error != "": msg += error
    elif ret.strFromTop() != sol: msg += justError("wrong max")
    else: # check if there was change
        changed = checkChange(tree,clone)
        if changed != "": mark = ifChanged
        else: mark = 1
        msg += changed    
    return (mark,msg)

def testST_M_01(): # max in 15 strings (root) [sample]
    words = words15_1
    sol = "zath"
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 1), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 1), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 1), □], (u, 0) -> [□, (n, 0) -> [□, (t, 1), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 1), □], □]], (i, 0) -> [□, (t, 1), □], □], (e, 0) -> [□, (n, 1), (o, 0) -> [□, (f, 1), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 1), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 1), □], □], □], (c, 0) -> [□, (a, 1), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 1), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 1), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 1), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 1), □], □], □]]"
    return maxTestST("01", words, model, None, sol, 1)

def testST_M_11(): # max in small tree (root) [sample]
    words = ["a", "aa", "aaa"]
    sol = "aaa"
    model = "(a, 1) -> [□, (a, 1) -> [□, (a, 1), □], □]"
    return maxTestST("11", words, model, None, sol, 1)

def testST_M_11m(): # max in small tree (root.mid) [sample]
    words = ["a", "aa", "aaa"]
    sol = "aaa"
    model = "(a, 1) -> [□, (a, 1) -> [□, (a, 1), □], □]"
    return maxTestST("11m", words, model, 2, sol, 1)

def testST_M_12(): # max in small tree (root) [sample]
    words = ["z", "zz", "b"]
    sol = "zz"
    model = "(z, 1) -> [(b, 1), (z, 1), □]"
    return maxTestST("12", words, model, None, sol, 1)

def testST_M_12l(): # max in small tree (root.left) [sample]
    words = ["z", "zz", "b"]
    sol = "b"
    model = "(z, 1) -> [(b, 1), (z, 1), □]"
    return maxTestST("12l", words, model, 0, sol, 1)

def testST_M_30(): # max in 30 strings (root) [sample]
    words = words30
    sol = "zath"
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 2), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 2), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 2), □], (u, 0) -> [□, (n, 0) -> [□, (t, 2), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 2), □], □]], (i, 0) -> [□, (t, 2), □], □], (e, 0) -> [□, (n, 2), (o, 0) -> [□, (f, 2), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 2), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 2), □], □], □], (c, 0) -> [□, (a, 2), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 2), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 2), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 2), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 2), □], □], □]]"
    return maxTestST("30", words, model, None, sol, 1)

def testST_M_51(): # max in 50 strings (root) [sample]
    words = words50_1
    sol = "trangredlu"
    model = "(r, 0) -> [(a, 0) -> [□, (r, 1) -> [(i, 0) -> [□, (x, 1), □], (t, 1) -> [(o, 0) -> [□, (b, 1), □], □, □], (s, 0) -> [□, (n, 0) -> [□, (u, 1), (t, 0) -> [□, (l, 0) -> [□, (e, 0) -> [□, (t, 0) -> [□, (w, 0) -> [□, (o, 1), □], □], □], □], □]], □]], (h, 0) -> [(c, 0) -> [(b, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (r, 1) -> [(c, 0) -> [□, (k, 1), □], □, □], □], (b, 0) -> [□, (d, 1), (f, 1)], □], □], (u, 0) -> [(a, 0) -> [□, (s, 0) -> [□, (t, 1), □], (h, 0) -> [□, (o, 1), □]], (s, 0) -> [□, (r, 0) -> [□, (e, 1), □], □], □], (g, 0) -> [(d, 0) -> [□, (r, 0) -> [(e, 0) -> [□, (n, 0) -> [□, (t, 1), □], (i, 0) -> [□, (s, 0) -> [□, (p, 0) -> [□, (a, 1), □], □], □]], (o, 0) -> [□, (u, 0) -> [□, (b, 0) -> [□, (i, 0) -> [□, (c, 0) -> [□, (a, 1), □], □], □], □], □], (u, 1) -> [□, □, (y, 1)]], (e, 0) -> [□, (d, 0) -> [□, (e, 0) -> [□, (n, 0) -> [□, (t, 1), □], □], (h, 0) -> [□, (i, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (e, 0) -> [□, (m, 1), □], □], □], □], (l, 0) -> [□, (s, 1), □]]], (f, 0) -> [□, (o, 0) -> [□, (c, 0) -> [□, (l, 0) -> [□, (o, 0) -> [□, (t, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (h, 1), □], □], □], □], □], □], □], □]]], (u, 0) -> [(o, 0) -> [□, (d, 1) -> [(c, 0) -> [□, (l, 1), □], □, □], □], (g, 1), □], □]], (a, 0) -> [□, (r, 1), □], (k, 0) -> [(j, 0) -> [□, (a, 0) -> [□, (t, 1), □], □], (n, 0) -> [□, (a, 0) -> [□, (t, 1), □], □], (l, 0) -> [□, (i, 0) -> [□, (r, 0) -> [□, (v, 0) -> [□, (i, 0) -> [□, (n, 0) -> [□, (n, 0) -> [□, (u, 0) -> [□, (n, 1), □], □], □], □], □], □], □], (p, 0) -> [(m, 0) -> [□, (u, 0) -> [□, (t, 0) -> [□, (l, 0) -> [□, (u, 0) -> [□, (n, 0) -> [□, (t, 1), □], □], □], □], □], (o, 0) -> [□, (n, 1), □]], (l, 0) -> [(a, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (a, 1), (t, 1)], □], (e, 0) -> [□, (j, 0) -> [□, (o, 0) -> [□, (r, 1), □], □], (i, 0) -> [□, (m, 1), □]]], (i, 1), (o, 0) -> [□, (n, 0) -> [□, (g, 1), □], (r, 0) -> [□, (a, 0) -> [□, (l, 0) -> [□, (i, 0) -> [□, (v, 0) -> [□, (e, 0) -> [□, (a, 0) -> [□, (r, 1), □], □], □], □], □], □], □]]], □]]]]], (u, 0) -> [(i, 0) -> [(a, 0) -> [□, (s, 0) -> [□, (s, 1) -> [□, □, (u, 0) -> [□, (i, 0) -> [□, (m, 0) -> [□, (u, 1), □], □], □]], (t, 0) -> [□, (c, 0) -> [□, (h, 1), □], □]], (e, 0) -> [□, (g, 1), □]], (p, 0) -> [□, (l, 0) -> [□, (y, 1), □], □], □], (o, 0) -> [□, (t, 0) -> [□, (c, 0) -> [□, (h, 1), □], □], □], □], (t, 0) -> [(s, 0) -> [□, (i, 0) -> [(c, 0) -> [□, (a, 0) -> [□, (n, 0) -> [□, (n, 0) -> [□, (a, 1), □], □], □], (h, 0) -> [□, (i, 0) -> [□, (f, 0) -> [□, (f, 0) -> [□, (o, 1), □], □], □], □]], (m, 0) -> [□, (m, 0) -> [□, (o, 1), □], □], (u, 0) -> [□, (t, 0) -> [□, (u, 0) -> [□, (r, 1), □], □], □]], □], (a, 0) -> [□, (l, 0) -> [□, (c, 0) -> [□, (r, 0) -> [□, (u, 1), □], □], □], (r, 0) -> [□, (a, 0) -> [□, (n, 0) -> [□, (g, 0) -> [□, (r, 0) -> [□, (e, 0) -> [□, (d, 0) -> [□, (l, 0) -> [□, (u, 1), □], □], □], □], □], □], □], □]], □]]"
    return maxTestST("51", words, model, None, sol, 1)

maxTestsST = [testST_M_01, testST_M_11, testST_M_11m, testST_M_12, testST_M_12l, testST_M_30, testST_M_51] 

###########################################################################
# succ tests (mark out of 25)
###########################################################################

def succTestSTHelper(tree,clone,args):
    cases, sols = args
    (mark,msg) = (0,"")
    minimark = 1/len(sols)
    for i in range(len(cases)):
        (word,sol) = (cases[i],sols[i])
        (successor,error) = tryWithTimeout(lambda : tree.succ(word))
        if error != "": msg += error
        elif successor != sol: justError(i)
        else: # check if there was change
            changed = checkChange(tree,clone)
            if changed != "": mark += minimark*ifChanged
            else: mark += minimark
            msg += changed         
    return (mark,msg)

def succTestST(nm,words,model,cases,sols,grade):
    if len(cases)!=len(sols): print("test size mismatch! "+nm)
    return mainTest("succ",nm,words,model,grade,succTestSTHelper,(cases,sols))

def testST_S_01(): # successor of 3 strings in the tree [sample]
    cases = ["a", "aa", "aaa"]
    words = ["a", "aa", "aaa"]
    model = "(a, 1) -> [□, (a, 1) -> [□, (a, 1), □], □]"
    sol = ['aa', 'aaa', None]
    return succTestST("01",words,model,cases,sol,2)

def testST_S_02(): # successor of 3 strings not/in the tree [sample]
    cases = ["g", "u", "zz"]
    words = ["zz", "yy", "c", "g", "gg"]
    model = "(z, 0) -> [(y, 0) -> [(c, 1) -> [□, □, (g, 1) -> [□, (g, 1), □]], (y, 1), □], (z, 1), □]"
    sol = ['gg', 'yy', None]
    return succTestST("02",words,model,cases,sol,2)

def testST_S_03(): # successor of 3 strings not in the tree [sample]
    cases = ["0", "b", "c"]
    words = ["a"]
    model = "(a, 1)"
    sol = ['a', None, None]
    return succTestST("03",words,model,cases,sol,2)

def testST_S_15_1(): # successor of 15 strings not/in the tree [sample] 
    cases = ["aa", "a", "z", words15_1[2], words15_1[3]]
    words = words15_1
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 1), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 1), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 1), □], (u, 0) -> [□, (n, 0) -> [□, (t, 1), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 1), □], □]], (i, 0) -> [□, (t, 1), □], □], (e, 0) -> [□, (n, 1), (o, 0) -> [□, (f, 1), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 1), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 1), □], □], □], (c, 0) -> [□, (a, 1), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 1), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 1), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 1), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 1), □], □], □]]"
    sol = ['cats', 'cats', 'zath', 'olne', 'men']
    return succTestST("15_1",words,model,cases,sol,2)

def testST_S_30(): # successor of 30 strings not/in the tree [sample]
    cases = ["g", "z", "zg", "height", "geometry", words30[0], words30[1], words30[29]]
    words = words30
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 2), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 2), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 2), □], (u, 0) -> [□, (n, 0) -> [□, (t, 2), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 2), □], □]], (i, 0) -> [□, (t, 2), □], □], (e, 0) -> [□, (n, 2), (o, 0) -> [□, (f, 2), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 2), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 2), □], □], □], (c, 0) -> [□, (a, 2), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 2), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 2), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 2), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 2), □], □], □]]"
    sol = ['gos', 'zath', None, 'hit', 'gos', 'tam', 'mof', 'hit']
    return succTestST("30",words,model,cases,sol,3)

succTestsST = [testST_S_01, testST_S_02, testST_S_03, testST_S_15_1, testST_S_30]

###########################################################################
# pred tests (mark out of 25)
###########################################################################

def predTestSTHelper(tree,clone,args):
    cases, sols = args
    (mark,msg) = (0,"")
    minimark = 1/len(sols)
    for i in range(len(cases)):
        (word,sol) = (cases[i],sols[i])
        (predecessor,error) = tryWithTimeout(lambda : tree.pred(word))
        if error != "": msg += error
        elif predecessor != sol: justError(i)
        else: # check if there was change
            changed = checkChange(tree,clone)
            if changed != "": mark += minimark*ifChanged
            else: mark += minimark
            msg += changed         
    return (mark,msg)

def predTestST(nm,words,model,cases,sols,grade):
    if len(cases)!=len(sols): print("test size mismatch! "+nm)
    return mainTest("pred",nm,words,model,grade,predTestSTHelper,(cases,sols))

def testST_P_01(): # predecessor of 3 strings in the tree [sample]
    cases = ["a", "aa", "aaa"]
    words = ["a", "aa", "aaa"]
    model = "(a, 1) -> [□, (a, 1) -> [□, (a, 1), □], □]"
    sol = [None, 'a', 'aa']
    return predTestST("01",words,model,cases,sol,2)

def testST_P_02(): # predecessor of 3 strings not/in the tree [sample] 
    cases = ["g", "u", "zz"]
    words = ["zz", "yy", "c", "g", "gg"]
    model = "(z, 0) -> [(y, 0) -> [(c, 1) -> [□, □, (g, 1) -> [□, (g, 1), □]], (y, 1), □], (z, 1), □]"
    sol = ['c', 'gg', 'yy']
    return predTestST("02",words,model,cases,sol,2)

def testST_P_03(): # predecessor of 3 strings not in the tree [sample]
    cases = ["0", "b", "c"]
    words = ["a"]
    model = "(a, 1)"
    sol = [None, 'a', 'a']
    return predTestST("03",words,model,cases,sol,2)

def testST_P_15_1(): # predecessor of 15 strings not/in the tree [sample]
    cases = ["aa", "a", "z", words15_1[2], words15_1[3]]
    words = words15_1
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 1), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 1), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 1), □], (u, 0) -> [□, (n, 0) -> [□, (t, 1), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 1), □], □]], (i, 0) -> [□, (t, 1), □], □], (e, 0) -> [□, (n, 1), (o, 0) -> [□, (f, 1), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 1), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 1), □], □], □], (c, 0) -> [□, (a, 1), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 1), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 1), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 1), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 1), □], □], □]]"
    sol = [None, None, 'wesk', 'men', 'gos']
    return predTestST("2",words,model,cases,sol,2)

def testST_P_30(): # predecessor of 30 strings not/in the tree [sample]
    cases = ["g", "z", "zg", "height", "geometry", words30[0], words30[1], words30[29]]
    words = words30
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [□, (o, 0) -> [(a, 0) -> [□, (t, 0) -> [□, (s, 2), □], □], (f, 0) -> [□, (s, 0) -> [□, (o, 0) -> [□, (d, 2), □], □], □], □], □], (o, 0) -> [□, (l, 0) -> [□, (s, 2), □], (u, 0) -> [□, (n, 0) -> [□, (t, 2), □], □]], (g, 0) -> [□, (o, 0) -> [□, (s, 2), □], □]], (i, 0) -> [□, (t, 2), □], □], (e, 0) -> [□, (n, 2), (o, 0) -> [□, (f, 2), □]], (o, 0) -> [□, (l, 0) -> [□, (n, 0) -> [□, (e, 2), □], □], □]], (e, 0) -> [(a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (u, 2), □], □], □], (c, 0) -> [□, (a, 2), □], □], (z, 0) -> [(t, 0) -> [□, (r, 0) -> [(a, 0) -> [□, (m, 2), □], (o, 0) -> [□, (s, 0) -> [□, (s, 0) -> [□, (y, 2), □], □], □], □], (w, 0) -> [□, (e, 0) -> [□, (s, 0) -> [□, (k, 2), □], □], □]], (a, 0) -> [□, (t, 0) -> [□, (h, 2), □], □], □]]"
    sol = ['dunt', 'wesk', 'zath', 'gos', 'dunt', 'sargu', 'hit', 'dunt']
    return predTestST("5",words,model,cases,sol,3)

predTestsST = [testST_P_01, testST_P_02, testST_P_03, testST_P_15_1, testST_P_30]

###########################################################################
# remove tests (mark out of 20)
###########################################################################

def removeTestST(nm,words,model,cases,sol,size,grade):
    return mainTest("remove",nm,words,model,grade,removeTestSTHelper,(cases,sol,size))

def removeTestSTHelper(tree,_,args):
    cases,sol,size = args
    model = parseST(sol)
    (mark,msg) = (0,"")
    for i in range(len(cases)):
        toRemove = cases[i]
        (_,error) = tryWithTimeout(lambda : tree.remove(toRemove))
        if error != "": return (0,error)
    (stree,error) = tryWithTimeout(lambda : str(tree))
    if error != "": return (0,error)    
    if stree == sol: mark += printMark
    else: msg += printError
    if tree.size == size: mark += sizeMark
    else: msg += sizeError
    (same, error) = tryWithTimeout(lambda : equalSTrees(tree,model))
    if same == 1: mark += structMark
    elif same == -1: 
        msg += structError+"(dlist); "
    elif same == -2: msg += structError+"(stree); "
    else: msg += structError+error
    return (mark,msg)

def testST_R_00(): # removing from empty tree [sample]
    words = []
    toremove = ["hello"]
    model = "empty"
    sol = "empty"
    return removeTestST("00",words,model,toremove,sol,0,1)

def testST_R_01(): # removing element from singleton tree [sample]
    words = ["hello"]
    toremove = ["hello"]
    model = "(h, 0) -> [□, (e, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (o, 1), □], □], □], □]"
    sol =   "empty"
    return removeTestST("01",words,model,toremove,sol,0,1)

def testST_R_02(): # removing some from small tree [sample]
    words = ["hello" for i in range(5)] + ["world" for i in range(5)]
    toremove = ["hello","world"]
    model = "(h, 0) -> [□, (e, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (o, 5), □], □], □], (w, 0) -> [□, (o, 0) -> [□, (r, 0) -> [□, (l, 0) -> [□, (d, 5), □], □], □], □]]"
    sol = "(h, 0) -> [□, (e, 0) -> [□, (l, 0) -> [□, (l, 0) -> [□, (o, 4), □], □], □], (w, 0) -> [□, (o, 0) -> [□, (r, 0) -> [□, (l, 0) -> [□, (d, 4), □], □], □], □]]"
    return removeTestST("02",words,model,toremove,sol,8,1)

def testST_R_03(): # removing all from small tree (case 3 node removal) [sample]
    words = ["one", "two", "six", "four", "five"]
    toremove = words[:]
    model = "(o, 0) -> [(f, 0) -> [□, (o, 0) -> [(i, 0) -> [□, (v, 0) -> [□, (e, 1), □], □], (u, 0) -> [□, (r, 1), □], □], □], (n, 0) -> [□, (e, 1), □], (t, 0) -> [(s, 0) -> [□, (i, 0) -> [□, (x, 1), □], □], (w, 0) -> [□, (o, 1), □], □]]"
    sol =   "empty"
    return removeTestST("03",words,model,toremove,sol,0,2)

def testST_R_04(): # removing prefix from singleton tree [sample]
    words = ["tar", "target"]
    toremove = ["tar"]
    model = "(t, 0) -> [□, (a, 0) -> [□, (r, 1) -> [□, (g, 0) -> [□, (e, 0) -> [□, (t, 1), □], □], □], □], □]"
    sol =   "(t, 0) -> [□, (a, 0) -> [□, (r, 0) -> [□, (g, 0) -> [□, (e, 0) -> [□, (t, 1), □], □], □], □], □]"
    return removeTestST("04",words,model,toremove,sol,1,1)

def testST_R_30(): # remove string from small ST [sample]
    toremove = ["azac", "azab", "azabz"]
    words = ["azaz", "azac", "azab", "azaa", "azabz"]
    model ="(a, 0) -> [□, (z, 0) -> [□, (a, 0) -> [□, (z, 1) -> [(c, 1) -> [(b, 1) -> [(a, 1), (z, 1), □], □, □], □, □], □], □], □]"
    sol = "(a, 0) -> [□, (z, 0) -> [□, (a, 0) -> [□, (z, 1) -> [(a, 1), □, □], □], □], □]"
    return removeTestST("30",words,model,toremove,sol,2,1)

removeTestsST = [testST_R_00, testST_R_01, testST_R_02, testST_R_03, testST_R_04, testST_R_30]

# non-trivial test cases for StringTree tests

words15_1 = ["seca", "men", "mof", "hit", "dols", "zath", "dunt", "cofsod", "olne", "sargu", "trossy", "tam", "wesk", "cats", "gos"]
words15_2 = ["coss", "stren", "cro", "amra", "chent", "buth", "thaps", "end", "geya", "tur", "troarn", "woiram", "das", "trot", "tretsca"]
words30 = words15_1 + words15_1
words50_1 = ["ruotch", "art", "har", "asnu", "riply", "cusre", "knat", "talcru", "gug", "lirvinnun", "god", "droubica", "edent", "simmo", "bobd", "rass", "pli", "arob", "palla", "pejor", "palt", "jat", "dent", "astletwo", "gocl", "mutlunt", "pong", "on", "trangredlu", "bar", "back", "pim", "cast", "pralivear", "ar", "aix", "ehillem", "scanna", "shiffo", "cho", "dispa", "du", "reg", "foclotesh", "ratch", "sutur", "dy", "els", "rasuimu", "bof"]

######################################################################
# StringTree tests 
######################################################################

def testStringTreeFull(sid):
    if sid%2 == 1:
        xTests, xd = predTestsST, "pred"
    else: 
        xTests, xd = succTestsST, "succ"

    x = 0
    tests = list(zip(range(x,x+len(countTestsST)),countTestsST))
    cntM, cntT, cntR = runTests(tests)
    
    x += len(tests)
    tests = list(zip(range(x,x+len(maxTestsST)),maxTestsST))
    maxM, maxT, maxR = runTests(tests)
        
    x += len(tests)
    tests = list(zip(range(x, x+len(xTests)), xTests))
    xM, xT, xR = runTests(tests)

    x += len(tests)
    tests = list(zip(range(x,x+len(removeTestsST)),removeTestsST))
    remM, remT, remR = runTests(tests)

    marks = round(cntM+maxM+xM+remM,2)
    total = round(cntT+maxT+xT+remT,2)
    results =  (f"Testing ...\n{cntR}{maxR}{xR}{remR}"+
                f"\n-> count : {cntM} [{cntT}]"+
                f"\n-> max : {maxM} [{maxT}]"+
                f"\n-> {xd} : {xM} [{xT}]"+
                f"\n-> remove: {remM} [{remT}]"+
                f"\n-> *Total: {marks} [{total}]")
    print(results)
    return (sid,cntM,maxM,xM,remM,marks,results)

######################################################################
# main test script (full, marks add up to 75)
######################################################################

# import student code

flag = ""
signal.alarm(timeout)    
try:
    mod = importlib.import_module(module.split(".")[0])
    StringTree = mod.StringTree
    STNode = mod.STNode
except Exception as err: 
    flag = "IMPORT: "+str(err)
signal.alarm(0)
    
if flag != "":
    s = "\nTotal testing marks [80]: 0\nError: "+flag
    print(s)
    res = (sid,0,0,0,0,s)
else:
    print("Imported and will test")
    res = testStringTreeFull(int(sid))