import sqlite3
import itertools
import numpy as np
from random import shuffle

projectDB = 'stripe_flyVRProjects.db'
expDB = 'stripe_flyVRExperiments.db'

project = 'DecisionGeometry'

nPosts = 10
nCubes = 3
cube0='None'
cube1='None'
cube2='None'

posts = range(1,2)
cubes = range(1,2)
#???
posts = list(itertools.chain.from_iterable(itertools.repeat(x, 10) for x in posts))
distances = [5.0]
start_ang_split = 8
angles2 = [np.pi/3, 7*np.pi/18, np.pi]
angles3 = [5*np.pi/18, 5*np.pi/18, 2*np.pi/3]

# creates empty database
def FirstGen():
	# establish a connection to the project database
	conn = sqlite3.connect(projectDB)
	# connect a cursor that goes through the project database
	cursorProject = conn.cursor()
	# create a table with specified column names and datatypes
	cursorProject.execute('''CREATE TABLE projects (project text, exp integer,
										replicate integer,
										tExp int,tSwitch integer, 
										nSwitch integer,
										nStimuli integer, 
										post0 text,post1 text, 
										post2 text,post3 text, 
										post4 text,post5 text, 
										post6 text,post7 text, 
										post8 text,post9 text,
										cube0 int, cube1 int,
										cube2 int)''')
	#cubes: 0=black, 1=white, 2=grey
	# commit and close connection
	conn.commit()
	conn.close()
	
	# establish a connection to the experiment database
	conn = sqlite3.connect(expDB)
	# connectr a cursor that goes through the experiment database
	cursorExperiment = conn.cursor()
	# create a table with specified column names and datatypes
	cursorExperiment.execute('''CREATE TABLE experiments (project text, exp integer,
										replicate integer,
										date text, tStart text, tEnd text, 
										nameExperimenter text,expId text)''')
	# commit and close connection
	conn.commit()
	conn.close()


# creates a no post  control
def dataController():
	data=[]
	#but if no post control, then no background needed right??!???
	# data are values inside cylinder
	#backgrounds=[]
	for j in range(0,nPosts):
		dataStimuli = 'None'
		data.append(str(dataStimuli))
	
		'''for l in range(0,nCubes):
		backgroundStimuli = 'None'
		backgrounds.append(str(backgroundStimuli))
		#or:???
		for l in range(0,nCubes):
		backgroundStimuli = 'None'
		data.append(str(dataStimuli))'''
	

	return data 






# define stimuli based on experimental condition
# the expType parameter defines which parameter is randomised for a given fly
# the other parameter is randomised between flies
def defineStimuli(expType, nSwitch, nReplicates=2, N=2, d=1.0, ang=np.pi/6, picked=[]):
	dataReplicates = []
	dataControl = dataController()

	'''if expType == 'nPosts':
		data = []
		# define stimuli nSwitch-2 times since we have two control stimuli - one in the beginning; other in the end
		for k in range(0,nSwitch-2):
			data.append([])
			# pick random number of posts
			N = np.random.randint(np.max(posts)-np.min(posts)+1)+np.min(posts)
			# pick a random start angle (one of six angles obtained by splitting angle of symmetry for N posts in six parts)
			start_ang = 2*np.pi*(np.random.randint(start_ang_split)+1) / start_ang_split
			for j in range(0,nPosts):
				if j < N:
					r = d
					theta = start_ang + j*2*np.pi*ang / (N*6)
					x = r*np.cos(theta)
					y = r*np.sin(theta)
					dataStimuli = {'position' : (x,y), 'distance' : r, 'angle' : 2*np.pi*ang / (N*6)}
				else:
					dataStimuli = 'None'
				data[-1].append(str(dataStimuli))'''	
	if expType == 'angles':
		data = []
		backgrounds =[]
		cubeStim= 0
		#randNumber = np.random.randint(0,4)
		# define stimuli nSwitch-2 times since we have two control stimuli - one in the beginning; other in the end
		for k in range(0,nSwitch-2):
			data.append([])
			#background.append([])
			# pick a random start angle (one of six angles obtained by splitting angle of symmetry for N posts in six parts)
			start_ang = 2*np.pi*(np.random.randint(start_ang_split)+1) / start_ang_split
			# pick a random angle that will be the angle between successive posts
			ang = -1.0
			while ang in picked or ang < 0.0:
				ang = np.random.randint(3)
			picked.append(ang)
			randNumber = np.random.randint(0,4)
			print('randnum', randNumber)

			for j in range(0,nPosts):
				print('going in loop')
				if j == randNumber:

					# here j < 4 creates 4 posts at experiment!!!

					#another if none and if background is the same color then --> none
					r = d
					angle = angles2[ang] if N == 2 else angles3[ang]
					theta = start_ang + j*angle
					x = r*np.cos(theta)
					y = r*np.sin(theta)
					dataStimuli = {'position' : (x,y), 'distance' : r, 'angle' : angle, 'color' : randNumber}
					#excluding cube to be equal color as cylinder
					for h in range(0,nCubes):
						if h == randNumber:
							cubeStim= randNumber
							globals()['cube' + str(randNumber)] = 'None'
						else:
							cubeStim= h
							globals()['cube' + str(randNumber)] = randNumber


					'''if globals()['cube' + str(randNumber)] = 'None'



					for h in range(0,nCubes):
						if h == randNumber:
							globals()['cube' + str(randNumber)] = 'None'
							cubeStim= 'None'
						else:
							globals()['cube' + str(randNumber)] = randNumber
							cubeStim= 1'''

				else:
					dataStimuli = 'None'
				data[-1].append(str(dataStimuli))
				#here it needs to  save the status of the cube in a dictionary (?)
				#backgrounds.append(cubeStim)


			
				#print('backgr',backgrounds)
				#print('data', data)	





	
	# permute replicates before adding them to the database
	# sandwich permutations between controls
	for k in range(0,nReplicates):
		dataReplicates.append([])
		dataReplicates[-1].append(dataControl)
		print(data)
		shuffle(data)
		for dataStimilus  in data:
			dataReplicates[-1].append(dataStimilus)
		dataReplicates[-1].append(dataControl)
	
	return dataReplicates


