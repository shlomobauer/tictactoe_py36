# tic tac toe

import sys
import numpy as np

LENGTH = 3
XVAL = -1
OVAL = 1

debug=False

class SmartAgent :
 def __init__(self, eps=0.1, alpha=0.5) :
  self.eps = eps
  self.alpha = alpha
  self.state_history = []
  self.V = [0.5]*(3**(LENGTH * LENGTH))

 def resetHistory(self) :
  self.state_history = []

 def set_symbol(self,sym) :
  self.sym = sym # XVAL or OVAL

 def saveBrainX(self):
  outf = open("./myhistoryX","w")
  for i in range(len(self.V)):
   outf.write(str(self.V[i]) + "\n")
  outf.close()

 def saveBrainO(self):
  outf = open("./myhistoryO","w")
  for i in range(len(self.V)):
   outf.write(str(self.V[i]) + "\n")
  outf.close()

 def loadBrainX(self):
  inf = open("./myhistoryX","r")
  i = 0
  for line in inf:
   v = float(line)
   self.V[i] = v
   i = i + 1
  inf.close()

 def loadBrainO(self):
  inf = open("./myhistoryO","r")
  i = 0
  for line in inf:
   v = float(line)
   self.V[i] = v
   i = i + 1
  inf.close()

 def update_state_history(self, s) :
  self.state_history.append(s)

  if debug :
   print("smart robot updating state history ")
   for ii in reversed(self.state_history) :
    print(ii)

 def update(self,env) :
  reward = None
  if env.is_tie():
   reward = 0.5
  else:
   reward = env.reward(self.sym) # 1 if this player won; 0 otherwise

  state = env.get_state()

  if reward == 1:
   self.V[state] = 1.0
  elif reward == 0.5:
   self.V[state] = 0.5
  else:
   self.V[state] = 0.0

  if debug :
   print("current state, value")
   for ii in reversed(self.state_history) :
    print("state ",ii, "value ", self.V[ii])
  
  target = reward

  for prev in reversed(self.state_history) :
   value = self.V[prev] + self.alpha * (target - self.V[prev])
   self.V[prev] = value
   target = value

  if debug :
   print("iteration learned state, value")
   for ii in reversed(self.state_history) :
    print("state ",ii, "value ", self.V[ii])

  self.resetHistory()

 def take_action(self, env):
  r = np.random.rand()
  if r < self.eps :  # explore by taking a random action
   if debug :
    print("Making a Random Move")
   possible_moves = []
   for i in range(LENGTH):
    for j in range(LENGTH):
     if env.is_empty(i, j):
      possible_moves.append((i, j))
   idx = np.random.choice(len(possible_moves))
   next_move = possible_moves[idx]
   env.board[next_move[0], next_move[1]] = self.sym
  else:  # choose best action based on current values
   qvalues={}
   best_value = -1
   for i in range(LENGTH) :
    for j in range(LENGTH) :
     if env.is_empty(i,j) :
      # we want to know the state we would be in, if we
      # made this move.  Why? so we can get the "Value"
      # of making this move.  We want to choose the
      # best next move - i.e., the one with the highest
      # value

      env.board[i,j] = self.sym # pretend to make the move
      state = env.get_state()   # the integer representing the state

      # is this a winning move?
      if env.game_over() :
       self.V[state] = 1 

      env.board[i,j] = 0        # unmove as soon as possible
      qvalues[(i,j)] = self.V[state]
      if self.V[state] > best_value :
       best_value = self.V[state]
       next_move = (i,j)

   
   if debug :
    print("Making a Greedy Move")
    for i in range(LENGTH):
     print("-----------------")
     for j in range(LENGTH):
      if env.is_empty(i,j):
       print('"%.2f|" % qvalues[(i,j)]',end="")
      else:
       if env.board[i,j] == env.x:
        print("   x|",end="")
       elif env.board[i,j] == env.o:
        print("   o|",end="")
       else:
        print("    |",end="")
     print("")
    print("-----------------")
  
   env.board[next_move[0], next_move[1]] = self.sym

