# Written by Gregory Libera, 2011
# A Checkers game written in Python using the Pygame Module set.
# Uses a combination of keyboard and mouse to play the game.
# Keyboard is used to select initial game setup options. The mouse is
#  used to move pieces.
# The player can play against either a human or computer opponent, or
#  watch 2 computer players play against each other.
# There are 3 levels of computer difficulty (albeit it, none are very difficult)

# In code Red is denoted by the string 'x', Gray is denoted by 'o'.
# Kings are denoted by the capitalized equivalents of each, 'X', and 'O' respectively.

# The computer AI is found in a seperate AI.py

import random, pygame, sys
from pygame.locals import *
from AI import *

# drawBoard is called each time the board needs to be drawn.
# drawBoard requires the list representation of the actual board,
#   and a reference to the window that the board is drawn on.
def drawBoard(board, window):
    
    boardRectangle = boardImage.get_rect()
    
    window.fill((0,0,0))
    window.blit(boardImage, boardRectangle)

    # Checks each entry in board[] to determine the location of each piece.
    for i in range(10,89):
      # Piece occupies position if entry is not ' '
      if board[i] != ' ':
        # Converts i into a two dimensional postion.
        # eg. 43 is the 4th row down, 3 column across.
        positionx, positiony  = list(str(i))
        # converts board position into pixel coordinate in window.
        coordinatex = (int(positiony)*100)-90
        coordinatey = (int(positionx)*100)-90
        # If a piece exists at a particular location, the corresponding image is drawn
        # on the screen.
        if board[i] == 'x':
          #location of red non-King
          window.blit(redPieceImage, (coordinatex,coordinatey))
        if board[i] == 'X':
          #location of red King
          window.blit(redKingPieceImage, (coordinatex,coordinatey))
        if board[i] == 'xh':
          #location of red highlighted non-King
          window.blit(redHighlightedPieceImage, (coordinatex,coordinatey))
        if board[i] == 'Xh':
          #location of red King
          window.blit(redHighlightedKingPieceImage, (coordinatex,coordinatey))
          
        if board[i] == 'o':
          #location of gray non-King
          window.blit(grayPieceImage, (coordinatex,coordinatey))
        if board[i] == 'O':
          #location of gray King
          window.blit(grayKingPieceImage, (coordinatex,coordinatey))
        if board[i] == 'oh':
          #location of gray highlighted non-King
          window.blit(grayHighlightedPieceImage, (coordinatex,coordinatey))
        if board[i] == 'Oh':
          #location of gray highlighted King
          window.blit(grayHighlightedKingPieceImage, (coordinatex,coordinatey))

    pygame.display.update()
       
# Used for testing purposes, draws the board in cmd window.
#    print('    1   2   3   4   5   6   7   8')
#    print('1 | ' + board[11] + ' | ' + board[12] + ' | ' + board[13] + ' | ' + board[14] + ' | ' + board[15] + ' | ' + board[16] + ' | ' + board[17] + ' | ' + board[18] + ' |')
#    print('-----------------------------------')
#    print('2 | ' + board[21] + ' | ' + board[22] + ' | ' + board[23] + ' | ' + board[24] + ' | ' + board[25] + ' | ' + board[26] + ' | ' + board[27] + ' | ' + board[28] + ' |')
#    print('-----------------------------------')
#    print('3 | ' + board[31] + ' | ' + board[32] + ' | ' + board[33] + ' | ' + board[34] + ' | ' + board[35] + ' | ' + board[36] + ' | ' + board[37] + ' | ' + board[38] + ' |')
#    print('-----------------------------------')
#    print('4 | ' + board[41] + ' | ' + board[42] + ' | ' + board[43] + ' | ' + board[44] + ' | ' + board[45] + ' | ' + board[46] + ' | ' + board[47] + ' | ' + board[48] + ' |')
#    print('-----------------------------------')
#    print('5 | ' + board[51] + ' | ' + board[52] + ' | ' + board[53] + ' | ' + board[54] + ' | ' + board[55] + ' | ' + board[56] + ' | ' + board[57] + ' | ' + board[58] + ' |')
#    print('-----------------------------------')
#    print('6 | ' + board[61] + ' | ' + board[62] + ' | ' + board[63] + ' | ' + board[64] + ' | ' + board[65] + ' | ' + board[66] + ' | ' + board[67] + ' | ' + board[68] + ' |')
#    print('-----------------------------------')
#    print('7 | ' + board[71] + ' | ' + board[72] + ' | ' + board[73] + ' | ' + board[74] + ' | ' + board[75] + ' | ' + board[76] + ' | ' + board[77] + ' | ' + board[78] + ' |')
#    print('-----------------------------------')
#    print('8 | ' + board[81] + ' | ' + board[82] + ' | ' + board[83] + ' | ' + board[84] + ' | ' + board[85] + ' | ' + board[86] + ' | ' + board[87] + ' | ' + board[88] + ' |')
    return

