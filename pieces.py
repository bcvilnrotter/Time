import pygame
from pygame.locals import *
from knickknack import *
from time import *

#==========================================================
# SETUP MAIN + MAIN
#==========================================================

BOARDWIDTH  = 8
BOARDHEIGHT = 8
BOARDDEPTH  = 2
ACTIVELIST  = BOARDWIDTH*BOARDHEIGHT

#         R    G     B
WHITE = (255, 255,  255)
BLACK = (  0,   0,    0)

OPPONENT_TURN                     = 'turn_opponent.png'
PLAYER_TURN                       = 'turn_player.png'
JOKER_HOLDER                      = 'joker_holder.png'
ENEMY_QUEEN                       = 'enemy_queen.png'
ENEMY_PAWN                        = 'enemy_pawn.png'

TANK_BASIC                        = 'ground_hex_frame_Tank_stg0.png'

HOLD_BAR                          = 'holding_bar.png'
GROUND_HEX_FRAME_OPTION_STG0      = 'ground_hex_frame_shade_option_stg0.png'
GROUND_HEX_FRAME_HIGHLIGHT_STG0   = 'ground_hex_frame_shade_highlight_stg0.png'
GROUND_HEX_GRASSY_PLAIN           = 'ground_hex_frame_grassy_plains.png'
GROUND_HEX_FRAME_STG0             = 'ground_hex_frame_shade_stg0.png'
GROUND_TILE_FRAME_STG1            = 'ground_tile_frame_stg1.png'
GROUND_TILE_FRAME_STG2            = 'ground_tile_frame_stg2.png'
GROUND_TILE_FRAME_STG3            = 'ground_tile_frame_stg3.png'

#============================================================
# BATTLE CARDS
#============================================================
CARD_FRAME                        = 'card_frame.png' 
CARD_PASS                         = 'card_pass.png'

#============================================================
# INITIALIZING
#============================================================
turn_opponent   = pygame.image.load(OPPONENT_TURN)
turn_player     = pygame.image.load(PLAYER_TURN)
joker_IMG       = pygame.image.load(JOKER_HOLDER)
enemy_queen_IMG = pygame.image.load(ENEMY_QUEEN)
enemy_pawn_IMG  = pygame.image.load(ENEMY_PAWN)

Tank_IMG_BASIC  = pygame.image.load(TANK_BASIC)

player_hold_bar = pygame.image.load(HOLD_BAR)
tileOP_0        = pygame.image.load(GROUND_HEX_FRAME_OPTION_STG0)
tileHI_0        = pygame.image.load(GROUND_HEX_FRAME_HIGHLIGHT_STG0)
tileIMG_0       = pygame.image.load(GROUND_HEX_FRAME_STG0)
hexGrassyIMG_0  = pygame.image.load(GROUND_HEX_GRASSY_PLAIN)
tileIMG_1       = pygame.image.load(GROUND_TILE_FRAME_STG1)
tileIMG_2       = pygame.image.load(GROUND_TILE_FRAME_STG2)
tileIMG_3       = pygame.image.load(GROUND_TILE_FRAME_STG3)

#=============================================================
# BATTLE CARDS
#=============================================================
card_frame      = pygame.image.load(CARD_FRAME)
card_pass       = pygame.image.load(CARD_PASS)

#========================================
# Class Declarations
#========================================

class card:
	def __init__(self):
		self.card_id = 0
		self.ind_id = 0
		self.rise = 71
		self.run = 55
		self.ltposx = 0
		self.ltposy = 0
		self.image = card_frame
	def __init__(self, ID):
		if ID == 1:
			self.card_id = 1
			self.ind_id = 0
			self.rise = 71
			self.run = 55
			self.ltposx = 0
			self.ltposy = 0
			self.image = card_pass
	def ResetCard(self, ID):
		if ID == 1:
			self.image = card_pass

class tile:
  def __init__(self):
    self.i = 0
    self.j = 0
    self.k = 0
    self.rise = 28
    self.run = 14
    self.height = 2
    self.ltposx = 0
    self.ltposy = 0
    self.pixlength = 45
    self.pixwidth = 24
    self.image = tileIMG_0
    self.active = 1
  def inactivate(self):
    self.active = 0

class board:
  def __init__(self):
    self.board = []
    self.activitylist = []

class joker:
  def __init__(self):
    self.istaken = 0
    self.movelist = []
    self.holdlist = []
    self.handlist = []
    self.teamlist = []
    self.handsize = 0
    self.cansee = 0
    self.isturn = 1
    self.height = 30
    self.i = 0
    self.j = 4
    self.k = 3
    self.image = joker_IMG
    self.haswon = 0
    self.enemypausetimer = None
    self.turntimer = settimer()
    self.timetotal = 0
  def clearmovelist(self):
    I = set()
    for i in range(len(self.movelist)):
        I.add(i)
    for i in sorted(I, reverse=True):
        del self.movelist[i]
  def clearhandlist(self):
    I = set()
    for i in range(len(self.handlist)):
        I.add(i)
    for i in sorted(I, reverse=True):
        del self.handlist[i]
  def setuphand(self, starthand):
    for i in range (starthand):
      self.handlist.append(card(1))
      self.handlist[i].ltposx = 10 + 35*i
      self.handlist[i].ltposy = 400
  def resethand(self):
    for i in range (len(self.handlist)):
      self.handlist[i].ResetCard(self.handlist[i].card_id)
      self.handlist[i].ltposy = 400
  #def clearknightmovelist(self):
  #  I = set()
  #  for i in range(len(self.knightmovelist)):
  #      I.add(i)
  #  for i in sorted(I, reverse=True):
  #      del self.knightmovelist[i]
  
class enemy_queen:
	def __init__(self):
		self.istaken = 0
		self.type = 2
		self.height = 35
		self.i = 0
		self.j = 0
		self.k = 0
		self.queenmovementlist = []
		self.image = enemy_queen_IMG

class enemy_pawn:
	def __init__(self):
		self.istaken = 0
		self.type = 1
		self.height = 21
		self.i = 0
		self.j = 0
		self.k = 0
		self.image = enemy_pawn_IMG
		self.pawnmovementlist = []

class tank:
	def __init__(self):
		self.istaken = 0
		self.type = 3
		self.height = 35
		self.i = 0
		self.j = 0
		self.k = 0
		self.image = Tank_IMG_BASIC
		self.tankmovementlist = []