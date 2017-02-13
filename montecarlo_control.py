import numpy as np
from easy21envt import step as step
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

"""
So my actions are hit (0) or stick (1)
My state is actually [dealer's card,player's sum]
Rewards are +1,0,-1
"""
num_states = 210.0 #21*10
num_actions = 2.0
Q = np.zeros((10,21,2)) #action value function
V = np.zeros((10,21)) #state value function
#note that policy will not be explicitly maintained in Monte-Carlo control

Nsa = np.zeros_like(Q) #number of times chosen state-action pair
Ns = np.zeros_like(V) #number of times visited state
N0 = 100.0

def policy(s,Q,Nst): #return action according to epsilon-greedy policy on Q
	greedy_action = np.argmax(Q[s[0]-1,s[1]-1])
	epsilon = N0/(N0+Nst)
	a = np.random.choice([greedy_action,0,1],p=[1-epsilon,epsilon/2.0,epsilon/2.0])
	return a

def run_episode():
	history = []
	state = [np.random.randint(1,11),np.random.randint(1,11)]
	old_state = []
	#print "Initial state is",state
	while (state[0]!=-1):				#capture an entire episode of experience
		a = policy(state,Q,Ns[state[0]-1,state[1]-1])	#always 0 initially
		#print "The action chosen is (0-hit,1-stick)",a
		old_state[:] = state
		temp,r = step(state,a)
		history.append([old_state[:],a,r])
	
	#print "History accumulated is",history

	reward = 0						#now calculating g - returns
	g = []
	for i in xrange(len(history)-1,-1,-1):
		reward += history[i][2]
		#print "Reward",i,reward
		g.append(reward)

	i = 1
	for s,a,r in history:
		Ns[s[0]-1,s[1]-1] += 1
		Nsa[s[0]-1,s[1]-1,a] += 1
		#print Ns[s[0]-1,s[1]-1],Nsa[s[0]-1,s[1]-1,a]
		Q[s[0]-1,s[1]-1,a] = Q[s[0]-1,s[1]-1,a] + (1.0/Nsa[s[0]-1,s[1]-1,a])*(g[-i]-Q[s[0]-1,s[1]-1,a])
		i += 1

	return Q,history

def get_value_function(Q):
	V = np.zeros((Q.shape[0],Q.shape[1]))
	for i in xrange(Q.shape[0]):
		for j in xrange(Q.shape[1]):
			V[i][j] = np.max(Q[i][j])
	return V

def plot_value_function(V):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	X,Y = np.meshgrid(range(V.shape[1]),range(V.shape[0]))
	ax.plot_wireframe(X,Y,V)
	ax.set_xlabel('Sum of player cards')
	ax.set_ylabel('Initial dealer card')
	plt.show()

