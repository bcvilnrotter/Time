import pygame, sys, math, random, cProfile
from knickknack import *
from pieces import *
from activitylist import *
from pygame.locals import *

class enemy_team:
	def __init__(self):
		self.enemylist = []
		self.turntimer = None
		self.timetotal = 0
	def establishteam(self):
		#self.enemylist.append(enemy_queen())
		#self.enemylist[0].j = 0
		#self.enemylist[0].k = 3

		# add enemy types to a list for placement
		enemy_type_list = []
		enemy_type_list.append(enemy_pawn)
		#enemy_type_list.append(tank)
		print(enemy_type_list)

		for i in range (5):
		  self.enemylist.append(random.choice(enemy_type_list)())
		  self.enemylist[i].j = random.randint(0,7)
		  self.enemylist[i].k = random.randint(0,7)
		print(self.enemylist)
	def deletemember(self, piece):
		self.enemylist.pop(piece)
  
#==========================================================
# STATES
#==========================================================

def createplayerstate():
  return joker()

def createenemystate():
  return enemy_team()

def createmovementsets(player):
  return player

#============================================
# FONT DEFINITIONS
#============================================

def drawfont():
  fontObj = pygame.font.Font('freesansbold.ttf', 32)
  textSurfaceObj = fontObj.render('Hello World!', True, BLACK, WHITE)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = (200, 150)
  DISPLAYSURF.blit(textSurfaceObj, textRectObj)

#============================================
# BOARD DEFINITIONS
#============================================

def tilereset(board, boardtype):
  for i in range(BOARDDEPTH):
    for j in range (BOARDWIDTH):
      for k in range (BOARDHEIGHT):
        if boardtype == 'grassy_plains':
          board[i][j][k].image = hexGrassyIMG_0
        else:
          board[i][j][k].image = tileIMG_0
  return board

def highlightpos(board, x, y):
  for i in range (BOARDDEPTH):
    for j in range (BOARDWIDTH):
      for k in range (BOARDHEIGHT):
        if x > board[i][j][k].ltposx + 6 and x < board[i][j][k].ltposx + board[i][j][k].pixlength - 6:
          if y > board[i][j][k].ltposy + 6 and y < board[i][j][k].ltposy + board[i][j][k].pixwidth - 3:
            board[i][j][k].image = tileHI_0
  return board

def createboardstate():
  board = []
  for i in range (BOARDDEPTH):
    layer = []
    for j in range (BOARDWIDTH):
      surface = []
      for k in range (BOARDHEIGHT):
        space = tile()
        space.i = i
        space.j = j
        space.k = k
        rise = space.rise
        run = space.run
        height = space.height
        space.ltposx = 225 + rise*(k) - rise*j
        space.ltposy = 180 + run*(k) + (run*j - height*i)
        if i != BOARDDEPTH-1:
          space.inactivate()
        surface.append(space)
      layer.append(surface)
    board.append(layer)
  return board

#======================================================================
# PLAYER MOVELISTS
#======================================================================