# playAgain returns True if the player wants to play again, otherwise it returns False.
def playAgain(window, font):
    
    RED = (255,0,0)
    
    rectangle = (125,325,500,40)
    pygame.draw.rect(window, (0,0,0), rectangle)
    print('Do you want to play again? (yes or no)')
    drawText('Do you want to play again? (y or n)', font , window, 125,325, RED)
    pygame.display.update()
    # Waits for user input.
    while True:
      event = pygame.event.wait()
      if event.type == QUIT:
        terminate()
      if event.type == KEYDOWN:
        if event.key == K_y:
          # Player wants another game played. So the screen if filled with black to
          # prevent the screen running over to the next game.
          window.fill((0,0,0))
          return True
        if event.key == K_n:
           return False
        if event.key == K_ESCAPE:
          terminate()
    return 

# After a move has been deemed valid, makeMove updates the board with changes.
def makeMove(board, letter, moveFrom, moveTo, jumpFlag):
    # The location of jumped piece becomes blank.
    board[jumpFlag] = ' '
    board[moveTo] = board[moveFrom]
    board[moveFrom] = ' '
    # Creates a king is the piece reaches the opponent's end.
    if letter == 'x' and moveTo < 20:
      board[moveTo] = letter.upper()
      return
    if letter == 'o' and moveTo > 80:
      board[moveTo] = letter.upper()
      return
    return

# isWinner determines if there is a winner. If the opponent has no valid moves,
# as determined by createMoveList then the player is the winner.
def isWinner(board, letter):
    if createMoveList(board, letter, None):
      return False
    else:
      return True

