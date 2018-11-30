from collections import deque

class Node:
    def __init__(self,name):
        self.name = name 
    def getName(self):
        return self.name
    def __str__(self):
        return self.name

class Edge:
    def __init__(self,src,dest):
        self.src = src 
        self.dest = dest
    
    def getSource(self):
        return self.src
    
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight = 1.0):
        self.src = src
        self.dest = dest
        self.weight = weight
    def getWeight(self):
        return self.weight
    def __str__(self):
        return self.src.getName() + '->(' + str(self.weight) + ')'+ self.dest.getName()

class Digraph:
    def __init__(self):
        self.nodes = []
        self.edges = {}
    def addNode(self,node):
        if node in self.nodes:
            raise ValueError('Duplicate node!')
        else:
            self.nodes.append(node)
            self.edges[node] = []
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if (src in self.nodes and dest in self.nodes):
            self.edges[src].append(dest)
        else:
            raise ValueError('Node not in graph')
    def childrenOf(self,node):
        return self.edges[node]
    def hasNode(self,node):
        return node in self.nodes
    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.getName() + '->'+ dest.getName() + '\n'
        return result[:-1] 


class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)

def printPath(path):
    result = ""
    for i in range(len(path)):
        result = result +str(path[i])
        if i != len(path) - 1:
            result =  result + '->'
    return result

def DFS(graph,start,end,path,shortest):
    
    path = path + [start]
    print('Current DFS path: ',printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path:
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph,node,end,path,shortest)
                if newPath != None:
                    shortest = newPath
    return shortest
def testDFS():
    nodes = []
    for name in range(5):
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.addNode(n)
    g.addEdge(Edge(nodes[0],nodes[1]))
    g.addEdge(Edge(nodes[0],nodes[2]))
    g.addEdge(Edge(nodes[1],nodes[3]))
    g.addEdge(Edge(nodes[2],nodes[3]))
    g.addEdge(Edge(nodes[3],nodes[4]))
    sp = DFS(g,nodes[0],nodes[4],[],None)
    print(printPath(sp))

def testDFS2():
    nodes = []
    for name in range(6):
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.addNode(n)
    g.addEdge(Edge(nodes[0],nodes[1]))
    g.addEdge(Edge(nodes[0],nodes[2]))
    g.addEdge(Edge(nodes[1],nodes[3]))
    g.addEdge(Edge(nodes[2],nodes[3]))
    g.addEdge(Edge(nodes[3],nodes[4]))
    g.addEdge(Edge(nodes[3],nodes[5]))
    g.addEdge(Edge(nodes[1],nodes[5]))
    g.addEdge(Edge(nodes[5],nodes[1]))
    g.addEdge(Edge(nodes[4],nodes[2]))
    g.addEdge(Edge(nodes[5],nodes[4]))
    sp = DFS(g,nodes[5],nodes[2],[],None)
    print(printPath(sp))

def BFS(graph,start,end):
    initPath = deque([start])
    pathQueue = deque([initPath]) # 保存当前已经探索的所有路径
    while len(pathQueue) != 0:
        tmpPath = pathQueue.popleft() # 每次迭代都会删除一条路径
        print('Current BFS path:',printPath(tmpPath))
        lastNode = tmpPath[-1] 
        if lastNode == end: # 如果这个路径的最后一个节点是end，那么这就是最短路径
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath: # 避免循环
                newPath = tmpPath + deque([nextNode]) # 创建新的路径
                pathQueue.append(newPath) # 添加到pathQueue
    return None
    
def testBFS():
    nodes = []
    for name in range(6):
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.addNode(n)
    g.addEdge(Edge(nodes[0],nodes[1]))
    g.addEdge(Edge(nodes[0],nodes[2]))
    g.addEdge(Edge(nodes[1],nodes[3]))
    g.addEdge(Edge(nodes[2],nodes[3]))
    g.addEdge(Edge(nodes[3],nodes[4]))
    g.addEdge(Edge(nodes[3],nodes[5]))
    g.addEdge(Edge(nodes[1],nodes[5]))
    g.addEdge(Edge(nodes[5],nodes[1]))
    g.addEdge(Edge(nodes[4],nodes[2]))
    g.addEdge(Edge(nodes[5],nodes[4]))
    sp = BFS(g,nodes[5],nodes[2])
    print(printPath(sp))

def main():
    testDFS()
    testDFS2()
    testBFS()

if __name__ == '__main__':
    main()