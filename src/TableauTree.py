'''
TableauTree.py

@author: fabior
'''

class TreeNode:
    
    def __init__(self, key, value, annotation, depth, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.annotation = annotation
        self.depth = depth;
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild
    
    def hasRightChild(self):
        return self.rightChild
    
    def hasParent(self):
        return self.parent
    
    def hasLeftBrother(self):
        return self.parent.leftChild
    
    def hasRightBrother(self):
        return self.parent.rightChild
        
    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)
    
    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value
    
    def getAnnotation(self):
        return self.annotation
    
    def getDepth(self):
        return self.depth
    
    def getLeftChild(self):
        return self.leftChild
    
    def getRightChild(self):
        return self.rightChild
    
    def getParent(self):
        return self.parent
    
    def getLeftBrother(self):
        return self.parent.leftChild
    
    def getRightBrother(self):
        return self.parent.rightChild

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild
    
    def replaceNodeData(self, key, value, annotation, left, right):
        self.key = key
        self.value = value
        self.annotation = annotation
        self.leftChild = left
        self.rightChild = right
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
            
class Tree:
    
    def __init__(self):
        self.root = None
        self.size = 0
        #self.leaves = []
        self.branches = []
        
    def length(self):
        return self.size
    
    def getRoot(self):
        return self.root
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return self.root.__iter__()
    
    def put(self, key, value, annotation, node):
        self.size = self.size + 1
        if self.root:
            self._put(key, value, annotation, self.size, node)
        else:
            self.root = TreeNode(key, value, annotation, self.size)
            #self.leaves.append(self.root)
        
    def _put(self, key, value, annotation, depth, currentNode):
        if not currentNode.hasLeftChild() and not currentNode.hasRightChild():
            currentNode.leftChild = TreeNode(key, value, annotation, depth, parent=currentNode)
            #self.leaves.remove(currentNode)
            #self.leaves.append(currentNode.getLeftChild())
        elif currentNode.hasLeftChild() and not currentNode.hasRightChild():
            self._put(key, value, annotation, depth, currentNode.leftChild)
            
    def split(self, key1, value1, annotation1, key2, value2, annotation2, node):
        self.size = self.size + 1
        self._split(key1, value1, annotation1, key2, value2, annotation2, self.size, node)
        
    def _split(self, key1, value1, annotation1, key2, value2, annotation2, depth, currentNode):
        if not currentNode.hasLeftChild() and not currentNode.hasRightChild():
            currentNode.leftChild = TreeNode(key1, value1, annotation1, depth, parent=currentNode)
            currentNode.rightChild = TreeNode(key2, value2, annotation2, depth, parent=currentNode)
            #self.leaves.remove(currentNode)
            #self.leaves.append(currentNode.getLeftChild())
            #self.leaves.append(currentNode.getRightChild())
        elif currentNode.hasLeftChild() and not currentNode.hasRightChild():
            self._split(key1, value1, annotation1, key2, value2, annotation2, depth, currentNode.leftChild)
            
    def getNode(self, key):
        if self.root:
            res = self._getNode(key, self.root)
            if res:
                return res
            else:
                return None
        else:
            return None
        
    def _getNode(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        else:
            res = self._getNode(key, currentNode.leftChild)
            if res:
                return res
            else:
                res = self._getNode(key, currentNode.rightChild)
                if res:
                    return res
                else:
                    return None    
                
    #def getLeaves(self):
    #    return self.leaves
    
    def getBranches(self, node):
        branches = []
        branch = []
        currentNode = node
        while currentNode.hasParent():
            currentNode = currentNode.getParent()
            branch.insert(0, currentNode)
        #if currentNode != node:
        self._getBranches(node, branches, branch)
        return branches
        
    def _getBranches(self, node, branches, branch):
        if not node:
            return
        branch.append(node)
        if not node.hasLeftChild() and not node.hasRightChild():
            branches.append(branch)
            return
        else:
            self._getBranches(node.getLeftChild(), branches, list(branch))
            self._getBranches(node.getRightChild(), branches, list(branch))
         
    def getBranchNum(self, node):
        branches = self.getBranches(self.getRoot())
        branchNum = 1
        for branch in branches:
            if node in branch:
                return branchNum
            branchNum = branchNum + 1
            
    def getBranch(self, branchNum):
        branches = self.getBranches(self.root)
        return branches[branchNum-1]
            
    def getParents(self, node):
        parents = []
        while node.hasParent():
            node = node.getParent()
            parents.append(node)
        return parents