# isNotValid determines is a particular move is valid or not, and if the move is made, if
# and where a piece must move in the event of a double jump.
# A return of True means that the move is NOT valid.
# A return of False means that the move IS valid.
def isnotValid(moveFrom, moveTo, board, turn):
  # jumpFlag is the location of an opponents piece that is to be jumped.
  jumpFlag = 0
  # Ensures that moveFrom and MoveTo actually lies on the board.
  if moveTo < 89 and moveFrom < 89 and moveTo > 11 and moveFrom > 11 and onBoard(moveTo):
    # If there is currently a list of pieces that must jump and picked move is not part of that
    # list, then the picked move is not valid
    jumpList = mustJumpList(board, turn, None)
    if jumpList != [] and jumpList.count([moveFrom, moveTo]) == 0:
      return [True, jumpFlag]
    # Checks for the indications of a valid move.
    if turn == 'x':
      #Kings and non-Kings
      if board[moveFrom].lower() == 'x' and board[moveTo] == ' ':
          # Up the board adjacent move.
          if moveFrom - 11 == moveTo or moveFrom - 9 == moveTo:
            return [False, jumpFlag]
          # Up the board jump move.
          if moveFrom-11>11 and ((board[moveFrom-11].lower() == 'o') and (moveFrom - 22 == moveTo)):
            jumpFlag = moveFrom-11
            return [False, jumpFlag]
          # Up the board jump move.
          if moveFrom-11>11 and (board[moveFrom-9].lower() == 'o') and (moveFrom - 18 == moveTo):
            jumpFlag = moveFrom-9
            return [False, jumpFlag]
      #Kings only
      if board[moveFrom] == 'X' and board[moveTo] == ' ':
          # Down the board adjacent move.
          if moveFrom + 11 == moveTo or moveFrom + 9 == moveTo:
            return [False, jumpFlag]
          # Down the board jump move.
          if moveFrom+11<89 and ((board[moveFrom+11].lower() == 'o') and (moveFrom + 22 == moveTo)):
            jumpFlag = moveFrom+11
            return [False, jumpFlag]
          # Down the board jump move.
          if moveFrom+9<89 and (board[moveFrom+9].lower() == 'o') and (moveFrom + 18 == moveTo):
            jumpFlag = moveFrom+9
            return [False, jumpFlag]
    if turn == 'o':
      #Kings and not-Kings
      if board[moveFrom].lower() == 'o' and board[moveTo] == ' ':
          # Down the board adjacent move.
          if moveFrom + 11 == moveTo or moveFrom + 9 == moveTo:
            return [False, jumpFlag]
          # Down the board jump move.
          if moveFrom+11 < 89 and (board[moveFrom+11].lower() == 'x') and (moveFrom + 22 == moveTo):
            jumpFlag = moveFrom+11
            return [False, jumpFlag]
          # Down the board jump move.
          if moveFrom+9 < 89 and(board[moveFrom+9].lower() == 'x') and (moveFrom + 18 == moveTo):
            jumpFlag = moveFrom+9
            return [False, jumpFlag]
      #Kings only
      if board[moveFrom] == 'O' and board[moveTo] == ' ':
          # Up the board adjacent move.
          if moveFrom - 11 == moveTo or moveFrom - 9 == moveTo:
            return [False, jumpFlag]
          # Up the board jump move.
          if moveFrom-11 > 11 and ((board[moveFrom-11].lower() == 'x') and (moveFrom - 22 == moveTo)):
            jumpFlag = moveFrom-11
            return [False, jumpFlag]
          # Up the board jump move.
          if moveFrom-9 > 11 and (board[moveFrom-9].lower() == 'x') and (moveFrom - 18 == moveTo):
            jumpFlag = moveFrom-9
            return [False, jumpFlag]
  # If the requested move meets none of the possible positions of a valid move, then the move is not valid.
  return [True, jumpFlag]

# Determines whether of not a specific location is actually on the board.
# For example, 30, and 49 are valid numbers to check in board[], however since the board
# is reprented in a two digit number, the first corresponding to the y coordinate, the
# second to the x, the location: y=3,x=0 or y=4,x=9 does not exist on a grid where the
# x-values span 1-8.
def onBoard(location):
  if (location % 10 > 0) and (location % 10 != 9):
    return True
  else:
    return False

# Returns a list of all moves that a player must do due to the must jump rule.
# trackLocation is used if a player may have already made a move and is in a position
# to do a multiple jump with one piece.
# If there is a trackLocation the function will only check at that location,
 # otherwise it will check all locations.
