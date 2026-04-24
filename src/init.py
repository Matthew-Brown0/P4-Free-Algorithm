from Graph import Graph
from Node import Node, InternalNode, VertexNode

#Resets the marks on all nodes of a tree, and marks leaf nodes.  Linked lists are also reset here
def markAdjacentLeaves(G: Graph, node: Node, x: VertexNode):
    node.mdValues.clear()
    node.unmark()

    if isinstance(node, VertexNode):
        if G.isEdge(node.vertex, x.vertex):
            node.mark()
    elif isinstance(node, InternalNode):
        for child in node.childNodes:
            markAdjacentLeaves(G, child, x)

#Given an empty list, populates it with marked nodes, given the root node
def insertMarkedNodes(node: Node, marked: list[Node]):
    if node.marked:
        marked.append(node)
    
    if isinstance(node, InternalNode):
        for child in node.childNodes:
            insertMarkedNodes(child, marked)

def MARK(G: Graph, R: InternalNode, x: VertexNode):
    markAdjacentLeaves(G, R, x)
    marked = []
    markedNodeRemains = False
    insertMarkedNodes(R, marked)

    while len(marked) > 0:
        u = marked.pop()
        if u.d != u.md:
            markedNodeRemains = True
            continue

        u.unmark()
        if u is not R:
            w = u.parentNode
            w.mark()
            w.md += 1
            w.mdValues.add(u)
            marked.insert(0, w)
    
    if R.d == 1 and markedNodeRemains:
        R.mark()

#Returns number of nodes between the given node (inclusive) and the root node (inclusive)
def nodeDepth(node: Node):
    if node.parentNode == None:
        return 0
    
    return 1 + nodeDepth(node.parentNode)

def numberOfAdjacentVertexNodes(G: Graph, R: Node, x: VertexNode):
    if isinstance(R, VertexNode):
        if G.isEdge(R.vertex, x.vertex):
            return 1
        else:
            return 0
    elif isinstance(R, InternalNode):
        count = 0
        for node in R.childNodes:
            count += numberOfAdjacentVertexNodes(G, node, x)
        return count

def areAllNodesMarkedAndUnmarked(R: Node):
    if R.marked:
        return False
    
    if isinstance(R, InternalNode):
        #All child nodes must have been marked and added to their parent's linked list
        if R.mdValues.size != len(R.childNodes):
            return False
        
        #Checks decendant nodes
        for node in R.childNodes:
            if not areAllNodesMarkedAndUnmarked(node):
                return False
    
    return True
    

#returns lowest node & success (is a cograph)
def findLowest(R: InternalNode) -> tuple[InternalNode, bool]:
    y = None
    if not R.marked:
        return None, False #Condition iii
    
    if R.md != R.d - 1:
        y = R
 
    w = R
    u = R
    R.unmark()

    markedNodes = []
    insertMarkedNodes(R, markedNodes)
    
    lowestNode = R
    lowestNodeDepth = 0

    while len(markedNodes) > 0:
        u = markedNodes.pop()
        t = None

        #Determines if u could be a returnable node
        if lowestNode is None:
            lowestNode = u
            lowestNodeDepth = nodeDepth(u)
        else:
            depth = nodeDepth(u)
            if depth > lowestNodeDepth:
                lowestNode = u
                lowestNodeDepth = depth

        if y is not None:
            return None, False #condition i or ii
        if u.label == 1:
            if u.md != u.d - 1:
                y = u
            if u.parentNode.marked:
                return None, False #condition i or vi
            else:
                t = u.parentNode.parentNode
        else:
            y = u
            t = u.parentNode
        u.unmark()

        while t is not w:
            if t is R:
                return None, False #Condition iv
            if not t.marked:
                return None, False #Condition iii, v, or vi
            if t.md != t.d - 1:
                return None, False  #Condition ii
            if t.parentNode.marked:
                return None, False #Condition i
            
            #Determines if t could be a returnable node
            depth = nodeDepth(u)
            if depth > lowestNodeDepth:
                lowestNode = t
                lowestNodeDepth = depth

            t.unmark()
            if t in markedNodes:
                markedNodes.remove(t)
            t = t.parentNode.parentNode
        w = u

    return lowestNode, True

