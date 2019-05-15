# Written by Gregory Libera, 2011
# Defines 4 different types of AI for use in checkers game written by myself.
# Companion to Checkers.py

from Checkers import *

# AIRandom defines an AI that creates a list of all possible move it can make,
#  and then picks randomly from them.      
def AIRandom(board, computerLetter, mustMoveFrom):
    # Create a list of all valid moves:
    #rand = random.seed(1543)
    moveList = []
    moveList = createMoveList(board, computerLetter, mustMoveFrom)
    
    # Each time a computer player makes a move, the event queue is checked for input.
    # If a person tries to exit, this allows them to.
    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          terminate()
    
    return random.choice(moveList)

# AIKings is very similar to AIRandom, except that it will always try to create a king
#  is possible.
def AIKings(board, computerLetter, mustMoveFrom):
    # Create a list of all valid moves:
    #rand = random.seed(1543)
    moveList = []
    moveList = createMoveList(board, computerLetter, mustMoveFrom)
    # dupeMoveList duplicated moveList to create a second list where non-preferencial
    # moves are discarded.
    dupeMoveList = list(moveList)
    
    i = len(moveList)
    # Runs through the loop a number of times equal to the length of the possible move list.
    while i:
      move = dupeMoveList[i-1]
      moveTo = move[1]
      moveFrom = move[0]
      # If a move does not involve a piece becoming a king, it is discarded from dupeMoveList.
      if (computerLetter == 'x' and moveTo>18) or board[moveFrom] == 'X':
        dupeMoveList.pop(i-1)
      if (computerLetter == 'o' and 81>moveTo) or board[moveFrom] == 'O':
        dupeMoveList.pop(i-1)
      i = i-1
    
    # Each time a computer player makes a move, the event queue is checked for input.
    # If a person tries to exit, this allows them to.
    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          terminate()
    
    # If a move, or moves exists that would create a king, those are given preference.
    # Otherwise a random move is chosen.
    if dupeMoveList:
      return random.choice(dupeMoveList)
    else:
      return random.choice(moveList)