def mustJumpList(board, turn, trackLocation):
  jumpList = [] 
  if trackLocation is None:
    a = 1
    b = 89
  else:
    a = trackLocation
    b = trackLocation + 1
  # Checks each location if a jump must be made from it. If so, the jump list is appended with
  # that location and the required destination.
  for i in range(a, b):
    #Kings and non-Kings
    if turn == 'x':
      if i-22>11 and onBoard(i-22) and board[i].lower() == 'x' and board[i-11].lower() == 'o' and board[i-22] == ' ':
        jumpList.append([i, i-22])
      if i-18>11 and onBoard(i-18) and board[i].lower() == 'x' and board[i-9].lower() == 'o' and board[i-18] == ' ':
        jumpList.append([i, i-18])
    #Kings only
    if turn == 'x' and board[i] == 'X':
      if i+22<89 and onBoard(i+22) and board[i+11].lower() == 'o' and board[i+22] == ' ':
        jumpList.append([i,i+22])
      if i+18<89 and onBoard(i+18) and board[i+9].lower() == 'o' and board[i+18] == ' ':
        jumpList.append([i, i+18])
    #Kings and non-Kings
    if turn == 'o':
      if i+22<89 and onBoard(i+22) and board[i].lower() == 'o' and board[i+11].lower() == 'x' and board[i+22] == ' ':
        jumpList.append([i, i+22])
      if i+18<89 and onBoard(i+18) and board[i].lower() == 'o' and board[i+9].lower() == 'x' and board[i+18] == ' ':
        jumpList.append([i, i+18])
    #Kings only
    if turn == 'o' and board[i] == 'O':
      if i-22>11 and onBoard(i-22) and board[i-11].lower() == 'x' and board[i-22] == ' ':
        jumpList.append([i, i-22])
      if i-18>11 and onBoard(i-18) and board[i-9].lower() == 'x' and board[i-18] == ' ':
        jumpList.append([i, i-18])
  return jumpList
        
def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if board[move] == ' ':
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