def showknightmovement(board, player, enemy):
  j = player.j
  k = player.k
  for i in range (BOARDDEPTH):
    if player.istaken == 0:
        if j-2 >= 0 and k-1 >= 0:
          if board [i][j-2][k-1].active == 1:
            board[i][j-2][k-1].image = tileOP_0
            player.movelist.append(board[i][j-2][k-1])
        if j+2 < 8 and k-1 >= 0:
          if board [i][j+2][k-1].active == 1:
            board[i][j+2][k-1].image = tileOP_0
            player.movelist.append(board[i][j+2][k-1])
        if j+2 < 8 and k+1 < 8:
          if board [i][j+2][k+1].active == 1:
            board[i][j+2][k+1].image = tileOP_0
            player.movelist.append(board[i][j+2][k+1])
        if j-2 >= 0 and k+1 < 8:
          if board [i][j-2][k+1].active == 1:
            board[i][j-2][k+1].image = tileOP_0
            player.movelist.append(board[i][j-2][k+1])
        if j-1 >= 0 and k-2 >= 0:
          if board [i][j-1][k-2].active == 1:
            board[i][j-1][k-2].image = tileOP_0
            player.movelist.append(board[i][j-1][k-2])
        if j+1 < 8 and k-2 >= 0:
          if board [i][j+1][k-2].active == 1:
            board[i][j+1][k-2].image = tileOP_0
            player.movelist.append(board[i][j+1][k-2])
        if j+1 < 8 and k+2 < 8:
          if board [i][j+1][k+2].active == 1:
            board[i][j+1][k+2].image = tileOP_0
            player.movelist.append(board[i][j+1][k+2])
        if j-1 >= 0 and k+2 < 8:
          if board [i][j-1][k+2].active == 1:
            board[i][j-1][k+2].image = tileOP_0
            player.movelist.append(board[i][j-1][k+2])
  return board, player
    

def showbishopmovement(board, player, enemy):
  j = player.j
  k = player.k
  for i in range (BOARDDEPTH):
    if player.istaken == 0:
      player.cansee = 1
      for move in range (1,8):
        if j-move >= 0 and k+move < 8 and player.cansee == 1:
            if board[i][j-move][k+move].active == 1 and player.cansee == 1: 
              board[i][j-move][k+move].image = tileOP_0
              player.movelist.append(board[i][j-move][k+move])
              for e in range (len(enemy.enemylist)):
                if j-move == enemy.enemylist[e].j and k+move == enemy.enemylist[e].k:
                  player.cansee = 0
      player.cansee = 1            
      for move in range (1,8):            
        if k-move >= 0 and player.cansee == 1:
            if board[i][j][k-move].active == 1:
               board[i][j][k-move].image = tileOP_0
               player.movelist.append(board[i][j][k-move])
               for e in range (len(enemy.enemylist)):
                if j == enemy.enemylist[e].j and k-move == enemy.enemylist[e].k:
                  player.cansee = 0
      player.cansee = 1
      for move in range (1,8):
        if j+move < 8 and player.cansee == 1:
            if board[i][j+move][k].active == 1:
               board[i][j+move][k].image = tileOP_0
               player.movelist.append(board[i][j+move][k])
               for e in range (len(enemy.enemylist)):
                if j+move == enemy.enemylist[e].j and k == enemy.enemylist[e].k:
                  player.cansee = 0
      #player.cansee = 1         
      #for move in range (1,8):         
      #  if j+move < 8 and k-move >= 0 and player.cansee == 1:
      #    if board[i][j+move][k-move].active == 1:
      #       board[i][j+move][k-move].image = tileOP_0
      #       player.bishopmovelist.append(board[i][j+move][k-move])
      #       for e in range (len(enemy.enemylist)):
      #          if j+move == enemy.enemylist[e].j and k-move == enemy.enemylist[e].k:
      #            player.cansee = 0
  return board, player

