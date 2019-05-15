import Tkinter, PIL.Image, PIL.ImageTk, os.path, sys, math, time
from Tkinter import * 
from collections import Counter
root = Tk()
root.wm_title('Checkers')

canvas = Tkinter.Canvas(root, width=800, height=800, background='white')
canvas.grid(row=0, rowspan=10, column=0, columnspan=1)
rcheck=12
ycheck=12
w, h = 8, 8
Board = [[0 for x in range (w)] for y in range(h)]

Piece = [[0 for x in range (w)] for y in range(h)]

directory = os.path.dirname(os.path.abspath(__file__)) 

filename = os.path.join(directory, 'yellowpiece.gif')
filename2 = os.path.join(directory, 'redpiece.gif')
filename3 = os.path.join(directory, 'checkerboard.gif')
filename4 = os.path.join(directory, 'goldpiece.gif')
filename5 = os.path.join(directory, 'purplepiece.gif')

img = PIL.Image.open(filename) # create a PIL.Image from the jpg file
YP = PIL.ImageTk.PhotoImage(img) # convert the PIL.Image to a PIL.TkImage
img2 = PIL.Image.open(filename2)
RP = PIL.ImageTk.PhotoImage(img2)
img3 = PIL.Image.open(filename3)
brd = PIL.ImageTk.PhotoImage(img3)
img4 = PIL.Image.open(filename4)
GP = PIL.ImageTk.PhotoImage(img4)
img5 = PIL.Image.open(filename5)
OP = PIL.ImageTk.PhotoImage(img5)
cannot = 'cannot place piece here'
mode = 0
turn = 'red'
def setUp():
    brdimg = canvas.create_image(400, 400, image=brd)
    #red pieces
    x=1
    for all in range(4):
        Board[x][0] += 1
        Piece[x][0] = canvas.create_image(50+(100*x), 50, image=RP)
        x+=2
    x -= 9
    for all in range(4):
        Board[x][1] += 1
        Piece[x][1] = canvas.create_image(50+(100*x), 150, image=RP)
        x+=2
    x-=7
    for all in range(4):
        Board[x][2] += 1
        Piece[x][2] = canvas.create_image(50+(100*x), 250, image=RP)
        x+=2
    #yellow pieces
    x-=9
    
    for all in range(4):
        Board[x][7] += 2
        Piece[x][7] = canvas.create_image(50+(100*x), 750, image=YP)
        x+=2
    x -= 7
    for all in range(4):
        Board[x][6] += 2
        Piece[x][6] = canvas.create_image(50+(100*x), 650, image=YP)
        x+=2
    x-=9
    for all in range(4):
        Board[x][5] += 2
        Piece[x][5] = canvas.create_image(50+(100*x), 550, image=YP)
        x+=2
    
def cleanUp():
    canvas.delete("all")

startx, starty = 300, 300

def down(event):
    global startx, starty
    startx = event.x
    starty = event.y
    mouseclick(startx/100, starty/100)
def capture(pcx, pcy, scx, scy, cx, cy, pc):
    global turn, rcheck, ycheck
    '''these are used differently from everywhere else, 
    pcy/pcy == previous location
    scy/scy == enemy piece
    cx/cy == new location of player moving'''
    canvas.delete(Piece[scx][scy])
    canvas.delete(Piece[pcx][pcy])
    Board[scx][scy] = 0
    Board[pcx][pcy] = 0
    if pc == 'RP':
        if cy != 7:
            Board[cx][cy] = 1
            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=RP)
        else:
            Board[cx][cy] = 3
            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=OP)
        ycheck -= 1
        turn = 'yellow'
    elif pc == 'YP':
        if cy != 0:
            Board[cx][cy] = 2
            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=YP)
        else:
            Board[cx][cy] = 4
            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=GP)
        rcheck -= 1
        turn = 'red'
    elif pc == 'GP':
        Board[cx][cy] = 4
        Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=GP)
        rcheck -= 1
        turn = 'red'
    elif pc == 'OP':
        Board[cx][cy] = 3
        Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=OP)
        ycheck -= 1
        turn = 'yellow'
    print rcheck, ycheck
    if ycheck == 0:
        canvas.create_text(400,150,fill="darkblue",font="Times 140 italic bold",text="Red wins!")
        canvas.update
    elif rcheck == 0:
        canvas.create_text(400,150,fill="darkblue",font="Times 140 italic bold",text="Yellow wins!")
        canvas.update
    
def mouseclick(cx, cy):
    global mode, scx, scy
    
    #print cx+1, cy+1
    #remove # on previous line for piece placement test
    
    time.sleep(0.2)
    
    if mode == 0:
        if (turn == 'red' and Board[cx][cy] == 1 or Board[cx][cy] == 3) or (turn == 'yellow' and Board[cx][cy] == 2 or Board[cx][cy] == 4):
            mode += 1
            scx = cx
            scy = cy
        else:
            print 'not your piece'
    else:
        mode -= 1 
        movepc(cx, cy, scx, scy)