# When a player is to make a move, getPlayerMove is called.
# Accepted methods to move a piece are to either click on a
# piece then click on the destination, or to click on a piece
# and drag to it's destination.
# When the mouse cursor is hovered over a piece that can make
# valid move the player is alerted to that fact.
# When a player clicks on a piece that can make a valid move,
# the player is alerted to that fact.
# If a piece is selected (clicked on), another piece will not
# be highlighted if hovered over. Only the selected piece will be.
def getPlayerMove(board, turn, mustMoveFrom, window):
    move = '0'
    moveFrom = '11'
    moveTo = '11'
    jumpFlag = 0
    notValid = True
    # A list of moves is created to facilitate feedback when
    # the moveable piece is hovered over.
    moveList = []
    moveList = createMoveList(board, turn, mustMoveFrom)
    # The loop will continue until a valid move is made.
    while notValid:
      # Creates a duplicate of the board such that if a valid
      # piece is selected by the player, the board is redrawn
      # alerting the player which piece is selected.
      # tempboard specifically relates to pieces selected via
      #  a mouse click.
      tempboard = list(board)
      while True:
        while True:
          # Waits for input.
          event = pygame.event.wait()
          if event.type == QUIT:
            terminate()
          # If the player moves the mouse the location of the mouse
          # is recorded, this is used for highlighting.
          if event.type == MOUSEMOTION:
            # Another duplicate board is created.
            # dupeboard specifically relates to highlighting pieces
            #  the mouse cursor is hovering over.
            dupeboard = list(board)
            coordinatex = event.pos[0]
            coordinatey = event.pos[1]
            # Converts the pixel coordinates into board coordinates.
            if coordinatex < 100:
              positionx = 1
            else:
              positionx = int(list(str(coordinatex))[0])+1
            if coordinatey < 100:
              positiony = 1
            else:
              positiony = int(list(str(coordinatey))[0])+1
            boardPosition = positiony*10 + positionx

            # Checks to see if the mouse is hovering over a piece that
            # can make a valid move.
            i = len(moveList)
            while i:
              move = moveList[i-1]
              checkFrom = move[0]
              if checkFrom == boardPosition:
                # Changes dupeBoard to alert player of moveable piece.
                if turn == 'o' and board[boardPosition] == 'o':
                  dupeboard[boardPosition] = 'oh'
                if turn == 'x' and board[boardPosition] == 'x':
                  dupeboard[boardPosition] = 'xh'
                if turn == 'o' and board[boardPosition] == 'O':
                  dupeboard[boardPosition] = 'Oh'
                if turn == 'x' and board[boardPosition] == 'X':
                  dupeboard[boardPosition] = 'Xh'
                break
              i = i-1
            # If the player is hovering over a moveable piece, the board is redrawn.
            if board != dupeboard:
              drawBoard(dupeboard,window)
            # If the player was hovering over a moveable piece, the original board
            # is drawn to ensure the player knows that that piece is no longer highlighted.
            else:
              drawBoard(board,window)
          
          # If the player has clicked the mouse that location is recorded.
          if event.type == MOUSEBUTTONDOWN:
            coordinatex = event.pos[0]
            coordinatey = event.pos[1]
            break
          if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              terminate()
        # The pixel coordinates are converted into board coordinates.
        if coordinatex < 100:
          positionx = 1
        else:
          positionx = int(list(str(coordinatex))[0])+1
        if coordinatey < 100:
          positiony = 1
        else:
          positiony = int(list(str(coordinatey))[0])+1
        # moveFrom is the location, in board coordinates, that the player wants to move from.
        moveFrom = positiony*10 + positionx
        
        # Creates a list of all the valid positions that a piece
        # can be moved from, called checkFromList.
        i = len(moveList)
        checkFromList = []
        while i:
          move = moveList[i-1]
          checkFromList.append(move[0])
          i = i-1
        
        # Checks to see if a valid move exists from the location clicked.
        # If it does tempboard is revised to reflect that.
        if turn == 'o' and board[moveFrom] == 'o' and checkFromList.count(moveFrom):
          tempboard[moveFrom] = 'oh'
          break
        if turn == 'x' and board[moveFrom] == 'x' and checkFromList.count(moveFrom):
          tempboard[moveFrom] = 'xh'
          break
        if turn == 'o' and board[moveFrom] == 'O' and checkFromList.count(moveFrom):
          tempboard[moveFrom] = 'Oh'
          break
        if turn == 'x' and board[moveFrom] == 'X' and checkFromList.count(moveFrom):
          tempboard[moveFrom] = 'Xh'
          break

      # tempboard is drawn, and will specifically overwrite dupeboard.
      if board != tempboard:
        drawBoard(tempboard,window)
      
      # Waits until the mouse button is released.
      # This checks for a click and drag situation.
      while True:
        event = pygame.event.wait()
        if event.type == QUIT:
          terminate()
        if event.type == MOUSEBUTTONUP:
          coordinatex = event.pos[0]
          coordinatey = event.pos[1]        
          break
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            terminate()
      # Converts pixel coordinates to board coordinates.
      if coordinatex < 100:
        positionx = 1
      else:
        positionx = int(list(str(coordinatex))[0])+1
      if coordinatey < 100:
        positiony = 1
      else:
        positiony = int(list(str(coordinatey))[0])+1
      # moveTo is the location that the player wants to move a piece to.
      moveTo = positiony*10 + positionx
      
      # If the mouse is clicked and release at the same postion,
      # this would indicate that the player wants to select a
      # piece and click elsewhere to move, and not click and drag.
      if moveFrom == moveTo:
        while True:
          event = pygame.event.wait()
          if event.type == QUIT:
            terminate()
          if event.type == MOUSEBUTTONDOWN:
            coordinatex = event.pos[0]
            coordinatey = event.pos[1]        
            break
          if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              terminate()
        if coordinatex < 100:
          positionx = 1
        else:
          positionx = int(list(str(coordinatex))[0])+1
        if coordinatey < 100:
          positiony = 1
        else:
          positiony = int(list(str(coordinatey))[0])+1
        # moveTo is the location that the player wants to move a piece to.
        moveTo = positiony*10 + positionx

      # The main loop will only end is notValid is False, meaning that the move
      # is valid.
      if mustMoveFrom is None or mustMoveFrom == moveFrom:
        notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        
    return [int(moveFrom), int(moveTo), jumpFlag]
    
