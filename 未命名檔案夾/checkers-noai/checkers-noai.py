from pygame import *
import random

board = [
		[0,1,0,1,0,1,0,1],
		[1,0,1,0,1,0,1,0],
		[0,1,0,1,0,1,0,1],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[2,0,2,0,2,0,2,0],
		[0,2,0,2,0,2,0,2],
		[2,0,2,0,2,0,2,0]
		]

PLAYERTURN,CPUTURN=1,0
SIGN,PIECE,valid_move,numpiece=[-1,1],[[1,3],[2,4]],[],[12,12]
normalmove,kingmove=[(-1,-1),(1,-1)],[(-1,-1),(1,-1),(-1,1),(1,1)]
running,over,picking,turn = True,False,False,PLAYERTURN
c1,c2,c3=(153,255,102),(0,102,0),(102,204,51)

init()
display.init()
display.set_caption("PyCheckers")
display.set_icon(image.load("logo.png"))
screen = display.set_mode((288,256), HWSURFACE|DOUBLEBUF)
clock=time.Clock()
boardimg=surface.Surface((256,256))

#create board surface
boardimg.fill(c1)
for y in range(0,8):
	for x in range(0,4):
		if y % 2 == 0:
			draw.rect(boardimg, c2, Rect(32*(x*2+1), 32*y, 32, 32))
		else:
			draw.rect(boardimg, c2, Rect(32*(x*2), 32*y, 32, 32))

#create pieces
pieces = [surface.Surface((32,32)),surface.Surface((32,32)),surface.Surface((32,32)),surface.Surface((32,32))]
for p in pieces:
	p.fill((255,0,255))
	p.set_colorkey((255,0,255))
draw.circle(pieces[0], (255,255,255), (16,16), 15)
draw.circle(pieces[1], (255,121,75), (16,16), 15)
draw.circle(pieces[2], (255,255,255), (16,16), 15)
draw.circle(pieces[3], (255,121,75), (16,16), 15)
draw.circle(pieces[2], (255,204,0), (16,16), 10)
draw.circle(pieces[3], (255,255,121), (16,16), 10)

#INFO
fnt=font.Font(None, 48)
winner=[fnt.render("CPU Win", 1, (255,0,0)),fnt.render("Player Win", 1, (0,0,255))]

def get_opposite(turn):
	if turn==PLAYERTURN:
		return CPUTURN
	else:
		return PLAYERTURN
		
def get_valid_move(x,y,turn):
	result = []
	opposite=get_opposite(turn)
	moverule=normalmove
	if board[y][x]>2:
		moverule=kingmove
	for n in moverule:
		dx,dy=n[0]+x,n[1]*SIGN[turn]+y
		if (dx>=0) and (dx<=7) and (dy>=0) and (dy<=7):
			if board[dy][dx]==0:
				result += [(dx,dy)]
			elif board[dy][dx] in PIECE[opposite]:#jump
				ex,ey=n[0]+dx,n[1]*SIGN[turn]+dy
				if (ex>=0) and (ex<=7) and (ey>=0) and (ey<=7) and board[ey][ex]==0:
					result += [(ex,ey)]
	return result
	
def no_more_move(turn):
	for y in range(0,8):
		for x in range(0,8):
			if board[y][x] in PIECE[turn]:
				if len(get_valid_move(x,y,turn)):
					return False
	return True
	
def switch_turn():
	global turn
	if turn==PLAYERTURN:
		turn=CPUTURN
	else:
		turn=PLAYERTURN
		
def pick(px,py,cx,cy,turn):
	result = []
	board[cy][cx] = board[py][px]
	board[py][px] = 0
	if abs(cx-px)>1:#jump
		board[(py+cy)/2][(px+cx)/2] = 0
		numpiece[get_opposite(turn)]-=1
		if numpiece[get_opposite(turn)]==0:
			over=True
			return []
		tmp = get_valid_move(cx,cy, turn)
		for j in tmp:
			if abs(j[0]-cx)>1:
				px,py=cx,cy
				result = tmp
				break
	if cy in [0,7] and (board[cy][cx]<3):
		board[cy][cx]+=2
	return result

while running:
	clock.tick(20)
	screen.fill((102,102,102))
	screen.blit(boardimg, (0, 0))
	screen.blit(pieces[turn], (256, 0))
	if picking:
		for v in valid_move:
			draw.rect(screen, c3, Rect(32*v[0], 32*v[1], 32, 32))
	for y in range(0,8):
		for x in range(0,8):
			if board[y][x]>0:
				screen.blit(pieces[(board[y][x])-1], (32*x, 32*y))
	for e in event.get():
		if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
			running = False
			break
		if not over and e.type == MOUSEBUTTONDOWN:
			cx,cy=e.pos[0]/32,e.pos[1]/32
			if cx in range(0,8) and cy in range(0,8):
				if board[cy][cx]>0 and board[cy][cx] in PIECE[turn]:
					if not picking:
						picking = True
					px,py=cx,cy
					valid_move = get_valid_move(px,py,turn)
					if no_more_move(turn):
						over = True
						switch_turn()
				elif picking and board[cy][cx]==0 and (cx,cy) in valid_move:
					picking = False
					board[cy][cx] = board[py][px]
					board[py][px] = 0
					
					if abs(cx-px)>1:#jump
						board[(py+cy)/2][(px+cx)/2] = 0
						numpiece[get_opposite(turn)]-=1
						if numpiece[get_opposite(turn)]==0:
							over=True
							break
						tmp = get_valid_move(cx,cy, turn)
						for j in tmp:
							if abs(j[0]-cx)>1:
								px,py=cx,cy
								valid_move = tmp
								picking=True
								break
					if cy in [0,7] and (board[cy][cx]<3):
						board[cy][cx]+=2
					if not picking:
						switch_turn()
	if over:
		screen.blit(winner[turn], ((screen.get_width()-winner[turn].get_width())/2,(screen.get_height()-winner[turn].get_height())/2))
	display.update()