def showreversebishopmovement(board, player, enemy):
  j = player.j
  k = player.k
  for i in range (BOARDDEPTH):
    if player.istaken == 0:
      player.cansee = 1
      for move in range (1,8):
        if j+move < 8 and k-move >= 0 and player.cansee == 1:
            if board[i][j+move][k-move].active == 1 and player.cansee == 1: 
              board[i][j+move][k-move].image = tileOP_0
              player.movelist.append(board[i][j+move][k-move])
              for e in range (len(enemy.enemylist)):
                if j+move == enemy.enemylist[e].j and k-move == enemy.enemylist[e].k:
                  player.cansee = 0
      player.cansee = 1            
      for move in range (1,8):            
        if k+move < 8 and player.cansee == 1:
            if board[i][j][k+move].active == 1:
               board[i][j][k+move].image = tileOP_0
               player.movelist.append(board[i][j][k+move])
               for e in range (len(enemy.enemylist)):
                if j == enemy.enemylist[e].j and k+move == enemy.enemylist[e].k:
                  player.cansee = 0
      player.cansee = 1
      for move in range (1,8):
        if j-move >= 0 and player.cansee == 1:
            if board[i][j-move][k].active == 1:
               board[i][j-move][k].image = tileOP_0
               player.movelist.append(board[i][j-move][k])
               for e in range (len(enemy.enemylist)):
                if j-move == enemy.enemylist[e].j and k == enemy.enemylist[e].k:
                  player.cansee = 0
      #player.cansee = 1         
      #for move in range (1,8):         
      #  if j+move < 8 and k-move >= 0 and player.cansee == 1:
      #    if board[i][j+move][k-move].active == 1:
      #       board[i][j+move][k-move].image = tileOP_0
      #       player.bishopmovelist.append(board[i][j+move][k-move])
      #       for e in range (len(enemy.enemylist)):
      #          if j+move == enemy.enemylist[e].j and k-move == enemy.enemylist[e].k:
      #            player.cansee = 0
  player.cansee = 1
  return board, player

def showplayermovelists(board, player, enemy):
    #board, player = showknightmovement(board, player, enemy)
    board, player = showbishopmovement(board, player, enemy)
    board, player = showreversebishopmovement(board, player, enemy)
    return board, player, enemy

#===================================================
# PLAY DEFINITIONS
#===================================================
  
def checkforwin(player, enemy):
  if len(enemy.enemylist) == 0:
    player.haswon = 1
  return player

def checktake(player, enemy):
  if player.istaken == 0:
    for piece in range (len(enemy.enemylist)):
      if player.j == enemy.enemylist[piece].j and player.k == enemy.enemylist[piece].k:
        if player.isturn == 1:
          enemy.enemylist[piece].istaken = 1
          player.holdlist.append(enemy.enemylist[piece].type)
          enemy.deletemember(piece)
          return player, enemy
        elif player.isturn == 0:
          player.holdlist.append(10)
          player.istaken = 1
          return player, enemy
    return player, enemy
            
def playertakeactionatpos(board, player, enemy, x, y):
  for i in range (BOARDDEPTH):
    for j in range (BOARDWIDTH):
      for k in range (BOARDHEIGHT):
        if player.isturn == 1:
          if x > board[i][j][k].ltposx + 6 and x < board[i][j][k].ltposx + board[i][j][k].pixlength - 6:
            if y > board[i][j][k].ltposy + 6 and y < board[i][j][k].ltposy + board[i][j][k].pixwidth - 3:
              for move in range (len(player.movelist)):
                if board[i][j][k].i == player.movelist[move].i:
                  if board[i][j][k].j == player.movelist[move].j and board[i][j][k].k == player.movelist[move].k:
                    player.i = i
                    player.j = j
                    player.k = k
                    #board = attackboard(board, player.i, player.j, player.k, 8)                    
                    player, enemy = checktake(player, enemy)
                    player.isturn = 0
                    player.turntimer.checktimer()
                    player.timetotal = player.turntimer.timeelapsed + player.timetotal
                    player.turntimer = None
                    enemy.turntimer = settimer()
                    player.enemypausetimer = settimer()
                    return board, player, enemy
              #for move in range (len(player.bishopmovelist)):
              #  if board[i][j][k].i == player.bishopmovelist[move].i:
              #    if board[i][j][k].j == player.bishopmovelist[move].j and board[i][j][k].k == player.bishopmovelist[move].k:
              #      player.i = i
              #      player.j = j
              #      player.k = k
              #      player, enemy = checktake(player, enemy)
              #      player.isturn = 0
              #      player.turntimer.checktimer()
              #      player.timetotal = player.turntimer.timeelapsed + player.timetotal
              #      player.turntimer = None
              #      enemy.turntimer = settimer()
              #      player.enemypausetimer = settimer()
              #      return board, player, enemy
  return board, player, enemy