# Creates a list of all possible valid moves a player can make.
# It checks each location on the board if a player's piece exists there,
# then determines is a move is possible.
def createMoveList(board, turn, mustMoveFrom):
    moveList = []
    jumpFlag = 0
    notValid = True
    # Checks over the range of the entire board.
    for i in range(10,89):
      #Kings and non-Kings
      if turn == 'o' and board[i].lower() == 'o':
        moveFrom = i
        moveTo = i+9
        notValid = True
        # Only if no pieces are in a position where they must jump,
        # or such a piece exists at board[i], is that location checked
        # for a valid move.
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        # If a valid move exists at a location is the move list appended
        # by the move from location, the move to location, and if a jump
        # is possible, the location of the jumped piece.
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        # Checks if a valid jump exists.
        if i+18<89 and board[moveTo].lower() == 'x':
          moveTo = i+18
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
        moveTo = i+11
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i+22<89 and board[moveTo].lower() == 'x':
          moveTo = i+22
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
            
      #Kings only
      moveFrom = i
      if turn == 'o' and board[moveFrom] == 'O':
        moveTo = i-9
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i-18>11 and board[moveTo].lower() == 'x':
          moveTo = i-18
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
        moveTo = i-11
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i-22>11 and board[moveTo].lower() == 'x':
          moveTo = i-22
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
      
      #Kings and non-Kings      
      if turn == 'x' and board[i].lower() == 'x':
        moveFrom = i
        moveTo = i-9
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i-18>11 and board[moveTo].lower() == 'o':
          moveTo = i-18
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
        moveTo = i-11
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i-22>11 and board[moveTo].lower() == 'o':
          moveTo = i-22
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
            
      #Kings only
      moveFrom = i
      if turn == 'x' and board[moveFrom] == 'X':
        moveTo = i+9
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i+18<89 and board[moveTo].lower() == 'o':
          moveTo = i+18
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
        moveTo = i+11
        notValid = True
        if mustMoveFrom is None or mustMoveFrom == moveFrom:
          notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
        if not notValid:
          moveList.append([moveFrom,moveTo,jumpFlag])
        if i+22<89 and board[moveTo].lower() == 'o':
          moveTo = i+22
          notValid = True
          if mustMoveFrom is None or mustMoveFrom == moveFrom:
            notValid, jumpFlag = isnotValid(moveFrom, moveTo, board, turn)
          if not notValid:
            moveList.append([moveFrom,moveTo,jumpFlag])
    return moveList
    
# Resets the board to its default configuration.
def resetBoard():
    board = [' '] * 89
    for i in range(1,9):
        if i%2 == 0:
          board[10+i] = 'o'
          board[30+i] = 'o'
          board[70+i] = 'x'
        if i%2 == 1:
          board[20+i] = 'o'
          board[60+i] = 'x'
          board[80+i] = 'x'
    #board[12] = 'o'
    #board[21] = 'x'
    #board[23] = 'x'
    #board[34] = 'x'
    #board[61] = 'x'
    return board
    
# drawText is used to simplify the process of writing text on the window.
def drawText(text, font, surface, x, y, color):
  textobj = font.render(text, 1, color)
  textrect = textobj.get_rect()
  textrect.topleft = (x, y)
  surface.blit(textobj, textrect)

# Is called whenever the player wants to exit the game.
def terminate():
  sys.exit(0)

