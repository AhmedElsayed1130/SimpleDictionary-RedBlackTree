import sys

class Node():
    #constructor 
    def __init__(self, value):
        self.parent = None
        self.value = value
        self.left = None
        self.right = None
        self.color = 'red'
    #helper function to check color and value of a spicific node 
    def printNode(self):
        print(self.value)
        print(self.color)

class RedBlackTree():
    # constructor is only used to init the tree
    def __init__(self, value):
        self.root = Node(value)
        self.root.color = 'black'
        self.size = 1;
    # function to search in the tree
    def search(self,input):
        tempnode = self.root
        while tempnode is not None:
            # go left 
            if input < tempnode.value:
                    tempnode = tempnode.left
            # go right
            elif input > tempnode.value:
                    tempnode = tempnode.right
            # found it
            else:
                print("YES")
                return
        # didnt find it
        print("NO")
    # function to insert in the tree
    def insert(self, input):
        #create a new node
        node = Node(input)
        tempnode = self.root

        while tempnode is not None:
            #value is less than node ---> Go Left
            if input < tempnode.value:
                # if node.left is null add the created node to it as a child
                if tempnode.left is None:
                    node.parent = tempnode
                    tempnode.left = node
                    break
                #  go left
                else:
                    tempnode = tempnode.left
            #value is more than node ---> Go Right
            elif input > tempnode.value:
                if tempnode.right is None:
                    node.parent = tempnode
                    tempnode.right = node
                    break
                else:
                    tempnode = tempnode.right
            else:
                print("Error: word already in dictionary ")
                return
        #i have added the increment size here to not increase size if a duplicate is inserted          
        self.size += 1
        # after normal BST insertion go handle the colors
        self.checkParentColor(node)

    # function to check color of parent and choose to either restructure tree or end
    def checkParentColor(self, node):

        if node.parent.color == 'black':
            return
        # parent's color is red go restructure
        else:
            self.restructure(node)
    # function to check color of uncle and act upon it if black rotate if red recolor
    def restructure(self, node):
        parent = node.parent
        grandparent = parent.parent
        # find position of parent to get the uncle 
        if grandparent.right == parent:
            uncle = grandparent.left
        else:
            uncle = grandparent.right

        # uncle is black go rotate
        if uncle is None or uncle.color == 'black':
            self.checkRotationCase(parent, uncle, grandparent, node)
        # uncle is red go recolor
        else:
            self.recolor(parent, uncle, grandparent)
    # function to recolor the parent uncle and grandparent 
    def recolor(self, parent, uncle, grandparent):
        parent.color = 'black'
        uncle.color = 'black'
        grandparent.color = 'red'
        # checking if grandparent is the root to not violet the RBT rules
        if grandparent == self.root:
            grandparent.color = 'black'
        # if grandparent isnt the root then go check what's the color of that grandparent
        else:
            self.checkParentColor(grandparent)
    # function to check which rotation case are we in
    def checkRotationCase(self, parent, uncle, grandparent, node):
        # we are looking for the position of parent and node
        # left
        if grandparent.left == parent:
            #left left
            if parent.left == node:
                self.leftLeftRotationCase(parent, grandparent)
            # left right
            else:
                self.leftRightRotationCase(parent, grandparent, node)
        # right
        else:
            # right right
            if parent.right == node:
                self.rightRightRotationCase(parent, grandparent)
            # right right 
            else:
                self.rightLeftRotationCase(parent, grandparent, node)
    # left left case
    def leftLeftRotationCase(self, parent, grandparent):
        # since rotation requires moving the grandparent that might change the root 
        if grandparent.parent is None:
            self.root = parent
        # in the left left case only the grandparent and parent are changing

        grandgrandparent = grandparent.parent

        ## Grandparent
        grandparent.color = 'red'
        grandparent.parent = parent
        grandparent.left = parent.right
        ## used to handle the 2 way refrence
        if parent.right is not None:
            parent.right.parent = grandparent
        grandparent.left = grandparent.left
        ## Parent
        parent.color = 'black'
        parent.left = parent.left
        parent.right = grandparent
        parent.parent = grandgrandparent
        # used to handle the 2 way refrence of the grandgrandparent
        if grandgrandparent is not None:
            if grandgrandparent.right == grandparent:
                grandgrandparent.right = parent
            else:
                grandgrandparent.left = parent
    # left right case
    def leftRightRotationCase(self, parent, grandparent, node):
        # in left right case only the node and parent changes
        ## parent 
        parent.parent = node
        parent.left = parent.left
        parent.right = node.left
        # 2 way refrence
        if node.left is not None:
            node.left.parent = parent
        ## node
        node.parent = grandparent
        node.right = node.right
        node.left = parent
        ## 2 way refrence
        if grandparent.left == parent:
            grandparent.left = node
        else:
            grandparent.right = node
        ## do the left left case but with the node as the parent
        self.leftLeftRotationCase(node, grandparent)
    # right right case
    def rightRightRotationCase(self, parent, grandparent):

        if grandparent.parent is None:
            self.root = parent

        grandgrandparent = grandparent.parent
        grandparent.color = 'red'
        grandparent.parent = parent
        grandparent.right = parent.left

        if parent.left is not None:
            parent.left.parent = grandparent
        grandparent.left = grandparent.left

        parent.color = 'black'
        parent.left = grandparent
        parent.right = parent.right
        parent.parent = grandgrandparent

        if grandgrandparent is not None:
            if grandgrandparent.right == grandparent:
                grandgrandparent.right = parent
            else:
                grandgrandparent.left = parent
    # right left case
    def rightLeftRotationCase(self, parent, grandparent, node):
        parent.parent = node
        parent.left = node.right
        parent.right = parent.right

        if node.right is not None:
            node.right.parent = parent
        node.parent = grandparent
        node.left = node.left
        node.right = parent
        if grandparent.left == parent:
            grandparent.left = node
        else:
            grandparent.right = node
        self.rightRightRotationCase(node, grandparent)
    #Depth First search approach to find height of tree
    def height(self,root):
        # check if tree is empty
        if root is None:
            # If TRUE return 0
            return 0 
        # Recursively call height of each node
        left = self.height(root.left)
        right = self.height(root.right)
    
        # Return max(leftHeight, rightHeight) at each iteration
        return max(left, right) + 1

