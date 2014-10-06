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

class Die:

    def __init(self, activeFace):
        self.activeFace = 1
        self.westSide = 4
        self.northSide = 2
    
    def rotate(direction):
        startActive = activeFace
        startWest = westFace
        startNorth = northFace
        if direction == Moves.north:   
            activeFace = 7-startNorth
            northFace = startNorth
        if direction == Moves.east:
            activeFace = startWest
            westFace = 7-startActive
        if direction == Moves.west:
            activeFace = 7-startWest
            westFace = startActive
        if direction == Moves.south:
            activeFace = startNorth
            startNorth = 7-active
        
class MazeState:
    maze = []

    def __init__(self, filename):
        readFile(filename)

    def readFile(filename):
        return 
    def getChildStates():
        return []