# The main function!
def main():

  # Initializes pygame.
  pygame.init()
  # Sets the caption in the upper right of the window.
  pygame.display.set_caption('Checkers')
  
  BLACK = (0,0,0)
  WHITE = (255,255,255)

  boardRectangle = boardImage.get_rect()

  # Creates the window the size of the CheckerBoard.png image.
  size = (width, height) = boardImage.get_size()
  theWindow = pygame.display.set_mode(size)
  font = pygame.font.SysFont(None, 48)
  theWindow.fill((0,0,0))

  print('Welcome to Checkers!')

  # The main loop of the program, this loop will never terminate unless the player,
  # wants to quit by pressing Esc, or clicking the X on the top left of the window.
  while True:  

    # players refers to the number of players playing each game.
    players = ''
    # playerLetter refers to the color that the human player will playing
    # as against a computer opponent.
    playerLetter = ''
    # difficulty refers to the difficulty of the computer player that
    # is playing the human player.
    difficulty = ''
    # Asks the player how many human players are going to be playing the game.
    # 0 = two computers, 1 = one human one computer, 2 = two human players.
    print('How many players?')
    drawText('How many players?', font , theWindow, 250,200, WHITE)
    drawText('Type 0, 1, or 2', font, theWindow, 290, 300, WHITE)
    print('Type 0, 1, or 2')
    pygame.display.flip()
    # Waits for valid input.
    while True:
      event = pygame.event.wait()
      if event.type == QUIT:
        terminate()
      if event.type == KEYDOWN:
        if event.key == K_0 or event.key == K_KP0:
          players = 0
          break
        if event.key == K_1 or event.key == K_KP1:
          players = 1
          break
        if event.key == K_2 or event.key == K_KP2:
          players = 2
          break
        if event.key == K_ESCAPE:
          terminate()

    print('Players = '+str(players))
    # player1, player2 refers to whether a computer or human player will be
    # playing either role.
    if int(players)==0:
      print('Zero Players')
      player1 = 'computer'
      player2 = 'computer'
    # If there is only 1 human player, the person can decide what level of
    # computer difficulty they want to play against, as well as their color.
    if int(players)==1:
      print('One Player')
      drawText('Select Difficulty: 1-Easy, 2-Medium, 3-Hard', font, theWindow, 50, 400, WHITE)
      print('Select Difficulty')
      pygame.display.flip()
      # Waits for input as the player decides on computer difficulty level.
      while True:
        event = pygame.event.wait()
        if event.type == QUIT:
          terminate()
        if event.type == KEYDOWN:
          if event.key == K_1 or event.key == K_KP1:
            difficulty = 'easy'
            break
          if event.key == K_2 or event.key == K_KP2:
            difficulty = 'medium'
            break
          if event.key == K_3 or event.key == K_KP3:
            difficulty = 'hard'
            break
          if event.key == K_ESCAPE:
            terminate()
      
      # Red = x,  Gray = o
      drawText('Do you want to be (R)ed or (G)ray?', font, theWindow, 120, 500, WHITE)
      print('Do you want to be (R)ed or (G)ray?')
      pygame.display.flip()
      # Waits for player to decide if they want to be red or gray.
      while True:
        event = pygame.event.wait()
        if event.type == QUIT:
          terminate()
        if event.type == KEYDOWN:
          if event.key == K_r:
            playerLetter = 'x'
            break
          if event.key == K_g:
            playerLetter = 'o'
            break
          if event.key == K_ESCAPE:
            terminate()
      # If player wants to be red, they are player 1.
      if playerLetter=='x':
        player1 = 'human'
        player2 = 'computer'
      # If player wants to be gray, they are player 2.
      else:
        player1 = 'computer'
        player2 = 'human'
    # If there are two human players.
    if int(players)==2:
      print('Two Players')
      player1 = 'human'
      player2 = 'human'
      
    theWindow.blit(boardImage, boardRectangle)    
    pygame.display.update()
    
    # theBoard is the representation of the board used throughout the game.
    # It is created and defined here.
    theBoard =  resetBoard()
    
    # player1Letter refers to red, player2Letter refers to gray.
    player1Letter, player2Letter = ['x', 'o']
    turn = 'Player 1'
    print(turn + ' will go first.')
    gameIsPlaying = True
    
    multiple = []

    while gameIsPlaying:
        if turn == 'Player 1':
            # Player 1's turn.
            multipleJump = None
            while True:
              # jumpFlag is used the location of a jumped piece.
              jumpFlag = 0
              # The board is drawn at the beginning of each move.
              drawBoard(theBoard, theWindow)
              print('Player 1')
              # A computer and a human each call different functions to make their moves.
              if player1 == 'computer':
                # The game is pause for 0.75 seconds such that the computer doesn't appear to move instantly.
                pygame.time.wait(0)
                if difficulty == 'hard':
                  moveFrom, moveTo, jumpFlag = AIAvoidBackLine(theBoard, player1Letter, multipleJump)
                elif difficulty == 'medium':
                  moveFrom, moveTo, jumpFlag = AIAvoid(theBoard, player1Letter, multipleJump)
                # Defaults to easy.
                else:
                  moveFrom, moveTo, jumpFlag = AIKings(theBoard, player1Letter, multipleJump)
              # Defaults to human controlled.
              else:
                moveFrom, moveTo, jumpFlag = getPlayerMove(theBoard, player1Letter,multipleJump, theWindow)
              # After the computer or human has created a valid move, makeMove is called to adjust the board.
              makeMove(theBoard, player1Letter, moveFrom, moveTo, jumpFlag)
              # If a jump was made during the move the board must be checked for a possible multiple jump.
              if jumpFlag != 0:
                multiple = mustJumpList(theBoard, player1Letter, moveTo)
                #print('multiple = ' + str(multiple))
              # If there exists another jump at the location moved to by the piece that made the original jump,
              # this fact is recorded in multipleJump.
              if multiple:
                multipleJump = multiple[0][0]
                #print('multipleJump = ' + str(multiple))
              else:
                multipleJump = None
              # Only if there does not exist a situation requiring a multiple jump, Player 1's turn ends.
              if multipleJump == None:
                break
            # Player 2 is checked for valid moves in isWinner.
            # If isWinner returns true, Player 1 is declared the winner, and the game ends.
            if isWinner(theBoard, player2Letter):
                drawBoard(theBoard, theWindow)
                print('Player 1 wins.')
                gameIsPlaying = False
            # Otherwise it is Player 2's turn.
            else:
                #input()
                turn = 'Player 2'

        # Player 2. Is basically the same as Player 1.
        if turn == 'Player 2':
            #Player 2's turn.
            multipleJump = None
            while True:
              jumpFlag = 0
              drawBoard(theBoard, theWindow)
              print('Player 2')
              if player2 == 'computer':
                pygame.time.wait(0)
                if difficulty == 'hard':
                  moveFrom, moveTo, jumpFlag = AIAvoidBackLine(theBoard, player2Letter, multipleJump)
                elif difficulty == 'medium':
                  moveFrom, moveTo, jumpFlag = AIAvoid(theBoard, player2Letter, multipleJump)
                else:
                  moveFrom, moveTo, jumpFlag = AIKings(theBoard, player2Letter, multipleJump)
              else:
                moveFrom, moveTo, jumpFlag = getPlayerMove(theBoard, player2Letter, multipleJump, theWindow)
              makeMove(theBoard, player2Letter, moveFrom, moveTo, jumpFlag)
              if jumpFlag != 0:
                multiple = mustJumpList(theBoard, player2Letter, moveTo)
                #print('multiple = ' + str(multiple))
              if multiple:
                multipleJump = multiple[0][0]
                #print('multipleJump = ' + str(multiple))
              else:
               multipleJump = None
              if multipleJump == None:
                break
            if isWinner(theBoard, player1Letter):
                drawBoard(theBoard, theWindow)
                print('Player 2 wins.')
                gameIsPlaying = False
            else:
                #input()
                turn = 'Player 1'

    # Asks the player is they want another game played, if not the program terminates.
    if not playAgain(theWindow, font):
        terminate()
        
if __name__ == '__main__':
    # Declaration of each external resource used in the game.
    redPieceImage = pygame.image.load('Checkers Resources\CheckerPieceRed.png')
    grayPieceImage = pygame.image.load('Checkers Resources\CheckerPieceGray.png')
    redKingPieceImage = pygame.image.load('Checkers Resources\CheckerPieceRedKing.png')
    grayKingPieceImage = pygame.image.load('Checkers Resources\CheckerPieceGrayKing.png')
    redHighlightedPieceImage = pygame.image.load('Checkers Resources\CheckerPieceRedHighlighted.png')
    grayHighlightedPieceImage = pygame.image.load('Checkers Resources\CheckerPieceGrayHighlighted.png')
    redHighlightedKingPieceImage = pygame.image.load('Checkers Resources\CheckerPieceRedKingHighlighted.png')
    grayHighlightedKingPieceImage = pygame.image.load('Checkers Resources\CheckerPieceGrayKingHighlighted.png')
    boardImage = pygame.image.load('Checkers Resources\CheckerBoard.png')
    main()