class Environment:
 def __init__(self):
  self.board = np.zeros((LENGTH, LENGTH))
  self.x = XVAL # represents an x on the board, player 1
  self.o = OVAL # represents an o on the board, player 2
  self.winner = 0
  self.ended = False
  self.num_states = 3**(LENGTH*LENGTH)  # 19683

 def is_empty(self, i, j) :
  return self.board[i,j] == 0

 def is_tie(self):
  return (self.winner == 0)

 def reward(self, sym) :
  # the winner gets the reward
  if self.winner == sym :
   return 1
  else:
   return 0

 def get_state(self) :
  # "godelize" state
  # 9 cells, each cell can have 3 possible values:
  #  empty, x, o ==> 0, 1, -1
  # cell 8 (2,2) = 3^8 * 0 | 3^8 * 1 | 3^8 * 2 for empty, x, o (0,6561,13122)
  # cell 7 (2,1) = 3^7 * 0 | 3^7 * 1 | 3^7 * 2 for empty, x, o (0,2187,4374)
  # cell 6 (2,0) = 3^6 * 0 | 3^6 * 1 | 3^6 * 2 for empty, x, o (0,729,1458)
  # cell 5 (1,2) = 3^5 * 0 | 3^5 * 1 | 3^5 * 2 for empty, x, o (0,243,486)
  # cell 4 (1,1) = 3^4 * 0 | 3^4 * 1 | 3^4 * 2 for empty, x, o (0,81,192)
  # cell 3 (1,0) = 3^3 * 0 | 3^3 * 1 | 3^3 * 2 for empty, x, o (0,27,54)
  # cell 2 (0,2) = 3^2 * 0 | 3^2 * 1 | 3^2 * 2 for empty, x, o (0,9,18)
  # cell 1 (0,1) = 3^1 * 0 | 3^1 * 1 | 3^1 * 2 for empty, x, o (0,3,6)
  # cell 0 (0,0) = 3^0 * 0 | 3^0 * 1 | 3^0 * 2 for empty, x, o (0,1,2)

  # examine each cell and calculate the integer corresponding
  # to the state (symbols in each cell)

  k = 0
  h = 0
  for i in range(LENGTH):
   for j in range(LENGTH):
    if self.board[i,j] == 0:
     v = 0
    elif self.board[i,j] == self.x:
     v = 1
    elif self.board[i,j] == self.o:
     v = 2

    h += (3**k) * v
    k += 1

  return h

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
   print("-------------")
   for j in range(LENGTH):
    print("|",end="")
    if self.board[i,j] == self.x:
     print("x",end="")
    elif self.board[i,j] == self.o:
     print("o",end="")
    else:
     print(" ",end="")
   print("|")
  print("-------------")

class Human:
 def __init__(self):
  pass

 def set_symbol(self, sym):
  self.sym = sym

 def take_action(self, env):
  while True:
   move = input("Enter coordinates i,j for your next move (i,j=0..2): ")
   i, j = move.split(',')
   i = int(i)
   j = int(j)
   if env.is_empty(i, j):
    env.board[i,j] = self.sym
    break

 def update(self, env) :
  pass

 def update_state_history(self, s):
  pass

def play_smartgame(p1, p2, env, draw=False):
 current_player = None
 while not env.game_over():
  if current_player == p1:
   current_player = p2
  else:
   current_player = p1

  if draw:
   if draw == 1 and current_player == p1:
    env.draw_board()
   if draw == 2 and current_player == p2:
    env.draw_board()

  current_player.take_action(env)

  # track state history, so
  # when game over, we can update
  # "values" so that are able
  # to play better next time

  state = env.get_state()

  p1.update_state_history(state)
  p2.update_state_history(state)

 # game over - 
 if draw:
  env.draw_board()

 # update the value function
 p1.update(env)
 p2.update(env)

def play_game(p1, p2, env, draw=False):
 current_player = None
 while not env.game_over():
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

 print("Training Experts")

 ai1=SmartAgent()
 ai1.set_symbol(XVAL)

 ai2=SmartAgent()
 ai2.set_symbol(OVAL)

 T=30000
 zz=0
 for t in range(T):
  if t % 200 == 0 :
   zz = zz + 1
   print(". ",end="")
   if zz % 10 == 0 :
    print("")
   sys.stdout.flush()

  play_smartgame(ai1,ai2,Environment())

 print("\nDone! Experts Trained.")

 ai1.eps = 0.0
 ai2.eps = 0.0

 debug=False

 goFirst = False
 answer = input("Go First? [Y/n]: ")
 if answer.lower()[0] == 'n':
  goFirst = False
 else:
  goFirst = True

 human = Human()

 if goFirst :
  human.set_symbol(XVAL)
  ai = ai2
  while True:
   myenv = Environment()
   play_smartgame(human, ai, myenv, draw=1)

   print("")
   if myenv.winner == XVAL :
    print("Congratulations! You Won!!!!")
   elif myenv.winner == OVAL :
    print("Good Try! You're Still Learning.")
   else:
    print("Tie!  Let's Play More.")
   print("")
 
   answer = input("Play again? [Y/n]: ")
   if answer.lower()[0] == 'n':
    break
 else:
  human.set_symbol(OVAL)
  ai = ai1
  while True:
   myenv = Environment()
   play_smartgame(ai, human, myenv, draw=2)
 
   print("")
   if myenv.winner == OVAL :
    print("Congratulations! You Won!!!!")
   elif myenv.winner == XVAL :
    print("Good Try! You're Still Learning.")
   else:
    print("Tie!  Let's Play More.")
   print("")

   answer = input("Play again? [Y/n]: ")
   if answer.lower()[0] == 'n':
    break