def getFirstLeaf(arr: list[Node]):
    for node in arr:
        if isinstance(node, VertexNode):
            return node
    return None



def colorCotree(R: InternalNode, currentColor: int | None = None):
    if currentColor is None:
        currentColor = 1

    for i in range(len(R.childNodes)):
        node = R.childNodes[i]
        if isinstance(node, InternalNode):
            currentColor = colorCotree(node, currentColor)
        elif isinstance(node, VertexNode):
            node.color = currentColor

        if R.label == 1 and i != len(R.childNodes)-1:
            currentColor += 1
            
    return currentColor



def isCograph(G: Graph) -> bool:
    R = InternalNode(1)
    v1 = VertexNode(G.verticies[0])
    v2 = VertexNode(G.verticies[1])
    
    if G.isEdge(G.verticies[0], G.verticies[1]):
        v1.changeParent(R)
        v2.changeParent(R)
    else:
        zeroNode = InternalNode(0)
        zeroNode.changeParent(R)
        v1.changeParent(zeroNode)
        v2.changeParent(zeroNode)

    for v in G.verticies[2:]:
        
        x = VertexNode(v)
        MARK(G, R, x)
        if areAllNodesMarkedAndUnmarked(R):
            x.changeParent(R)
            continue
        #if there are no verticies, then there were no leafs to mark
        noNodesMarked = numberOfAdjacentVertexNodes(G, R, x) == 0
        if noNodesMarked:
            if R.d == 1:
                x.changeParent(R.childNodes[0])
            else:
                oldR = R
                R = InternalNode(1)
                zeroNode = InternalNode(0)
                zeroNode.changeParent(R)
                x.changeParent(zeroNode)
                oldR.changeParent(zeroNode)
            continue
        
        u, success = findLowest(R)
        if not success:
            return False
        
        markedChildren: list[Node] = u.mdValues.toArray()
        unmarkedChildren = []
        for child in u.childNodes:
            if child not in markedChildren:
                unmarkedChildren.append(child)

        childrenSet = markedChildren if u.label == 0 else unmarkedChildren
        if len(childrenSet) == 1:
            w = childrenSet[0]
            if isinstance(w, VertexNode):
                newNode = InternalNode(1) if u.label == 0 else InternalNode(0)
                newNode.changeParent(u)
                w.changeParent(newNode)
                x.changeParent(newNode)
            else:
                x.changeParent(w)
        else:
            y = InternalNode(u.label)
            for node in markedChildren:
                node.changeParent(y)

            if u.label == 0:
                newNode = InternalNode(1)
                newNode.changeParent(u)
                y.changeParent(newNode)
                x.changeParent(newNode)
            else:
                y.changeParent(u.parentNode)
                newNode = InternalNode(0)
                newNode.changeParent(y)
                u.changeParent(newNode)
                x.changeParent(newNode)
            if u is R:
                R = y
    colorCotree(R)
    print(R.toString())
    return True
            

#Example 1
#Uses Figure 1
graph = Graph(['a', 'b', 'c', 'd', 'e', 'f'])
graph.addEdge('a','b').addEdge('a','f').addEdge('a','e').addEdge('a','d')
graph.addEdge('b','e').addEdge('b','d').addEdge('b','f')
graph.addEdge('c','f').addEdge('c','e').addEdge('c','d')
print(isCograph(graph))

#Example 2
#Uses Figure 1 with a vertex 'x' and edge ax
graph = Graph(['a', 'b', 'c', 'd', 'e', 'f', 'x'])
graph.addEdge('a','b').addEdge('a','f').addEdge('a','e').addEdge('a','d')
graph.addEdge('b','e').addEdge('b','d').addEdge('b','f')
graph.addEdge('c','f').addEdge('c','e').addEdge('c','d')
graph.addEdge('a', 'x')
print(isCograph(graph))