# MazeState.py
# Developed for CSCI-331 at RIT
# Authors: Mike Wideman, Dan Lavoie
# Description: Provides a class representing the state of a Rolling Die Maze

from enum import Enum
class Moves(Enum):
    north=1
    east=2
    south=3
    west=4

class Spaces:
    free=1
    obstacle=2
    current=3
    
class Die:
    def __init__(self):
        self.activeFace = 1
        self.westSide = 4
        self.northSide = 2
    
    def rotate(self, direction):
        startActive = self.activeFace
        startWest = self.westFace
        startNorth = self.northFace
        if direction == Moves.north:   
            self.activeFace = 7-startNorth
            self.northFace = startNorth
        if direction == Moves.east:
            self.activeFace = startWest
            self.westFace = 7-startActive
        if direction == Moves.west:
            self.activeFace = 7-startWest
            self.westFace = startActive
        if direction == Moves.south:
            self.activeFace = startNorth
            self.startNorth = 7-active

    def getCurrentFace(self):
        return self.activeFace
        
class MazeState:
    
    def __init__(self, file):
        self.maze = []
        self.start = ()
        self.goal = ()
        self.readFile(file)
        self.die = Die()
        self.current = ()
        
    def readFile(self, filename):
        file = open(filename)
        curLine = 0
        curChar = 0
        for line in file:
            self.maze.append([])
            for char in line:
                if char == 'S':
                    self.maze[curLine].append(Spaces.current)
                    self.start = (curLine, curChar)
                    self.current = (curLine, curChar)
                if char == '.':
                    self.maze[curLine].append(Spaces.free)
                if char == '*':
                    self.maze[curLine].append(Spaces.obstacle)
                if char == 'G':
                    self.maze[curLine].append(Spaces.free)
                    self.goal = (curLine,curChar)
                curChar+=1
            curLine+=1
            
    def getChildStates(self):
        return []

    def isSolution(self):
        return current == goal
    
    def printMaze(self):
        curLine = 0
        curChar = 0
        for line in self.maze:
            for space in line:
                if space == Spaces.current:
                    print(str(self.die.getCurrentFace()), end="")
                elif space == Spaces.obstacle:
                    print('*', end="")
                elif space == Spaces.free:
                    if (curLine,curChar) == self.start:
                        print('S', end="")
                    elif (curLine,curChar) == self.goal:
                        print('G', end="")
                    else:
                        print('.',end="")
                curChar+=1
            curLine+=1
            print() #print newline


maze = MazeState("maze.dat.txt")
maze.printMaze()
