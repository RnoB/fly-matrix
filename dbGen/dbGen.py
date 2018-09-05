import sqlite3
import numpy as np
from random import shuffle

projectDB = 'flyProjects.db'
expDB = 'flyExperiments.db'

project = 'DecisionGeometry'

nPosts = 10
expPosts_min = 1
expPosts_max = 1
distances = [8.0, 10.0, 12.0]

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
										post8 text,post9 text)''')
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




def dataController():
	data=[]
	for j in range(0,10):
		data.append('None')
	return data 




def defineStimuli(expType, nSwitch, nReplicates=2, N=2, d=1.0, ang=np.pi/6):
	dataReplicates = []
	dataControl = dataController()


	if expType == 'nPosts':
		data = []
		for k in range(0,nSwitch-1):
			data.append([])
			N = np.random.randint(expPosts_max-expPosts_min+1)+expPosts_min
			start_ang = 2*np.pi*(np.random.randint(6)+1) / 6
			for j in range(0,nPosts):
				if j < N:
					r = d
					theta = start_ang + j*2*np.pi*ang / (N*6)
					x = r*np.cos(theta)
					y = r*np.sin(theta)
					dataStimuli = {'position' : (x,y), 'distance' : r, 'angle' : 2*np.pi*ang / (N*6)}
				else:
					dataStimuli = 'None'
				data[-1].append(str(dataStimuli))
		for k in range(0,nReplicates):
			dataReplicates.append([])
			dataReplicates[-1].append(dataControl)
			print(data)
			shuffle(data)
			for dataStimilus  in data:
				dataReplicates[-1].append(dataStimilus)

	elif expType == 'distances':
		data = []
		for k in range(0,nSwitch-1):
			data.append([])
			start_ang = 2*np.pi*(np.random.randint(6)+1) / 6 
			for j in range(0,nPosts):
				if j < N:
					r = np.random.choice(distances)
					theta = start_ang + j*2*np.pi*ang / (N*6)
					x = r*np.cos(theta)
					y = r*np.sin(theta)
					dataStimuli = {'position' : (x,y), 'distance' : r, 'angle' : 2*np.pi*ang / (N*6)}
				else:
					dataStimuli = 'None'
				data[-1].append(str(dataStimuli))
		for k in range(0,nReplicates):
			dataReplicates.append([])
			dataReplicates[-1].append(dataControl)
			print(data)
			shuffle(data)
			for dataStimilus  in data:
				dataReplicates[-1].append(dataStimilus)

	elif expType == 'angles':
		data = []
		for k in range(0,nSwitch-1):
			data.append([])
			start_ang = 2*np.pi*(np.random.randint(6)+1) / 6 
			ang = np.random.randint(6)+1
			for j in range(0,nPosts):
				if j < N:
					r = d
					theta = start_ang + j*2*np.pi*ang / (N*6)
					x = r*np.cos(theta)
					y = r*np.sin(theta)
					dataStimuli = {'position' : (x,y), 'distance' : r, 'angle' : 2*np.pi*ang / (N*6)}
				else:
					dataStimuli = 'None'
				data[-1].append(str(dataStimuli))
		for k in range(0,nReplicates):
			dataReplicates.append([])
			dataReplicates[-1].append(dataControl)
			print(data)
			shuffle(data)
			for dataStimilus  in data:
				dataReplicates[-1].append(dataStimilus)
	
	return dataReplicates




def writeStimuli(cursor,projects,exp,nReplicate,tExp,tSwitch,nSwitch,data):

	for perm in range(0, nReplicate):
		for k in range(0, nSwitch):
			values = [projects, exp, perm, tExp, tSwitch, nSwitch, k, str(data[perm][k][0]), str(data[perm][k][1]), str(data[perm][k][2]), str(data[perm][k][3]), str(data[perm][k][4]), str(data[perm][k][5]), str(data[perm][k][6]), str(data[perm][k][7]), str(data[perm][k][8]), str(data[perm][k][9])]
			cursor.execute("INSERT INTO projects VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)



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


	# WRITE NEW EXPTYPE IF YOU WANT DISTANCES OR ANGLES AS EXPERIMENTAL PARAMETER
	
	expType = 'angles'
	tSwitch = 10
	nSwitch = 6
	tExp = tSwitch*nSwitch   
	nReplicates = 10

	N = 2
	d = 1.0
	ang = np.pi/6

	if expType == 'nPosts':
		for d in distances:
			for ang in range(1,7):
				# write your new stimuli
				exp += 1
				data = defineStimuli(expType, nSwitch, nReplicates, N=N, d=d, ang=ang)
				writeStimuli(cursorProject, project, exp, nReplicate = nReplicates, tExp = tExp, tSwitch = tSwitch, nSwitch = nSwitch, data=data)
	if expType == 'distances':
		for ang in range(1,7):	
			for N in range(expPosts_min,expPosts_max+1):
				# write your new stimuli
				exp += 1
				data = defineStimuli(expType, nSwitch, nReplicates, N=N, d=d, ang=ang)
				writeStimuli(cursorProject, project, exp, nReplicate = nReplicates, tExp = tExp, tSwitch = tSwitch, nSwitch = nSwitch, data=data)
	if expType == 'angles':
		for N in range(expPosts_min,expPosts_max+1):
			for d in distances:
				# write your new stimuli
				exp += 1
				data = defineStimuli(expType, nSwitch, nReplicates, N=N, d=d, ang=ang)
				writeStimuli(cursorProject, project, exp, nReplicate = nReplicates, tExp = tExp, tSwitch = tSwitch, nSwitch = nSwitch, data=data)


	# commit and close connection
	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()