def playertakeactionathand(player, x, y):
  for move in range (len(player.handlist)): 
    if move == len(player.handlist):
      if x > player.handlist[move].ltposx and x < player.handlist[move].ltposx + player.handlist[move].run:
        if y > player.handlist[move].lyposy and y < player.handlist[move].ltposy + player.handlist[move].rise:
          player.handlist[move].ltposy = player.handlist[move].ltposy - player.handlist[move].rise
          pygame.transform.scale2x(player.handlist[move].image)
          return player
    else:
      if x > player.handlist[move].ltposx and x < player.handlist[move].ltposx + player.handlist[move].ltposx:
        if y > player.handlist[move].ltposy and y < player.handlist[move].ltposy + player.handlist[move].rise:
          player.handlist[move].ltposy = player.handlist[move].ltposy - player.handlist[move].rise
          player.handlist[move].image = pygame.transform.scale2x(player.handlist[move].image)
          return player
  return player

def enemymove(player, enemy):
  if enemy.enemylist:
    if player.isturn == 0:
      player.enemypausetimer.checktimer()
      if player.enemypausetimer.timeelapsed >= 1250:
        for index in range (len(enemy.enemylist)):
          if player.j == enemy.enemylist[index].j and player.k - 1 == enemy.enemylist[index].k or player.j - 1 == enemy.enemylist[index].j and player.k + 1 == enemy.enemylist[index].k:
            enemy.enemylist[index].j = player.j
            enemy.enemylist[index].k = player.k
            checktake(player, enemy)
            player.isturn = 1
            player.turntimer = settimer()
            enemy.turntimer.checktimer()
            enemy.timetotal = enemy.turntimer.timeelapsed + enemy.timetotal
            player.enemypausetimer = None
            enemy.turntimer = None
            return player, enemy
        if len(enemy.enemylist) > 0:
          rand = random.randrange(0, (len(enemy.enemylist)))
          if enemy.enemylist[rand].j <= BOARDWIDTH - 2 and enemy.enemylist[rand].j + 1 != player.j and enemy.enemylist[rand].k != player.k:
            if enemy.enemylist[rand].type == 1:
              enemy.enemylist[rand].j = enemy.enemylist[rand].j + 1
              player.isturn = 1
              player.turntimer = settimer()
              enemy.turntimer.checktimer()
              enemy.timetotal = enemy.turntimer.timeelapsed + enemy.timetotal
              player.enemypausetimer = None
              enemy.turntimer = None
            #elif enemy.enemylist[rand].type == 2:
              #
            return player, enemy
        elif len(enemy.enemylist) == 0:
          enemy.enemylist[0].j = enemy.enemylist[0].j + 1
          changetoplayerturn(player, enemy)
          return player, enemy
      if player.enemypausetimer.timeelapsed >= 12500:
        changetoplayerturn(player, enemy)
        return player, enemy
  enemy = checktransform(enemy)
  return player, enemy

def changetoplayerturn (player, enemy):
  player.isturn = 1
  player.turntimer = settimer()
  enemy.turntimer.checktimer()
  enemy.total = enemy.turntimer.timeelapsed + enemy.timetotal
  player.enemypausetimer = None
  enemy.turntimer = None
  return player, enemy

def checktransform (enemy):
  for i in range (len(enemy.enemylist)):
    if enemy.enemylist[i].j == 7:
      add = enemy_queen()
      add.i = enemy.enemylist[i].i
      add.j = enemy.enemylist[i].j
      add.k = enemy.enemylist[i].k
      del enemy.enemylist [i]
      enemy.enemylist.insert(i, add)
  return enemy       

def updateplayerdepth(board, player):
  i = player.i
  j = player.j
  k = player.k
  if board[i][j][k].active == 0:
    for new in range (BOARDDEPTH):
      if board[new][j][k].active == 1:
        player.i = new
  return player

