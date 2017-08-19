# tic tac toe
# non-human player plays randomly

import numpy as np

LENGTH = 3
XVAL = -1
OVAL = 1

class Agent:
 def __init__(self):
  pass

 def set_symbol(self, sym):
  self.sym = sym

 # choose next move randomly
 # from open cells
 def take_action(self, env):
  possible_moves = []
  for i in range(LENGTH):
   for j in range(LENGTH):
    if env.is_empty(i, j):
     possible_moves.append((i, j))
  idx = np.random.choice(len(possible_moves))
  next_move = possible_moves[idx]
  env.board[next_move[0], next_move[1]] = self.sym

class Environment:
 def __init__(self):
  self.board = np.zeros((LENGTH, LENGTH))
  self.x = XVAL # represents an x on the board, player 1
  self.o = OVAL # represents an o on the board, player 2
  self.winner = 0
  self.ended = False
  self.num_states = 3**(LENGTH*LENGTH)  # 19683

 def is_empty(self, i, j):
  return self.board[i,j] == 0

 def game_over(self) :
  # check rows
  # (i,j) == 1 ==> o in cell, so if (i,0) + (i,1) + (i,2) == 3, then o won!
  # (i,j) == -1 ==> x in cell, so if (i,0) + (i,1) + (i,2) == -3, then x won!

  for i in range(LENGTH) :
   for player in (self.x, self.o) :
    if self.board[i].sum() == player*LENGTH :
     self.winner = player
     self.ended = True
     return True

  # check columns
  for j in range(LENGTH) :
   for player in (self.x, self.o) :
    if self.board[:,j].sum() == player*LENGTH :
     self.winner = player
     self.ended = True
     return True

  # check diagonals
  for player in (self.x, self.o) :
   if (self.board[0,0] + self.board[1,1] + self.board[2,2]) == player*LENGTH :
    self.winner = player
    self.ended = True
    return True

   if (self.board[0,2] + self.board[1,1] + self.board[2,0]) == player*LENGTH :
    self.winner = player
    self.ended = True
    return True

  # check if draw
  # all cells have an x or o
  if np.all((self.board == 0) == False):
   self.winner = 0
   self.ended = True
   return True

  # game is not over
  self.winner = 0
  return False

  # Example board
  # -------------
  # | x |   |   |
  # -------------
  # |   |   |   |
  # -------------
  # |   |   | o |
  # -------------
 def draw_board(self):
  for i in range(LENGTH):
   print ("-------------")
   for j in range(LENGTH):
    print ("|",end="")
    if self.board[i,j] == self.x:
     print ("x",end="")
    elif self.board[i,j] == self.o:
     print ("o",end="")
    else:
     print (" ",end="")
   print ("|")
  print ("-------------")

class Human:
 def __init__(self):
  pass

 def set_symbol(self, sym):
  self.sym = sym

 def take_action(self, env):
  while True:
   move = input("Enter coordinates i,j for your next move (i,j=0..2): ")
   i,j = move.split(',')
   i = int(i)
   j = int(j)
   if env.is_empty(i, j):
    env.board[i,j] = self.sym
    break

def play_game(p1, p2, env, draw=False):
 # loops until the game is over
 current_player = None
 while not env.game_over():
  # alternate between players
  # p1 always starts first
  if current_player == p1:
   current_player = p2
  else:
   current_player = p1

  # draw the board before the user who wants to see it makes a move
  if draw:
   if draw == 1 and current_player == p1:
    env.draw_board()
   if draw == 2 and current_player == p2:
    env.draw_board()

  # current player makes a move
  current_player.take_action(env)

 # game over
 if draw:
  env.draw_board()

if __name__ == '__main__':
  
 goFirst = False

 while True:
  answer = input("Go First? [Y/n]: ")
  if answer.lower()[0] == 'n':
   goFirst = False
  else:
   goFirst = True

  ai = Agent()
  human = Human()
  myenv = Environment()

  if goFirst :
   human.set_symbol(XVAL)
   ai.set_symbol(OVAL)
   play_game(human, ai, myenv, draw=1)
  else :
   human.set_symbol(OVAL)
   ai.set_symbol(XVAL)
   play_game(ai, human, myenv, draw=2)
   
  print ("")
  if (myenv.winner==XVAL and goFirst)or(myenv.winner==OVAL and not goFirst) :
   print ("Congratulations! You Won!!!!")
  elif (myenv.winner==OVAL and goFirst)or(myenv.winner==XVAL and not goFirst) :
   print ("Good Try! You're Still Learning.")
  else:
   print ("Tie!  Let's Play More.")

  print ("")

  answer = input("Play again? [Y/n]: ")
  if answer and answer.lower()[0] == 'n':
   break
 
 print("\nThanks For Playing!\n")
