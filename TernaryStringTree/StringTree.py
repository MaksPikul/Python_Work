class StringTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.dlist = DLinkedList()
        
    def __str__(self):
        if self.root == None: return "empty"
        return self.root.strTree()

    def add(self,st):
        if st == "": return
        dlistPtr = self.updateDList(st)
        if self.root == None: 
            self.root = STNode(st[0])
        ptr = self.root
        for i in range(len(st)):
            char = st[i]
            found_node = ptr.bin_search(char)
            if char < found_node.data:
                found_node.left = STNode(char)
                found_node.left.parent = found_node
                ptr = found_node.left
            elif char > found_node.data:
                found_node.right = STNode(char)
                found_node.right.parent = found_node
                ptr = found_node.right
            else:
                ptr = found_node
            # after the ith character is put into place, we move ptr
            # one level below 
            if i < len(st)-1:
                if ptr.mid == None:
                    ptr.mid = STNode(st[i+1])
                    ptr.mid.parent = ptr
                ptr = ptr.mid
        ptr.mult += 1
        if ptr.mult == 1: 
            ptr.dlistPtr = dlistPtr
        self.size += 1
    
    def addAll(self,A):
        for x in A: self.add(x)

    def printElems(self):
        ptr = self.dlist.head
        st = ""
        while ptr != None:
            st += ptr.data
            if ptr.next != None:
                st += ", "
            ptr = ptr.next
        print(st)

    # returns the smallest string in the tree (None if tree empty)
    def min(self):
        if self.root == None: return None
        return self._min(self.root).strFromTop()

    # returns the lexicographically minimal node in the tree rooted at node
    def _min(self, node):
        ptr = node
        while True: 
            while ptr.left != None: ptr = ptr.left
            if ptr.mult > 0: return ptr 
            ptr = ptr.mid
            
    # returns the largest string in the tree (None if tree empty)
    def max(self):
        if self.root == None: return None
        return self._max(self.root).strFromTop()
    
    # returns the lexicographically maximal node in the tree rooted at node
    
    def _max(self, node):
        ptr = node
        while True: 
            while ptr.right == None: 
                if ptr.mid == None:
                    return ptr
                ptr = ptr.mid
            ptr = ptr.right
            


    # returns the number of times that string st is stored in the tree
    def count(self, st):
        ptr = self.root # node which will be comparing data
        prevNode = ptr  # node which will hold the previous node when we reach ptr == None
        i = 0           
        
        while i != len(st):  # we do not move onto the next character unless we reach 
            char = st[i]     # the same character in the Tree
            temp = ptr
            if ptr == None: # returns 0 if tree is empty before starting
                return 0

            if char == ptr.data:
                ptr = ptr.mid
                i = i + 1
            elif char < ptr.data:
                ptr = ptr.left
            else:
                ptr = ptr.right
        return temp.mult
   

   


    # insert st in doubly linked list and return pointer to new list node
    # inefficient version
    def updateDList(self, st):
        if self.dlist.length == 0:
            return self.dlist.insertLeft(st,None)
        ptr = self.dlist.head
        while ptr != None and ptr.data < st:
            ptr = ptr.next
        if ptr == None:
            return self.dlist.append(st)
        if ptr.data == st: return None
        return self.dlist.insertLeft(st,ptr)
        
    # returns the smallest string in the tree
    # that is larger than st. If no such string exists, return None
    def succ(self, st): 
        # TODO
        return None
        

    # returns the largest string in the tree
    # that is smaller than st. If no such string exists, return None
    def pred(self, st): 
        if st == "" or self.root == None:
            return None
        firstNode = prev = ptr  = self.root.bin_search(st[0])
        pred = firstNode.left
        i = 0

        while ptr and i < len(st):
            prev = ptr
            if st[i] < ptr.data:
                ptr = ptr.left
            elif st[i] > ptr.data:
                pred = ptr
                ptr = ptr.right
            else:
                if ptr.left:  
                    pred = ptr.left
                

                i = i + 1
                prev = ptr
                ptr = ptr.mid
        
        
        if pred == None:
            if firstNode == self.root:
                return None
            if firstNode.parent.right == firstNode:
                if firstNode.parent.mid:
                    pred = firstNode.parent.mid
                else:
                    pred = firstNode.parent
        
        if pred:
             
            if pred.mult >= 1:
                return pred.strFromTop()
            else:
                return self._max(pred).strFromTop()
        else:
            return None


    def remove(self, st):
        if st == "" or self.root == None:
            return None
        
        firstNode = ptr = self.root.bin_search(st[0])
        i = 0
        while i < len(st):
            prev = ptr
            

            if ptr == None:
                return None # word not found

            if ptr.data == st[i]:
                i = i + 1
                ptr = ptr.mid
            elif ptr.data > st[i]:
                ptr = ptr.left
            else:
                ptr = ptr.right
        
        Node = None
        #can check multiplicites and start removing
        if prev.mult == 0:
            return None      # st exists within a word in tree, check multiplicity to see if word in tree
        elif prev.mult > 1:
            prev.mult = prev.mult - 1
            self.size = self.size - 1 
            return None
        else:
            Node = prev.dlistPtr
            prev.mult = prev.mult - 1
            ptr = prev
            while ptr.mult == 0 and ptr.mid == None:

                if ptr == self.root:
                    if ptr.right:
                        self.root = ptr.right
                        self.root.parent = None
                        if ptr.left:
                            if self.root.left:
                                self.root.left.left = ptr.left
                                ptr.left.parent = self.root.left
                            else:
                                self.root.left = ptr.left
                                ptr.left.parent = self.root
                    elif ptr.left:
                        self.root = ptr.left
                        self.root.parent = None
                    else:
                        self.root = None
                        self.dlist = DLinkedList()
                    break

                elif ptr.left or ptr.right:
                    
                    if ptr.right:
                        
                        if ptr.parent.mult == 1 and ptr.mid:
                            ptr.parent.right = ptr.right
                            
                        else:
                            ptr.parent.mid = ptr.right
                            ptr.right.left = ptr.left 
                        ptr.right.parent = ptr.parent
                        if ptr.left:
                            ptr.left.parent = ptr.right
                    else:
                        if ptr.parent.mult == 1:
                            ptr.parent.left = ptr.left
                        else:
                            ptr.parent.mid = ptr.left
                        ptr.left.parent = ptr.parent
                    break

                else:
                    compare = ptr
                    ptr = ptr.parent
                    if compare == ptr.left:
                        ptr.left = compare.left
                        if compare.left:
                            compare.left.parent = ptr
                    elif compare == ptr.right:
                        ptr.right = compare.right
                        if compare.right:
                            compare.right.parent = ptr
                    else:
                        ptr.mid = None

        
        self.size = self.size - 1
        self.dlist.remove(Node)
        return None
        
        

        
        

    def updateDList2(self, st):
        return None
    
        #find the last node of predecessor string of string st
        #this node will hold dlistPtr, a pointer to the node containing predecessor word
        # predNode = ptr.dlistPtr
        # newNode = DNode(st, predNode, predNode.next)
        # predNode.next = newNode
        # newNode.prev = newNode
        


    