def updateenemydepth(board, enemy):
  for index in range (len(enemy.enemylist)):
    i = enemy.enemylist[index].i
    j = enemy.enemylist[index].j
    k = enemy.enemylist[index].k
    if board[i][j][k].active == 0:
      for new in range (BOARDDEPTH):
       if board[new][j][k].active == 1:
          enemy.enemylist[index].i = new
  return enemy

def attackboard(board, i, j, k, limit):
  if board[i][j][k].active == 1 and i-2 > 0:
    board[i][j][k].active = 0
    board[i-1][j][k].active = 1
    if k-1 < limit and i-1 > 0 and k-1 > 0:
      if board[i][j][k-1].active == 1:
        board[i][j][k-1].active = 0
        board[i-1][j][k-1].active = 1
    if k+1 < limit and i-1 > 0:
      if board[i][j][k+1].active == 1:
        board[i][j][k+1].active = 0
        board[i-1][j][k+1].active = 1
    if j-1 < limit and i-1 > 0 and j-1 > 0:
      if board[i][j-1][k].active == 1:
        board[i][j-1][k].active = 0
        board[i-1][j-1][k].active = 1
    if j+1 < limit and i-1 > 0:
      if board[i][j+1][k].active == 1:
        board[i][j+1][k].active = 0
        board[i-1][j+1][k].active = 1
  return board

#==================================================================
# MISC.
#==================================================================

def randomizeboardactivity(board):
  for i in range (BOARDDEPTH):
    for j in range (BOARDWIDTH):
      for k in range (BOARDHEIGHT):
        board[i][j][k].active = random.choice([0,1])
  return board

#==================================================================
# DRAW DEFINITIONS
#==================================================================

def drawboard(board):
  
  #if growTimer <= 2000:
  #  DISPLAYSURF.blit(tileIMG_0, (x - (22*i), y + (6*i)))
  #elif growTimer > 2000 and growTimer <= 6000:
  #  DISPLAYSURF.blit(tileIMG_1, (x - (22*i), y + (6*i)))
  #elif growTimer > 6000 and growTimer <= 14000:
  #  DISPLAYSURF.blit(tileIMG_2, (x - (22*i), y + (6*i)))
  #elif growTimer > 14000:
  #  DISPLAYSURF.blit(tileIMG_3, (x - (22*i), y + (6*i)))
  activitylist = createactivitylist(board)
  activitylist = sortheightactivitylist(activitylist)
  for i in range (ACTIVELIST):
    DISPLAYSURF.blit(player_hold_bar, (0, 25))
    DISPLAYSURF.blit(player_hold_bar, (0, 425))
    DISPLAYSURF.blit(activitylist[i].image, (activitylist[i].ltposx, activitylist[i].ltposy))

def drawpieces(player, enemy, board):
  for i in range (BOARDDEPTH):
    for j in range (BOARDWIDTH):
      for k in range (BOARDHEIGHT):
        for piece in range (len(enemy.enemylist)):
          if enemy.enemylist[piece].istaken == 0: 
            if enemy.enemylist[piece].i == i and enemy.enemylist[piece].j == j and enemy.enemylist[piece].k == k:
              x = board[i][j][k].ltposx + 16
              y = board[i][j][k].ltposy - enemy.enemylist[piece].height
              DISPLAYSURF.blit(enemy.enemylist[piece].image, (x, y))
        if player.istaken == 0:
          if player.i == i and player.j == j and player.k == k:
            x = board[i][j][k].ltposx + 14
            y = board[i][j][k].ltposy - player.height
            DISPLAYSURF.blit(player.image, (x, y))
  player.clearmovelist()

def drawhold(player):
  for i in range (len(player.holdlist)):
    if  player.holdlist[i] == 1:
      DISPLAYSURF.blit(enemy_pawn_IMG, (10 + 35*i, 20))
    elif player.holdlist[i] == 2:
      DISPLAYSURF.blit(enemy_queen_IMG, (10 + 35*i, 15))
    elif player.holdlist[i] == 10:
      DISPLAYSURF.blit(joker_IMG, (10 + 35*i, 20))

