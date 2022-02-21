import sys

BOARDDEPTH = 2
BOARDWIDTH = 8
BOARDHEIGHT = 8
ACTIVELIST = 64

def checkactivitylist(activitylist):
  for i in range (ACTIVELIST):
      sys.stdout.write("(%d%% \r)" % (activitylist[i].k))

def createactivitylist(board):
  activitylist = []
  for i in range (BOARDDEPTH):
    for j in range (BOARDWIDTH):
      for k in range (BOARDHEIGHT):
        if board[i][j][k].active == 1:
          activitylist.append(board[i][j][k])
  return activitylist

def sortheightactivitylist(activitylist):
  activitylist.sort(key=lambda x: x.ltposy)
  return activitylist

#              |BOARD CONFIGURATION|
#
#                      (0,0)
#                   (1,0),(0,1)
#                (2,0),(1,1),(0,2)
#             (3,0),(2,1),(1,2),(0,3)
#          (4,0),(3,1),(2,2),(1,3),(0,4)
#       (5,0),(4,1),(3,2),(2,3),(1,4),(0,5)
#    (6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6)
# (7,0),(6,1),(5,2),(4,3),(3,4),(2,5),(1,6),(0,7)
#    (7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7)
#       (7,2),(6,3),(5,4),(4,5),(3,6),(2,7)
#          (7,3),(6,4),(5,5),(4,6),(3,7)
#             (7,4),(6,5),(5,6),(4,7)
#                (7,5),(6,6),(5,7)
#                   (7,6),(6,7)
#                      (7,7)
