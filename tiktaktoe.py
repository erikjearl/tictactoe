#tiktaktoe.py

import turtle
import random
import time

#turtle
screen = turtle.Screen()
screen.title("Tik Tak Toe")
screen.bgcolor("lightgreen")
screen.setup(width=600, height=600)
screen.tracer(0)
pen = turtle.Turtle()
pen.pensize(10)
pen.ht()

#vars
gameState = -1
board = [[0,0,0],[0,0,0],[0,0,0]]
turns = 0
won = False
xTurn = True
cMoves = []
middle = False
side = False
corner = False
xWins = 0
oWins = 0

#gameState 0
def resetVars():
    global gameState
    global board
    global turns
    global won
    global xTurn
    global cMoves
    global middle
    global side
    global corner
    gameState = 0
    board = [[0,0,0],[0,0,0],[0,0,0]]
    turns = 0
    won = False
    cMoves = []
    middle = False
    side = False
    corner = False

def menuGUI():
    pen.clear()
    screen.bgcolor("blue")
    pen.penup()
    pen.color('hot pink')
    big = ('Courier', 31, 'bold')
    small = ('Courier', 20, 'bold')
    large = ('Courier', 75, 'bold')
    pen.goto(0,105)
    pen.write('Welcome to Tik Tak Toe', font=big, align='center')
    pen.color('red')
    pen.goto(-225,0)
    pen.write('Press:', font=small, align='center')
    pen.goto(-250,-50)
    pen.write('1- Play 1v1', font=small, align='left')
    pen.goto(-250,-75)
    pen.write('2- Computer Easy', font=small, align='left')
    pen.goto(-250,-100)
    pen.write('3- Computer Hard', font=small, align='left')
    pen.color("lime green")
    pen.goto(60,0)
    pen.write('Start:', font=small, align='left')
    pen.goto(125,-100)
    if xTurn:
        pen.write('X', font=large, align='left')
    else:
        pen.write('O', font=large, align='left')
    pen.goto(155,-105)
    pen.write('4- toggle', font=small, align='center')
    pen.goto(-120,-175)
    pen.color("cyan")
    pen.write('-X- wins: ' + str(xWins), font=small, align='center')
    pen.goto(120,-175)
    pen.write('-O- wins: ' + str(oWins), font=small, align='center')
    pen.color("orange")
    pen.goto(280,-290)
    pen.write('i- info', font=small, align='right')


#gameState 1
def drawBoard():
    pen.color("black")
    pen.setheading(0)
    for i in range(2):
        pen.penup()
        pen.goto(-300,100 - 200 * i)
        pen.pendown()
        pen.forward(600)
    pen.right(90)
    for i in range(2):
        pen.penup()
        pen.goto(-100 + 200 * i, 300)
        pen.pendown()
        pen.forward(600)
    screen.update()

def drawX(x,y):
    pen.color("red")
    pen.penup()
    pen.goto(-250 + 200 * x, 250 - 200 * y)
    pen.setheading(315)
    pen.pendown()
    pen.forward(141)
    pen.penup()
    pen.goto(-250 + 200 * (x + 0.5), 250 - 200 * y)
    pen.setheading(225)
    pen.pendown()
    pen.forward(141)
    pen.penup()
    screen.update()

def drawO(x,y):
    pen.color("blue")
    pen.penup()
    pen.goto(-245 + 200 * x, 245 - 200 * y)
    pen.setheading(225)
    pen.pendown()
    pen.circle(60)
    pen.penup()
    screen.update()

def makeMove(x,y):
    if gameState == 0:
        startMenu()
    else:
        global turns
        global xTurn

        if won:
            startMenu()
        else:
            r = 0 if x < -100 else 1 if x < 100 else 2
            c = 2 if y < -100 else 1 if y < 100 else 0
            if board[r][c] == 0 and not won:
                if gameState == 1 or (gameState in (2,3) and xTurn):
                    turns += 1
                    if xTurn:
                        board[r][c] = 'x'
                        drawX(r,c)
                    else:
                        board[r][c] = 'o'
                        drawO(r,c)
                    if checkWin():
                        win(xTurn)
                    xTurn = not xTurn
        if gameState == 2 and not (xTurn or won):
            xTurn = True
            time.sleep(0.5)
            logicCompE()
        elif gameState == 3 and not (xTurn or won):
            xTurn = True
            time.sleep(0.5)
            logicCompH()