# AIAvoid does what AIKings does, expect it will not put a piece in a position where
# it can be captured is at all possible.
def AIAvoid(board, computerLetter, mustMoveFrom):

    moveList = []
    moveList = createMoveList(board, computerLetter, mustMoveFrom)
    # Two duplicate move lists are created.
    # avoidMoveList is the list of moves where a piece does not move into a position where
    # it can be captured.
    avoidMoveList = list(moveList)
    # kingMoveList is the list of moves where pieces can become kings.
    kingMoveList = list(moveList)
    
    
    i = len(moveList)
    # Runs through the loop a number of times equal to the length of the possible move list.
    while i:
        move = moveList[i-1]
        moveTo = move[1]
        moveFrom = move[0]
      #Avoid
        # Checks each move such that if the piece moves into a position where it can be captured,
        # then that move is discarded from avoidMoveList.
        if moveTo-9>11 and moveFrom+2<89 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-11 and board[moveTo-9].lower() == 'o' and board[moveFrom+2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-11>11 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-9 and board[moveTo-11].lower() == 'o' and board[moveFrom-2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+9<89 and moveFrom+2<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==11 and board[moveTo+9].lower() == 'x' and board[moveFrom+2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+11<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==9 and board[moveTo+11].lower() == 'x' and board[moveFrom-2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-9>11 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-9 and board[moveTo-9].lower() == 'o':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-11>11 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-11 and board[moveTo-11].lower() == 'o':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+9<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==9 and board[moveTo+9].lower() == 'x':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+11<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==11 and board[moveTo+11].lower() == 'x':
          avoidMoveList.pop(i-1)
          i = i-1
        #Worry about Kings
        elif moveTo-9>11 and moveFrom+2<89 and board[moveFrom].lower() == 'x' and board[moveTo-9] == ' ' and board[moveFrom+2] == 'O':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-11>11 and board[moveFrom].lower() == 'x' and board[moveTo-11] == ' ' and board[moveFrom-2] == 'O':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+9<89 and board[moveFrom].lower() == 'o' and board[moveTo+9] == ' ' and board[moveFrom-2] == 'X':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+11<89 and moveFrom+2<89 and board[moveFrom].lower() == 'o' and board[moveTo+11] == ' ' and board[moveFrom+2] == 'X':
          avoidMoveList.pop(i-1)
          i = i-1
        else:
          i = i-1
    
    # Same as AIKings.
    i = len(moveList)  
    while i:        
        move = moveList[i-1]
        moveTo = move[1]
        moveFrom = move[0]
      #Kings
        if (computerLetter == 'x' and moveTo>18) or board[moveFrom] == 'X':
          kingMoveList.pop(i-1)
          i = i-1
        elif (computerLetter == 'o' and moveTo<81):
          kingMoveList.pop(i-1)
          i = i-1
        else:
          i = i-1
          
    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          terminate()
    
    # Preference given to creating a king, then avoiding capture, then random move.
    if kingMoveList:
      return random.choice(kingMoveList)
    elif avoidMoveList:
      return random.choice(avoidMoveList)
    else:
      return random.choice(moveList)
     
# AIAvoidBackLine adds to AIAvoid by doing everything AIAvoid does, plus it tries to avoid
# moving pieces from it's backline is at all possible.
def AIAvoidBackLine(board, computerLetter, mustMoveFrom):

    moveList = []
    moveList = createMoveList(board, computerLetter, mustMoveFrom)
    avoidMoveList = list(moveList)
    kingMoveList = list(moveList)
    
    i = len(moveList)
    while i:
        move = moveList[i-1]
        moveTo = move[1]
        moveFrom = move[0]
      #AvoidBackLine
        # Only difference between AIAvoid, and AIAvoidBackLine
        # If the move originates at player's backline, that move is discarded.
        if board[moveFrom] == 'x' and moveFrom>80:
          avoidMoveList.pop(i-1)
          i = i-1
        elif board[moveFrom] == 'o' and moveFrom<20:
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-9>11 and moveFrom+2<89 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-11 and board[moveTo-9].lower() == 'o' and board[moveFrom+2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-11>11 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-9 and board[moveTo-11].lower() == 'o' and board[moveFrom-2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+9<89 and moveFrom+2<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==11 and board[moveTo+9].lower() == 'x' and board[moveFrom+2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+11<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==9 and board[moveTo+11].lower() == 'x' and board[moveFrom-2] == ' ':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-9>11 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-9 and board[moveTo-9].lower() == 'o':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-11>11 and board[moveFrom].lower() == 'x' and moveTo-moveFrom==-11 and board[moveTo-11].lower() == 'o':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+9<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==9 and board[moveTo+9].lower() == 'x':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+11<89 and board[moveFrom].lower() == 'o' and moveTo-moveFrom==11 and board[moveTo+11].lower() == 'x':
          avoidMoveList.pop(i-1)
          i = i-1
        #Worry about Kings
        elif moveTo-9>11 and moveFrom+2<89 and board[moveFrom].lower() == 'x' and board[moveTo-9] == ' ' and board[moveFrom+2] == 'O':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo-11>11 and board[moveFrom].lower() == 'x' and board[moveTo-11] == ' ' and board[moveFrom-2] == 'O':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+9<89 and board[moveFrom].lower() == 'o' and board[moveTo+9] == ' ' and board[moveFrom-2] == 'X':
          avoidMoveList.pop(i-1)
          i = i-1
        elif moveTo+11<89 and moveFrom+2<89 and board[moveFrom].lower() == 'o' and board[moveTo+11] == ' ' and board[moveFrom+2] == 'X':
          avoidMoveList.pop(i-1)
          i = i-1
        else:
          i = i-1
    
    i = len(moveList)  
    while i:        
        move = moveList[i-1]
        moveTo = move[1]
        moveFrom = move[0]
      #Kings
        if (computerLetter == 'x' and moveTo>18) or board[moveFrom] == 'X':
          kingMoveList.pop(i-1)
          i = i-1
        elif (computerLetter == 'o' and moveTo<81):
          kingMoveList.pop(i-1)
          i = i-1
        else:
          i = i-1
          
    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          terminate()
    
    if kingMoveList:
      return random.choice(kingMoveList)
    elif avoidMoveList:
      return random.choice(avoidMoveList)
    else:
      return random.choice(moveList)