def movepc(cx, cy, scx, scy):
    global turn
    if Board[cx][cy] == 0:
        if turn == 'red' and (Board[scx][scy] == 1 or Board[scx][scy] == 3):#start of red pieces
            if Board[scx][scy] == 1:
                if cy == scy + 1:
                    if cx == scx + 1 or cx == scx - 1:
                        canvas.delete(Piece[scx][scy])#deletes previous piece
                        Board[scx][scy]=0
                        if cy == 7:
                            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=OP)
                            Board[cx][cy] = 3
                        else:
                            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=RP)
                            Board[cx][cy] = 1
                        turn = 'yellow' 
                
                elif cy == scy + 2:
                    if cx == scx + 2 and (Board[scx+1][scy+1] == 2 or Board[scx+1][scy+1] == 4):
                        capture(scx, scy, scx+1, scy+1, cx, cy, 'RP')  
                    elif cx == scx - 2 and (Board[scx-1][scy+1] == 2 or Board[scx+1][scy+1] == 4):
                        capture(scx, scy, scx-1, scy+1, cx, cy, 'RP')
                    else:
                        print cannot
                else:
                    print cannot
            elif Board[scx][scy] == 3:#orange(purple now) piece
                if Board[cx][cy] == 0 and (cy == scy + 1 or cy == scy - 1) and (cx == scx + 1 or cx == scx - 1):
                    canvas.delete(Piece[scx][scy])
                    Board[scx][scy] = 0
                    Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=OP)
                    Board[cx][cy] = 3 
                    turn = 'yellow'
                elif (cx == scx - 2 or cx == scx + 2) and (cy == scy - 2 or cy == scy + 2):
                    if cx>scx:
                        if cy>scy and (Board[scx+1][scy+1] == 2 or Board[scx+1][scy+1] == 4):
                            capture(scx, scy, scx+1, scy+1, cx, cy, 'OP')  
                        elif cy<scy and (Board[scx+1][scy-1] == 2 or Board[scx+1][scy-1] == 4):
                            capture(scx, scy, scx+1, scy-1, cx, cy, 'OP')
                        else:
                            print cannot
                    elif cx<scx:
                        if cy>scy and (Board[scx-1][scy+1] == 2 or Board[scx-1][scy+1] == 4):
                            capture(scx, scy, scx-1, scy+1, cx, cy, 'OP')
                        elif cy<scy and (Board[scx-1][scy-1] == 2 or Board[scx-1][scy-1] == 4):
                            capture(scx, scy, scx-1, scy-1, cx, cy, 'OP')
                        else:
                            print cannot
                    else:
                        print cannot
                else:
                    print cannot
            
        
        elif turn == 'yellow' and (Board[scx][scy] == 2 or Board[scx][scy] == 4): #start of yellow pieces
            if Board[scx][scy] == 2:
                if cy == scy - 1:#yellow
                    if cx == scx + 1 or cx == scx - 1:
                        canvas.delete(Piece[scx][scy])#deletes previous piece
                        Board[scx][scy] = 0
                        if cy == 0:
                            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=GP)
                            Board[cx][cy] = 4
                            turn = 'red'
                        else:
                            Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=YP)
                            Board[cx][cy] = 2
                            turn = 'red'
                        
                elif cy == scy - 2:
                    if cx == scx + 2 and (Board[scx+1][scy-1] == 1 or Board[scx+1][scy-1] == 3):
                        capture(scx, scy, scx+1, scy-1, cx, cy, 'YP')
                    elif cx == scx - 2 and (Board[scx-1][scy-1] == 1 or Board[scx-1][scy-1] == 3):
                        capture(scx, scy, scx-1, scy-1, cx, cy, 'YP')
                    else:
                        print cannot
                else:
                    print cannot
            elif Board[scx][scy]==4:#gold piece
                if Board[cx][cy] == 0 and (cy == scy + 1 or cy == scy - 1) and (cx == scx + 1 or cx == scx - 1):
                    canvas.delete(Piece[scx][scy])
                    Board[scx][scy] = 0
                    Piece[cx][cy] = canvas.create_image(50+(100*cx), 50+(100*cy), image=GP)
                    Board[cx][cy] = 4 
                    turn = 'red'
                elif (cx == scx - 2 or cx == scx + 2) and (cy == scy - 2 or cy == scy + 2):
                    if cx>scx:
                        if cy>scy and (Board[scx+1][scy+1] == 1 or Board[scx+1][scy+1] == 3):
                            capture(scx, scy, scx+1, scy+1, cx, cy, 'GP')  
                        elif cy<scy and (Board[scx+1][scy-1] == 1 or Board[scx+1][scy-1] == 3):
                            capture(scx, scy, scx+1, scy-1, cx, cy, 'GP')
                        else:
                            print cannot
                    elif cx<scx:
                        if cy>scy and (Board[scx-1][scy+1] == 1 or Board[scx-1][scy+1] == 3):
                            capture(scx, scy, scx-1, scy+1, cx, cy, 'GP')
                        elif cy<scy and (Board[scx-1][scy-1] == 1 or Board[scx-1][scy-1] == 3):
                            capture(scx, scy, scx-1, scy-1, cx, cy, 'GP')
                        else:
                            print cannot
                    else:
                        print cannot
                else:
                    print cannot
        else:
            print cannot
    else:
        print cannot
    

    
    
    
    
    
    
canvas.bind('<Button-1>', down)

sb = Tkinter.Button(root, text='Start', command=setUp)
sb.grid(row=0, column=1)
    
     
rb = Tkinter.Button(root, text='Reset', command=cleanUp)
rb.grid(row=1, column=1)


root.mainloop()