def logicCompE():
    global turns
    global xTurn
    moves = []
    if wMove():
        moves = [wMove()[0]]
    elif lMove():
        moves = [lMove()[0]]
    else:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    moves.append((i,j))
    r,c = moves[random.randint(0,len(moves)-1)]
    moveComp(r,c)

def logicCompH():
    global cMoves
    global middle
    global side
    global corner
    
    moves = []
    print("turn",turns)
    
    if wMove():
        moves = [wMove()[0]]
    elif lMove():
        moves = [lMove()[0]]
    elif (turns % 2) == 0:
        if turns == 0:
            moves = [(0,0), (0,2), (2,0), (2,2)]
        elif turns == 2:
            arr = [board[0][1], board[1][0], board[1][2], board[2][1]]
            if board[1][1] != 0:
                middle = True
            elif arr.count(arr[0]) == len(arr):
                corner = True
            else:
                side = True
            if side:
                moves.append(aCorner(cMoves[0]))
            elif middle:
                moves.append(oCorner(cMoves[0]))
            else:
                moves = [(0,0), (0,2), (2,0), (2,2)]
        elif turns == 4:
            if side:
                moves.append(oCorner(cMoves[0]))
            elif corner:
                moves = [(0,0), (0,2), (2,0), (2,2)]
    else:   
        if turns == 1:
            if board[1][1] == 0:
                moves = [(1,1)]
            else:
                moves = [(0,0), (0,2), (2,0), (2,2)]
        elif turns == 3:
            if board[1][1] == 'o':
                moves = [(0,1), (1,0), (1,2), (2,1)]
            else:
                moves = [(0,0), (0,2), (2,0), (2,2)]
                

    if not moves:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    moves.append((i,j))

    print("avaliable", moves)
    r,c = moves[random.randint(0,len(moves)-1)]
    while board[r][c] != 0:
        r,c = moves[random.randint(0,len(moves)-1)]
    cMoves.append((r,c))
    moveComp(r,c)
    print("moves made", cMoves)

def wMove():
    mList = []
    for i in range(9):
        j = checkTeam(i,'o')
        if j:
            mList.append(j[0])
    return mList
    
def lMove():
    mList = []
    for i in range(9):
        j = checkTeam(i,'x')
        if j:
            mList.append(j[0])
    return mList

def aCorner(sMove):
    mList = ()
    if (0,0) == sMove:
        if board[0][1] == 'x' or board[1][2] == 'x':
            mList = (2,0)
        else:
            mList = (0,2)
    if (0,2) == sMove:
        if board[0][1] == 'x' or board[1][0] == 'x':
            mList = (2,2)
        else:
            mList = (0,0)
    if (2,2) == sMove:
        if board[2][1] == 'x' or board[1][0] == 'x':
            mList = (0,2)
        else:
            mList = (2,0)
    if (2,0) == sMove:
        if board[1][2] == 'x' or board[2][1] == 'x':
            mList = (0,0)
        else:
            mList = (2,2)
    return mList

def oCorner(sMove):
    mList = [(0,0), (0,2), (2,0), (2,2)]
    mList.remove(sMove)
    if (0,0) == sMove or (2,2) == sMove:
        mList.remove((0,2))
        mList.remove((2,0))
    else:
        mList.remove((0,0))
        mList.remove((2,2))
    return mList[0]

def moveComp(r,c):
    global turns
    turns += 1
    board[r][c] = 'o'
    drawO(r,c)
    if checkWin():
        win(not xTurn)


def checkWin():
    global turns
    global won
    if board[0][0] != 0:
        if check(0) or check (1):
            return True
    if board[1][1] != 0:
        if check(4) or check(5) or check(6) or check(7):
            return True
    if board[2][2] != 0:
        if check(2) or check (3):
            return True
    if not won and turns == 9:
        won = True
        screen.bgcolor("lightgrey")
        pen.penup()
        pen.goto(4,-4)
        pen.color("black")
        style = ('Courier', 34, 'bold')
        pen.write('TIE', font=style, align='center')
        return False
    
