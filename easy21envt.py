import numpy as np
import random

def step(s,a):
	"""
	Implements one step for the Easy21 game. a (action) is 0 for hit, 1 for stick. s (state) is of the form (dealer's card,player's sum).
	returns (s',r) where s' is the next state and r is the reward. if s'==-1 then that is the terminal state.
	red cards are -1, black cards are +1
	"""
	if (a==0):
		draw = [np.random.choice([-1,1,1]),np.random.randint(1,11)] #draw appropriate card with appropriate colour
		#print draw
		s[1] += draw[0]*draw[1] #player did not go bust, return s and zero reward
		r = 0
		if (s[1]>21 or s[1]<1): #player is bust, terminal-state and -1 reward
			#print "player went bust"
			s[0] = -1
			r = -1
	else:
		while (s[0]<17 and s[0]>=1):
			draw = [np.random.choice([-1,1,1]),np.random.randint(1,11)] #draw appropriate card with appropriate colour
			#print draw
			s[0] += draw[0]*draw[1]
		if (s[0]>21 or s[0]<1):  #dealer is bust, terminal-state
			#print "dealer went bust"
			r = +1
		else: #dealer did not go bust, now the sum will be compared
			#print "dealer did not go bust, comparing cards"
			if (s[0]>s[1]): r = -1
			elif (s[0]<s[1]): r = 1
			else: r = 0

		s[0] = -1
	#print "state,reward is",s,r
	return s,r

if __name__ == "__main__":
	state = [np.random.randint(1,11),np.random.randint(1,11)]
	action = 0
	state,reward = step(state,action)
	#whatever your policy is for choosing next action, implement it below and keep calling step function



