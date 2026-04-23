#Graph with a vertex and edge set
class Graph:

    #Provide a list of vertex names
    def __init__(self, verticies: list[str]):
        self.verticies = verticies
        self.edges = {}

    #Create an edge between to verticies, given both vertex names
    def addEdge(self, a: str, b: str):
        if a == b:
            return self
        if a not in self.verticies:
            return self
        if b not in self.verticies:
            return self
        
        #stores vertex-pair both ways in a hashmap
        self.edges[a + "," + b] = True
        self.edges[b + "," + a] = True

        return self

    def isEdge(self, a: str, b: str) -> bool:
        return self.edges.get(a + "," + b) or self.edges.get(b + "," + a) or False