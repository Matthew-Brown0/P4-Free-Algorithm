class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, obj):
        newNode = Node(obj)
        if not self.head:
            self.head = newNode
        else:
            newNode.next = self.head
            self.head = newNode

        self.size += 1
        
    def clear(self):
        self.head = None
        self.size = 0

    def toArray(self):
        returnArr = []
        curNode: Node = self.head
        while self.head is not None:
            returnArr.append(curNode.data)
            self.head = self.head.next
        return returnArr