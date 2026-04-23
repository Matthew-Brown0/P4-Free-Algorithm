from LinkedList import LinkedList

class Node:
    d = 0

    def __init__(self):
        self.marked = False
        self.parentNode: InternalNode = None
        self.md = 0
        self.mdValues = LinkedList()

    def changeParent(self, node: InternalNode):

        if (self.parentNode is not None) and self in self.parentNode.childNodes:
            self.parentNode.childNodes.remove(self)

        self.parentNode = node
        if self.parentNode is not None:
            self.parentNode.childNodes.append(self)

    def mark(self):
        self.marked = True

    def unmark(self):
        self.md = 0
        self.marked = False

    def toString():
        return "N/A"
    
# Node with 0 or 1 label, may have child nodes
class InternalNode(Node):

    def __init__(self, label: int):
        Node.__init__(self)
        self.childNodes = []
        self.label = label

    @property
    def d(self):
        return len(self.childNodes)
    
    def toString(self):
        childrenStr = ""
        for child in self.childNodes:
            if (len(childrenStr) == 0):
                childrenStr = " " + child.toString() + " "
            else:
                childrenStr += ", "+child.toString() + " "

        if self.marked:
            return f"Node({self.label})(M)[{childrenStr}]"
        else:
            return f"Node({self.label})[{childrenStr}]"
    
#Node with vertex reference, no child nodes
class VertexNode(Node):

    def __init__(self, value):
        Node.__init__(self)
        self.vertex = value

    def toString(self):
        if self.marked:
            return f"Vertex(M)[{self.vertex}]"
        else:
            return f"Vertex[{self.vertex}]"