def drawhand(player):
  for i in range (len(player.handlist)):
    if  player.handlist[i].card_id == 1:
      DISPLAYSURF.blit(player.handlist[i].image, (player.handlist[i].ltposx, player.handlist[i].ltposy))

def drawturn(player, enemy):
  if player.haswon == 1:
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('Clear!', True, BLACK, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, 100)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
  elif player.isturn == 0:
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('Opponent', True, BLACK, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, 100)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
  elif player.isturn == 1:
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('Player', True, BLACK, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, 100)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
  elif player.istaken == 1:
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('Loss!', True, BLACK, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, 100)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawtime(player, enemy):
  nullvalue = 0
  
  if player.istaken == 1:
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    textSurfaceObjPlayerTurn = fontObj.render('%20d s.' % (nullvalue), True, BLACK, WHITE)
    textSurfaceObjPlayerTotal = fontObj.render('%20d s.' % (player.timetotal/1000), True, BLACK, WHITE)
    textSurfaceObjEnemyTurn = fontObj.render('%20d s.' % (nullvalue), True, BLACK, WHITE)
    textSurfaceObjEnemyTotal = fontObj.render('%20d s.' % (enemy.timetotal/1000), True, BLACK, WHITE)
    
    textRectObjPlayerTurn = textSurfaceObjPlayerTurn.get_rect()
    textRectObjPlayerTotal = textSurfaceObjPlayerTotal.get_rect()
    textRectObjEnemyTurn = textSurfaceObjEnemyTurn.get_rect()
    textRectObjEnemyTotal = textSurfaceObjEnemyTotal.get_rect()
    
    textRectObjPlayerTurn.center = (100, 105)
    textRectObjPlayerTotal.center = (100, 85)
    textRectObjEnemyTurn.center = (325, 105)
    textRectObjEnemyTotal.center = (325, 85)
    
    DISPLAYSURF.blit(textSurfaceObjPlayerTurn, textRectObjPlayerTurn)
    DISPLAYSURF.blit(textSurfaceObjPlayerTotal, textRectObjPlayerTotal)
    DISPLAYSURF.blit(textSurfaceObjEnemyTurn, textRectObjEnemyTurn)
    DISPLAYSURF.blit(textSurfaceObjEnemyTotal, textRectObjEnemyTotal)
    
  elif player.turntimer:
    
    player.turntimer.checktimer()
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    textSurfaceObjPlayerTurn = fontObj.render('%20d s.' % (player.turntimer.timeelapsed/1000), True, BLACK, WHITE)
    textSurfaceObjPlayerTotal = fontObj.render('%20d s.' % (player.timetotal/1000), True, BLACK, WHITE)
    textSurfaceObjEnemyTurn = fontObj.render('%20d s.' % (nullvalue), True, BLACK, WHITE)
    textSurfaceObjEnemyTotal = fontObj.render('%20d s.' % (enemy.timetotal/1000), True, BLACK, WHITE)
    
    textRectObjPlayerTurn = textSurfaceObjPlayerTurn.get_rect()
    textRectObjPlayerTotal = textSurfaceObjPlayerTotal.get_rect()
    textRectObjEnemyTurn = textSurfaceObjEnemyTurn.get_rect()
    textRectObjEnemyTotal = textSurfaceObjEnemyTotal.get_rect()
    
    textRectObjPlayerTurn.center = (100, 105)
    textRectObjPlayerTotal.center = (100, 85)
    textRectObjEnemyTurn.center = (325, 105)
    textRectObjEnemyTotal.center = (325, 85)
    
    DISPLAYSURF.blit(textSurfaceObjPlayerTurn, textRectObjPlayerTurn)
    DISPLAYSURF.blit(textSurfaceObjPlayerTotal, textRectObjPlayerTotal)
    DISPLAYSURF.blit(textSurfaceObjEnemyTurn, textRectObjEnemyTurn)
    DISPLAYSURF.blit(textSurfaceObjEnemyTotal, textRectObjEnemyTotal)
    
  elif enemy.turntimer and player.isturn == 0:
    
    enemy.turntimer.checktimer()
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    textSurfaceObjPlayerTurn = fontObj.render('%20d s.' % (nullvalue), True, BLACK, WHITE)
    textSurfaceObjPlayerTotal = fontObj.render('%20d s.' % (player.timetotal/1000), True, BLACK, WHITE)
    textSurfaceObjEnemyTurn = fontObj.render('%20d s.' % (enemy.turntimer.timeelapsed/1000), True, BLACK, WHITE)
    textSurfaceObjEnemyTotal = fontObj.render('%20d s.' % (enemy.timetotal/1000), True, BLACK, WHITE)
    
    textRectObjPlayerTurn = textSurfaceObjPlayerTurn.get_rect()
    textRectObjPlayerTotal = textSurfaceObjPlayerTotal.get_rect()
    textRectObjEnemyTurn = textSurfaceObjEnemyTurn.get_rect()
    textRectObjEnemyTotal = textSurfaceObjEnemyTotal.get_rect()
    
    textRectObjPlayerTurn.center = (100, 105)
    textRectObjPlayerTotal.center = (100, 85)
    textRectObjEnemyTurn.center = (325, 105)
    textRectObjEnemyTotal.center = (325, 85)
    
    DISPLAYSURF.blit(textSurfaceObjPlayerTurn, textRectObjPlayerTurn)
    DISPLAYSURF.blit(textSurfaceObjPlayerTotal, textRectObjPlayerTotal)
    DISPLAYSURF.blit(textSurfaceObjEnemyTurn, textRectObjEnemyTurn)
    DISPLAYSURF.blit(textSurfaceObjEnemyTotal, textRectObjEnemyTotal)

