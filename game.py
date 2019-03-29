
import project5
import sys
from copy import copy,deepcopy
import pygame

'module with game mechanics'

class Faller:
    def __init__(self, col:str,grid:list,one: str,two :str,three: str,state:str):
        self.grid = grid
        self.col = int(col)
        self.one = one
        self.two = two
        self.three = three
        self.row = 0
        self.copy = []
        self.changed = []
        self.bottom = Jewel(self.three, self.col -1,-1)
        self.middle = Jewel(self.two, self.col -1,-1)
        self.top = Jewel(self.one, self.col -1,-1)
        self.jewels = [self.top.stat,self.middle.stat,self.bottom.stat]
        self.state = state.state

        self.count = 0

    def copygrid(self) -> None:
        '''makes a copy of grid'''
        copy = deepcopy(self.grid)
        return copy

    def tick(self) -> None:
        '''function that dictates what action to take once user inputs blank line (tick)'''
        if self.state == 'fall':
            self.continu()
        if self.state == 'land':
            self.land()
        elif self.state == 'match':
            self.match()
        elif self.state == 'freeze':
            self.freeze()
        else:
            pass




    def continu(self) -> None:
        '''makes the faller continue falling'''
        copy = self.copygrid()
        if ((self.row == 12) and (self.grid[self.row][self.col -1] is ' ')) or ((self.row < 12) and (self.grid[self.row+1][self.col -1] is not ' ')):
            copy[self.row][self.col - 1] = ('[' + str(self.jewels[2][2]) + ']')
            self.bottom = Jewel(str(self.jewels[2][2]),self.col -1,self.row)


            if (self.row - 1) >= 0:
                copy[self.row-1][self.col - 1] = ('[' + str(self.jewels[1][2]) + ']')
                self.middle = Jewel(str(self.jewels[1][2]),self.col -1,self.row-1)


            if (self.row - 2) >= 0:
                copy[self.row - 2][self.col - 1] = ('[' + str(self.jewels[0][2]) + ']')
                self.top = Jewel(str(self.jewels[0][2]), self.col -1, self.row - 2)

            self.state = 'land'
            self.copy = copy
            self.jewels = [self.top.stat, self.middle.stat, self.bottom.stat]




        elif (self.grid[self.row][self.col -1] is ' ') and (self.row < len(copy)-1):
            copy[self.row][self.col - 1] = ('[' + str(self.jewels[2][2]) + ']')
            self.bottom = Jewel(str(self.jewels[2][2]),self.col -1,self.row)


            if (self.row - 1) >= 0:
                copy[self.row-1][self.col - 1] = ('[' + str(self.jewels[1][2]) + ']')
                self.middle = Jewel(str(self.jewels[1][2]),self.col -1,self.row-1)


            if (self.row - 2) >= 0:
                copy[self.row - 2][self.col - 1] = ('[' + str(self.jewels[0][2]) + ']')
                self.top = Jewel(str(self.jewels[0][2]), self.col - 1, self.row - 2)


            self.copy = copy
            self.row += 1

            self.jewels = [self.top.stat, self.middle.stat, self.bottom.stat]
            self.state = 'fall'




    def land(self) -> None:
        '''makes the faller land'''
        for a in self.jewels:
            old = str(self.copy[a[0]][(a[1])])
            if a[0] >= 0:
                self.copy[a[0]][(a[1])] = ('|' + str(old[1]) + '|')
        self.state = 'freeze'


    def moveright(self) -> None:
        '''makes the faller move right'''
        if self.state is not 'ready':
            try:
                r = self.jewels[2][0]
                c = self.jewels[2][1]
                v = int(c) + 1
                if self.copy[r][v] is ' ':
                    for a in self.jewels:
                        if a[0] != -1:
                            self.copy[a[0]][(a[1]+1)] = self.copy[a[0]][(a[1])]
                            self.copy[a[0]][(a[1])] = ' '
                            a[1] +=1
                    self.col += 1
                else:
                    pass
            except:
                pass
            else:
                if self.freebelow() == True:
                    if self.state == 'land' or self.state == 'freeze':
                        self.state = 'fall'
                        self.continu()
                elif self.freebelow() == False:
                    if self.state == 'fall':
                        self.state = 'land'
                        self.land()
                        self.row +=1

        else:
            pass



    def moveleft(self) -> None:
        '''makes faller move left'''
        if self.state is not 'ready':
            try:
                r = self.jewels[2][0]
                c = self.jewels[2][1]
                v = int(c) + -1
                if self.copy[r][v] is ' ':
                    for a in self.jewels:
                        if a[0] != -1 and a[1]-1 >=0:
                            self.copy[a[0]][(a[1]-1)] = self.copy[a[0]][(a[1])]
                            self.copy[a[0]][(a[1])] = ' '
                            a[1] = a[1]- 1


            except:
                pass
            else:
                if self.jewels[2][1] >= 0:
                    self.col = self.jewels[2][1] + 1
                    if self.freebelow() == True:
                        if self.state == 'land' or self.state == 'freeze':
                            self.state = 'fall'
                            self.continu()
                    elif self.freebelow() == False:
                        if self.state == 'fall':
                            self.state = 'land'
                            self.land()
                            self.row +=1

        else:
            pass



    def rotate(self) -> None:
        '''makes faller rotate'''
        three = self.jewels[2][2]
        two = self.jewels[1][2]
        one = self.jewels[0][2]
        self.jewels[0][2] = three
        self.jewels[1][2] = one
        self.jewels[2][2] = two

        for a in self.jewels:
            if self.state == 'fall':
                if a[0] != -1:
                    self.copy[a[0]][a[1]] = ('[' + str(a[2]) + ']')
            elif self.state == 'freeze' or 'land':
                if a[0] != -1:
                    self.copy[a[0]][a[1]] = ('|' + str(a[2]) + '|')





    def freeze(self) -> None:
        '''makes faller freeze'''
        c = 0
        for a in self.jewels:
            old = str(self.copy[a[0]][(a[1])])
            if a[0] >= 0:
                c+=1
                self.copy[a[0]][(a[1])] = (str(old[1]))
        if c < 3:
            self.state = 'done'
        else:
            self.state = 'ready'
            self.grid = self.copy


    def match(self) -> None:
        '''changes grid if there is horizontal or vertical matching'''
        for i in range(len(self.copy)):
            for j in range(len(self.copy[0])):
                if '*' in self.copy[i][j]:
                    self.copy[i][j] = ' '
        self.copy = dropdown(self.copy)
        if horizontal(self.copy) == True or vertical(self.copy) == True:
            self.state = 'match'
        else:
            self.state = 'ready'


    def freebelow(self) -> bool:
        '''returns if a jewel has a free space below or not'''
        r = self.jewels[2][0]
        c = self.jewels[2][1]
        v = int(r) + 1
        try:
            if self.copy[v][c] == ' ':
                return True
            else:
                return False
        except:
            return False