file1 = open('EN-US-Dictionary.txt', 'r')
Lines = file1.readlines()

#first word is used to init the root of the tree
tree = RedBlackTree(Lines[0].strip())
# Strips the newline character
for i in range(1,len(Lines)):
    tree.insert(Lines[i].strip())

print("Dictionary Loaded !!")
print("Dictionary Size is: "+str(tree.size))


choice = 0 
while(True):
    print("Press 1 to Insert,  Press 2 to Search , Press 3 to Exit , Press 4 to view Dictionary Size , Press 5 to view Tree Height")
    choice = input()
    if choice == "3" :
        break
    elif choice == "2":
        word = input("Enter a word to Search for: ")
        tree.search(word)
    elif choice == "1":
        word = input("Enter a word to Insert: ")
        tree.insert(word)
    elif choice == "4":
        print("Dictionary Size is: "+str(tree.size))
    elif choice == "5":
        print("Tree Height is: "+str(tree.height(tree.root)))



# tree = RedBlackTree(1)
# tree.insert(2)
# tree.insert(3)
# tree.insert(4)
# tree.insert(5)
# tree.insert(6)
# tree.insert(7)
# tree.insert(8)
# tree.insert(9)
# tree.insert(10)
# tree.insert(11)



#tree.print_tree()
# tree.root.printNode()
# tree.root.left.printNode()
# tree.root.left.left.printNode()
# tree.root.left.right.printNode()
# tree.root.right.printNode()
# tree.root.right.left.printNode()
# tree.root.right.right.printNode()
# tree.root.right.right.left.printNode()
# tree.root.right.right.right.printNode()


