import random
from enum import Enum

class Tile:
    def __init__(self, position):
        self.mine = False
        self.closeBombsCounter = 0
        self.isClicked = False
        self.position = position

class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class Difficulty:
    def __init__(self, difficulty):
        self.size = self.selectSize(difficulty)
        self.numberOfMines = self.selectNumberOfMines(difficulty)

    def selectSize(self, difficulty):
        if difficulty == DifficultyEnum.EASY: return 10
        if difficulty == DifficultyEnum.MEDIUM: return 15
        if difficulty == DifficultyEnum.HARD: return 20

    def selectNumberOfMines(self, difficulty):
        if difficulty == DifficultyEnum.EASY: return 10
        if difficulty == DifficultyEnum.MEDIUM: return 40
        if difficulty == DifficultyEnum.HARD: return 99

class DifficultyEnum(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    NONE = 4

class Board:
    def __init__(self, difficulty):
        self.difficulty = Difficulty(difficulty)
        self.tiles = self.createEmptyBoard()
        self.placeMines()
        self.shuffleTiles()
        self.initialiseCloseBombCounter()
        self.numberOfTilesClicked = 0
        self.gameFinished = False

    def createEmptyBoard(self):
        tiles = [[Tile(Position(i, j)) for j in range(self.difficulty.size)] for i in range(self.difficulty.size)]
        return tiles
    
    def placeMines(self):
        numberOfMines = self.difficulty.numberOfMines
        for i in range(self.difficulty.size):
            for j in range(self.difficulty.size):
                self.tiles[i][j].mine = True
                numberOfMines -= 1
                if(numberOfMines == 0): return

    def shuffleTiles(self):
        numberOfShuffles = self.difficulty.numberOfMines
        for i in range(self.difficulty.size):
            for j in range(self.difficulty.size):
                y = random.randint(0, self.difficulty.size-1)
                x = random.randint(0, self.difficulty.size-1)
                if self.tiles[y][x].mine == False:
                    self.tiles[y][x].mine = True
                    self.tiles[i][j].mine = False
                numberOfShuffles -= 1
                if numberOfShuffles == 0: return

    def getAdjacentList(self, tile):
        adjacentPositions = [Position(tile.position.y - 1,tile.position.x - 1),
        Position(tile.position.y, tile.position.x - 1),
        Position(tile.position.y + 1, tile.position.x - 1),
        Position(tile.position.y - 1, tile.position.x),
        Position(tile.position.y + 1, tile.position.x),
        Position(tile.position.y - 1, tile.position.x + 1),
        Position(tile.position.y, tile.position.x + 1),
        Position(tile.position.y + 1, tile.position.x + 1)]

        return adjacentPositions

    def checkAdjacentForMines(self, tile):
        noOfMines = 0
        adjacentPositions = self.getAdjacentList(tile)
        for i in adjacentPositions:
            noOfMines += self.isBomb(i)

        return noOfMines

    def isBomb(self, position):
        if(position.y >= 0 and position.y < self.difficulty.size and position.x >= 0 and position.x < self.difficulty.size):
            if(self.tiles[position.y][position.x].mine == True):
                return 1
        return 0
    
    def initialiseCloseBombCounter(self):
        for i in range(self.difficulty.size):
            for j in range(self.difficulty.size):
                if(self.tiles[i][j].mine == False):
                    self.tiles[i][j].closeBombsCounter = self.checkAdjacentForMines(self.tiles[i][j])

    def chooseTile(self, position):
        if(self.tiles[position.y][position.x].isClicked == False):
            if(self.tiles[position.y][position.x].mine == True):
                self.failure()
                return
            self.tiles[position.y][position.x].isClicked = True
            self.numberOfTilesClicked += 1
            if(self.tiles[position.y][position.x].closeBombsCounter == 0):
                self.flipTiles(self.tiles[position.y][position.x])

    def checkTileIsInRangeAndUntouched(self, tile, tilesToBeFlipped):
        if(tile.y >= 0 and tile.y < self.difficulty.size and 
           tile.x >= 0 and tile.x < self.difficulty.size and 
           self.tiles[tile.y][tile.x] not in tilesToBeFlipped and 
           self.tiles[tile.y][tile.x].isClicked == False):
            return 1
        else:
            return 0

    def flipTiles(self, tile):
        tilesToBeFlipped = [tile]
        while(len(tilesToBeFlipped) > 0):
            currentTile = tilesToBeFlipped[len(tilesToBeFlipped) - 1]
            tilesToBeFlipped.pop()
            adjacentPositions = self.getAdjacentList(currentTile)
            for i in adjacentPositions:
                if(self.checkTileIsInRangeAndUntouched(i, tilesToBeFlipped)):
                    self.tiles[i.y][i.x].isClicked = True
                    self.numberOfTilesClicked += 1
                    if(self.tiles[i.y][i.x].closeBombsCounter == 0):
                        tilesToBeFlipped.append(self.tiles[i.y][i.x])

    def tilePrinter(self, i, j):
        if self.tiles[i][j].isClicked == False:
            return "."
        return str(self.tiles[i][j].closeBombsCounter)

    def printBoard(self):
        size = self.difficulty.size
        noOfLines = ((self.difficulty.size * 4) + 1)

        print("\n    ", end="")
        for i in range(size):
            print(" " + str(i).ljust(3, " "), end="")
        print("")

        print("   ", end="")
        for i in range(noOfLines):
            print("-", end="")

        for i in range(size, 0, -1):
            print("\n" + str(i - 1).ljust(3, " ") + "|", end="")
            for j in range(size):
                print(" " + self.tilePrinter(i - 1, j) + " |", end="")
            print(" " + str(i - 1) + "\n   ", end="")
            for j in range(noOfLines):
                print("-", end="")

        print("\n    ", end="")
        for i in range(size):
            print(" " + str(i).ljust(3, " "), end="")
        print("\n")

    def success(self):
        print("\nWinner")
        self.gameFinished = True

    def failure(self):
        print("\nBANG")
        self.gameFinished = True

def setDifficulty():

    print("Choose your difficulty!\n\nEasy    Medium     Hard\n")
    difficulty = DifficultyEnum.NONE

    while(difficulty == DifficultyEnum.NONE):
        difficultyString = input().lower()
        match difficultyString:

            case "easy":    
                difficulty = DifficultyEnum.EASY

            case "medium":
                difficulty = DifficultyEnum.MEDIUM

            case "hard":
                difficulty = DifficultyEnum.HARD

            case _:
                print("I'm sorry, could you repeat that?")

    return difficulty

def isNumber(coordinate):
    try:
        int(coordinate)
    except:
        return False
    else:
        return True

def chooseCoodinates(board, coordinateString):
    print(coordinateString + " input:")
    coordinate = input()
    coordinateIsNumber = isNumber(coordinate)

    while(coordinateIsNumber == False):
        print(coordinateString + " needs to be a number")
        coordinate = input()
        coordinateIsNumber = isNumber(coordinate)
    
    while(int(coordinate) < 0 or int(coordinate) >= board.difficulty.size):
        print("I'm sorry, could you repeat that?")
        coordinate = input()

    return coordinate

def main():
    
    difficulty = setDifficulty()

    board = Board(difficulty)

    while(board.gameFinished == False):
        board.printBoard()
        print("choose a tile")
        x = chooseCoodinates(board, "x")
        y = chooseCoodinates(board, "y")
        position = Position(x, y)
        board.chooseTile(position)
        if board.numberOfTilesClicked == ((board.difficulty.size ** 2) - board.difficulty.numberOfMines):
            board.success()

    print("\nThank you for playing!\n")
    exit(0)

main()