#============================================================
# INITIALIZING
#============================================================
FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((500, 500))
time = pygame.time.Clock()

def __main__():
  mousex = 0
  mousey = 0

  pygame.display.set_caption('time')
  player = createplayerstate()
  board = createboardstate()
  enemy_team = createenemystate()
  enemy_team.establishteam()
  player.setuphand(7)
  
  while True:
    pygame.font.init()
    growTimer = pygame.time.get_ticks()
    DISPLAYSURF.fill(WHITE)
    boardtype = 'grassy_plains'
    board = tilereset(board, boardtype)
    player.resethand()
    player = updateplayerdepth(board, player)
    enemy_team = updateenemydepth (board, enemy_team)
    showplayermovelists(board, player, enemy_team)

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEMOTION:
        mousex, mousey = event.pos
      elif event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        #player = playertakeactionathand(player, mousex, mousey)
        board, player, enemy_team = playertakeactionatpos(board, player, enemy_team, mousex, mousey)

    player = checkforwin(player, enemy_team)
    player = playertakeactionathand(player, mousex, mousey)
    player, enemy_team = enemymove(player, enemy_team)
    board = highlightpos(board, mousex, mousey)
    drawboard(board)
    #for i in range (BOARDDEPTH):
    #  for j in range (BOARDWIDTH):
    #    for k in range (BOARDHEIGHT):
    #      if player.i == i and player.j == j and player.k == k:
    #        x = board[i][j][k].ltposx + 35
    #        y = board[i][j][k].ltposy - player.height
    #        DISPLAYSURF.blit(player.image, (x, y))
    drawpieces(player, enemy_team, board)
    drawhold(player)
    drawhand(player)
    drawtime(player, enemy_team)
    drawturn(player, enemy_team)
    pygame.display.update()
    fpsClock.tick(FPS)

cProfile.run('__main__()')
__main__()