# write defined stimuli to database
def writeStimuli(cursor,projects,exp,nReplicate,tExp,tSwitch,nSwitch,data):

#***in values insert str(....backgrounds grey, white, black[][0-2])
# insert color information of posts: exclude same color post/background 
	#print("HEHEHEHEHEHEHEHE", data[0][0][7])


	for perm in range(0, nReplicate):
		for k in range(0, nSwitch):
			values = [projects, exp, perm, tExp, tSwitch, nSwitch, k, str(data[perm][k][0]), str(data[perm][k][1]), str(data[perm][k][2]), str(data[perm][k][3]), str(data[perm][k][4]), str(data[perm][k][5]), str(data[perm][k][6]), str(data[perm][k][7]), str(data[perm][k][8]), str(data[perm][k][9]), cube0, cube1, cube2]
			cursor.execute("INSERT INTO projects VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
			#cursor.execute("INSERT INTO projects VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values)

# fill database created by FirstGen
def main():
	# open the database
	conn = sqlite3.connect(projectDB)
	cursorProject = conn.cursor()

	# check the number of experiments in the project
	cursorProject.execute("Select exp from projects where project = ? ",(project,))
	fetched = cursorProject.fetchall()
	expType = np.unique(fetched)
	print(expType)
	print(len(expType))

	if len(expType) == 0:
		exp = -1
	else:
		exp = int(np.amax(expType))


	# define expType based on what variable needs randomisation within individual i.e. your experimental parameter
	expType = 'angles'
	tSwitch = 3
	nSwitch = 5
	tExp = tSwitch*nSwitch   
	nReplicates = 5

	N = 2
	d = 1.0
	ang = np.pi/6

	'''if expType == 'nPosts':
		for d in distances:
			for ang in range(1,7):
				# write your new stimuli
				exp += 1
				data = defineStimuli(expType, nSwitch, nReplicates, N=N, d=d, ang=ang)
				writeStimuli(cursorProject, project, exp, nReplicate = nReplicates, tExp = tExp, tSwitch = tSwitch, nSwitch = nSwitch, data=data)'''
	if expType == 'angles':
		for N in posts:
			for d in distances:
				picked_angs = []
				# write your new stimuli
				exp += 1
				data = defineStimuli(expType, nSwitch, nReplicates, N=N, d=d, ang=ang, picked=picked_angs)
				writeStimuli(cursorProject, project, exp, nReplicate = nReplicates, tExp = tExp, tSwitch = tSwitch, nSwitch = nSwitch, data=data)



	# commit and close connection
	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()