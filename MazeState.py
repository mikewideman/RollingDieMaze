# MazeState.py
# Developed for CSCI-331 at RIT
# Authors: Mike Wideman, Dan Lavoie
# Description: Provides a class representing the state of a Rolling Die Maze.
# Also provides a Die class representing the state of a standard six-sided die.

from enum import Enum
import copy
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
        self.westFace = 4
        self.northFace = 2
    
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
            self.startNorth = 7-startActive

    def getActiveFace(self):
        return self.activeFace
        
class MazeState:
    
    def __init__(self, file):
        self.maze = []
        self.start = ()
        self.goal = ()
        self.readFile(file)
        self.die = Die()
        self.current = (0,0)
        
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

    def isValidSpace(self,x,y):
        return x >= 0 and y >=0 and x < len(self.maze) and y < len(self.maze[x]) and not self.maze[x][y] == '*'

    def getChildStates(self):
        children = []
        possibleMoves = [Moves.north, Moves.east, Moves.south, Moves.west]
        for move in possibleMoves:
            childCandidate = copy.deepcopy(self)
            nextSpace = self.current
            if move == Moves.north:
                nextSpace = (self.current[0]-1, self.current[1])
            elif move == Moves.south:
                nextSpace = (self.current[0]+1, self.current[1])
            elif move == Moves.east:
                nextSpace = (self.current[0], self.current[1]+1)
            elif move == Moves.west:
                nextSpace = (self.current[0], self.current[1]-1)
            if self.isValidSpace(nextSpace[0], nextSpace[1]):
                childCandidate.maze[self.current[0]][self.current[1]] = Spaces.free
                childCandidate.maze[nextSpace[0]][nextSpace[1]] = Spaces.current
                childCandidate.current = nextSpace
                childCandidate.die.rotate(move)
                if not childCandidate.die.getActiveFace() == 6:
                    children.append(childCandidate)
        return children

    def isSolution(self):
        return self.current == self.goal
    
    def printMaze(self):
        curLine = 0
        curChar = 0
        for line in self.maze:
            for space in line:
                if space == Spaces.current:
                    print(str(self.die.getActiveFace()), end="")
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

#Test code for this module
#maze = MazeState("maze.dat.txt")
#children = maze.getChildStates()
#nextChildren = children[0].getChildStates()
#maze.printMaze()
#for child in children:
#    child.printMaze()
#for child in nextChildren:
#    child.printMaze()