class STNode:
    def __init__(self,d):
        self.data = d
        self.left = self.right = self.mid = None
        self.mult = 0
        self.dlistPtr = None
        self.parent = None

    # performs BST search for d starting from d. If d is not in the
    # tree, it returns the parent node of where it should have been
    def bin_search(self, d):
        if self.data == d: return self
        if self.data > d: 
            if self.left == None: return self
            return self.left.bin_search(d)
        if self.data < d: 
            if self.right == None: return self
            return self.right.bin_search(d)
        assert(0) # should not get here    

    # prints the node's data and multiplicity
    def __str__(self):
        return "("+str(self.data)+", "+str(self.mult)+")"   

    # returns string corresponding to node
    def strFromTop(self):
        ptr = self
        s = str(self.data)
        while ptr.parent != None and ptr.parent.mid != ptr:
            ptr = ptr.parent
        if ptr.parent == None: return s
        return ptr.parent.strFromTop()+s
   
    # prints the node and all its children in a string
    def strTree(self):  
        st = "("+str(self.data)+", "+str(self.mult)+")"
        if self.left == self.mid == self.right == None: return st
        st += " -> ["
        if self.left != None:
            st += self.left.strTree()
        else: st += "□"
        if self.mid != None:
            st += ", "+self.mid.strTree()
        else: st += ", □"
        if self.right != None:
            st += ", "+self.right.strTree()
        else: st += ", □"
        return st + "]"

class DNode:
    def __init__(self, d, n, p):
        self.data = d
        self.next = n
        self.prev = p

    def __str__(self):
        return str(self.data)
        
class DLinkedList:
    def __init__(self):
        self.head = self.tail = None
        self.length = 0

    # inserts a node to the left of n with data d and returns it. 
    # If it is an empty list, it does not matter what n is, 
    # we create just one node.
    def insertLeft(self, d, n):
        self.length += 1
        
        if self.length == 1: 
            self.head = DNode(d, None, None)
            self.tail = self.head
            return self.head

        np = n.prev
        n.prev = DNode(d, n, np)
        if np == None:
            self.head = n.prev
        else:
            np.next = n.prev
        return n.prev

    # inserts node with d at tail of list and returns it
    def append(self, d):
        if self.length == 0:
            return self.insertLeft(d,None)
        self.length += 1
        self.tail.next = DNode(d, None, self.tail)
        self.tail = self.tail.next
        return self.tail
        
    # removes node n off the list
    def remove(self, n): 
        self.length -= 1
        if n.prev == None:
            if n.next != None: n.next.prev = None
            self.head = n.next
            return
        if n.next == None:
            n.prev.next = None
            self.tail = n.prev
            return
        n.prev.next = n.next
        n.next.prev = n.prev

    def __str__(self):
        if self.head == None: 
            return "empty"
        st = "-"
        ptr = self.head
        while ptr != None:
            st += "-> "+str(ptr)+" "
            ptr = ptr.next
        return st+"|"