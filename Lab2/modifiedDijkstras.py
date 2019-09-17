#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 00:39:59 2019

@author: Daniyal Maniar
"""

class graph:
    def __init__(self, maxVertex):
        self.maxVertex = maxVertex
        self.vertexs = {}
    def addNode(self, node):
        self.vertexs[node.name] = node
       
class node:
    def __init__(self, name):
        self.name = name
        self.neighbours = []
    def addNeighbours(self, node, dep, arr):
        self.neighbours.append({"node": node,"departure": dep,"arrival":arr})
        
class dijkstras:
    def __init__(self, graph):
        self.graph = graph
        self.reached = {}
        self.estimate = {}
        self.candidate = {}
        self.cost = {}
        self.predecessor = {}
        for vertex in self.graph.vertexs:      
            self.reached[vertex] = False
            self.estimate[vertex] = float('inf')
            self.candidate[vertex] = False
            self.cost[vertex] = float('inf')
            self.predecessor[vertex] = None
    def modifiedAlgorithm(self, start, end):
        self.cost[start] = 0
        self.reached[start] = True
        for neighbour in self.graph.vertexs[start].neighbours:
            if (self.estimate[neighbour["node"].name] > (neighbour["arrival"] - neighbour["departure"])):
                self.estimate[neighbour["node"].name] = neighbour["arrival"] - neighbour["departure"]
                self.predecessor[neighbour["node"].name] = {"name":start, "arrival": neighbour["arrival"]}
                self.candidate[neighbour["node"].name] = True
        for _ in range(self.graph.maxVertex):
            best_candidate_estimate = float('inf')
            for vertex in self.graph.vertexs:
                if (self.candidate[vertex] == True) and (self.estimate[vertex] < best_candidate_estimate):
                    v = vertex
                    best_candidate_estimate = self.estimate[vertex]
            self.cost[v] = self.estimate[v]
            self.reached[v] = True
            self.candidate[v] = False
            for neighbour in self.graph.vertexs[v].neighbours:
                if (self.predecessor[v] and (self.predecessor[v]["arrival"] < neighbour["departure"])) or not self.predecessor[v]:
                    if (self.reached[neighbour["node"].name] == False):
                        if ((self.cost[v] + (neighbour["arrival"] - neighbour["departure"])) < self.estimate[neighbour["node"].name]):
                            self.estimate[neighbour["node"].name] = self.cost[v] + (neighbour["arrival"] - neighbour["departure"]) 
                            self.candidate[neighbour["node"].name] = True
                            self.predecessor[neighbour["node"].name] = {"name":v, "arrival": neighbour["arrival"]}
            if self.reached[end]:
                return self.cost[end]
        return None
    
if __name__ == '__main__':
    with open("2019_Lab_2_flights_test_data.txt") as f:    
        s = f.read()
        s = s.strip()
        s = s.splitlines()
    #set the first line to be the size of graph
    testGraph = graph(int(s[0]))
    #remove the first line
    vertexs = int(s.pop(0))
    #Add all the nodes to the graph
    for i in range(vertexs):
        testGraph.addNode(node(i))
    #Add all the neighbours for each node
    for i in s:
        i = i.split()
        testGraph.vertexs[int(i[0])].addNeighbours(testGraph.vertexs[int(i[1])], int(i[2]), int(i[3]))
    #Initialize the class
    testingAlgo = dijkstras(testGraph)
    #Get the highest cost for the test case
    startVertex = 0
    endingVertex = 3
    result = testingAlgo.modifiedAlgorithm(startVertex,endingVertex)
    print ("Optimal route from "+str(startVertex)+" to "+str(endingVertex)+" which costs "+str(result)+" :\n")
    current = endingVertex
    path = []
    while current!= startVertex:
        previous = testingAlgo.predecessor[current]["name"]
        path.append("Fly from "+str(previous)+" to "+str(current)+".")
        current = testingAlgo.predecessor[current]["name"]
    for i in range(len(path)):
        print(path[len(path)-i-1])
    print("\nArrive at "+str(endingVertex)+" at time "+str(testingAlgo.predecessor[endingVertex]["arrival"])+".")