class Jewel:
    '''creates a instance of one Jewel in the faller'''
    def __init__(self,value,column,row):
        self.val = value
        self.column = column
        self.row = row
        self.stat = [self.row,self.column,self.val]



class GameOverException(Exception):
    '''exception raised when frozen faller does not fit'''
    def __init__(self):

        sys.exit()

def horizontal(grid: list) -> bool:
    '''checks horizontal matching'''
    index = []
    count = 0
    for a in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[a][c] is not ' ' and (c <= len(grid[0]) - 3):
                if grid[a][c] == grid[a][c+1] == grid[a][c+2]:
                    index.append([a,c])
                    count = 1
                    while c+count < len(grid[0])-1:
                        try:
                            while grid[a][c + count] == grid[a][c]:
                                index.append([a,c + count])
                                count +=1
                        except:
                            pass
    for a in index:

        old = grid[a[0]][a[1]]
        if '*' not in grid[a[0]][a[1]]:
            grid[a[0]][a[1]] = ('*' + old + '*')
            count +=1
    if len(index) > 1:
        return True
    else:
        return False

def vertical(grid: list) -> bool:
    '''checks vertical matching'''
    index = []
    count = 0
    for a in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[a][c] is not ' ' and (a <= len(grid) - 3):
                if grid[a][c] == grid[a+1][c] == grid[a+2][c]:
                    index.append([a,c])
                    count = 1
                    while a+count < len(grid)-1:
                        try:
                            while grid[a + count][c] == grid[a][c]:
                                index.append([a + count,c])
                                count +=1
                        except:
                            pass
    for a in index:
        old = grid[a[0]][a[1]]
        if '*' not in grid[a[0]][a[1]]:
            grid[a[0]][a[1]] = ('*' + old + '*')
            count +=1
    if len(index) > 1:
        return True
    else:
        return False


def checker(grid: list) -> bool:
    '''checks if board has no holes'''
    result = True
    for r in range(len(grid) - 1):
        for c in range(len(grid[0])):
            if (grid[r][c] is not ' ') and (grid[r + 1][c] == ' '):
                result = False
    return result



def dropdown(grid) -> list:
    '''fills holes in grid'''
    while checker(grid) == False:
        for r in range(len(grid)-1):
            for c in range(len(grid[0])):
                if (grid[r][c] is not ' ') and (grid[r+1][c] == ' '):
                    val = grid[r][c]
                    grid[r][c] = ' '
                    grid[r+1][c] = val


    return grid



def startgrid():
    '''creates starting grid'''
    grid = [[' ' for x in range(int(6))] for y in range(int(13))]

    return grid



class GameState():
    '''creates initial gamestate'''
    def __init__(self):
        self.state = 'fall'
    def falling(self):
        self.state = 'fall'
    def landing(self):
        self.state = 'land'