def check(case):
    if case == 0:
        arr = board[0]
    elif case == 1:
        arr = [row[0] for row in board]
    elif case == 2:
        arr = board[2]
    elif case == 3:
        arr = [row[2] for row in board]
    elif case == 4:
        arr = board[1]
    elif case == 5:
        arr = [row[1] for row in board]
    elif case == 6:
        arr = [board[0][0], board[1][1], board[2][2]]
    elif case == 7:
        arr = [board[0][2], board[1][1], board[2][0]]
    
    if arr.count(arr[0]) == len(arr):
        return True
    else:
        return False

def checkTeam(case, team):
    arr = []
    if case == 0:
        arr = board[0]
    elif case == 1:
        arr = board[1]
    elif case == 2:
        arr = board[2]
    elif case == 3:
        arr = [row[0] for row in board]
    elif case == 4:
        arr = [row[1] for row in board]
    elif case == 5:
        arr = [row[2] for row in board]
    elif case == 6:
        arr = [board[0][0], board[1][1], board[2][2]]
    elif case == 7:
        arr = [board[2][0], board[1][1], board[0][2]]
    mList = []
    if arr.count(team) == 2 and 0 in arr:
        if case in [0,1,2]:
            mList.append((case, arr.index(0)))
        elif case in [3,4,5]:
            mList.append((arr.index(0), case-3))
        elif case == 6:
            mList.append((arr.index(0),arr.index(0)))
        elif case == 7:
            if arr.index(0) == 0:
                mList.append((2,0))
            elif arr.index(0) == 1:
                mList.append((1,1))
            else:
                mList.append((0,2))
    return mList

def win(winner):
    global won
    global xWins
    global oWins
    won = True
    pen.color("black")
    pen.goto(4,-4)
    style = ('Courier', 34, 'bold')
    if(winner):
        screen.bgcolor("pink")
        pen.write('X WINS!', font=style, align='center')
        xWins += 1
    else:
        screen.bgcolor("lightblue")
        pen.write('O WINS!', font=style, align='center')
        oWins += 1

#select state
def startMenu():
    global gameState
    gameState = 0
    if gameState == 0:
        menuGUI()

def toggleTurn():
    global xTurn
    if gameState == 0:
        xTurn = not xTurn
        menuGUI()

def startGame():
    global gameState
    if gameState == 0:
        pen.clear()
        screen.bgcolor("yellow")
        resetVars()
        gameState = 1
        drawBoard()
    
def startComputerE():
    global gameState
    global xTurn
    if gameState == 0:
        pen.clear()
        screen.bgcolor("lightgreen")
        resetVars()
        gameState = 2
        drawBoard()
        if(not xTurn):
            xTurn = True
            logicCompE()

def startComputerH():
    global gameState
    global xTurn
    if gameState == 0:
        pen.clear()
        screen.bgcolor("lime green")
        resetVars()
        gameState = 3
        drawBoard()
        if(not xTurn):
            xTurn = True
            logicCompH()

def info():
    if gameState == 0:
        pen.clear()
        pen.penup()
        pen.color('hot pink')
        big = ('Courier', 31, 'italic')
        small = ('Courier', 20, 'bold')
        pen.goto(0,105)
        pen.write('INFO', font=big, align='center')
        pen.goto(-190,50)
        pen.write('* 3 in a row to win', font=small, align='left')
        pen.goto(-190,20)
        pen.write('* Computer plays as O', font=small, align='left')
        pen.goto(-190,-10)
        pen.write('* Press \'c\' to clear game', font=small, align='left')

#listeners
screen.listen()

screen.onkey(startGame, "1")
screen.onkey(startComputerE, "2")
screen.onkey(startComputerH, "3")
screen.onkey(toggleTurn, "4")
screen.onkey(startMenu, "c")
screen.onkey(info, "i")

screen.onclick(makeMove)

#update
startMenu()
screen.mainloop()
