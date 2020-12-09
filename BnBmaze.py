import math

def isValid(maze,row,col):	#helps avoid out of the bounds of the array exception
	return (row >=0) and (row < len(maze)) and (col >=0) and (col < len(maze[0]))

def child(maze,cell,visited):	#find the next possible moves in the maze
	c =[]
	rowNum = [-1,0,0,1]
	colNum = [0,-1,1,0]
	for i in range(4):
		col = cell[1] + colNum[i]
		row = cell[0] + rowNum[i]
		if (isValid(maze,row,col) and maze[row][col] > 0 and visited[row][col] == False):
			c.append(row)
			c.append(col)
			visited[row][col] = True
	if len(c)%4==0: #turns [a,b,c,d] to [[a,b],[c,d]] since every [i,j] pair stands for a child of a cell
		ch = [[c[i],c[i+1]] for i in range(0,len(c),2)]
		return ch
	else:
		return c

def initializeVisited(list,visited):	#initializes the visited array to avoid the problem
	#of a cell having already been visited but still used for an alternative better path
	visited = [[False for i in range(5)] for i in range(6)]
	if len(list)!=0:
		for x in list:
			if(visited[x[0]][x[1]] == False):
				visited[x[0]][x[1]] = True
		return visited
	else:
		return visited

def visualizeBestPath(path,maze): 	#shows the best path on the maze
	maze = [[0 for i in range(len(maze[0]))] for i in range(len(maze))]
	for cell in path:
		if maze[cell[0]][cell[1]] == 0:
			maze[cell[0]][cell[1]] = 1
	return maze

def add(next,search): #adds te children to the searching front: if children =[[a,b],...,[c,d]] they are added to the front as alternative paths with different ending cells
	temp = []
	alternative = []
	if(any(isinstance(i,list) for i in search[0])): #checks if the searching front has paths in it already: actually checks if a list has nested lists in it
		current = search[0]
		alternative = search[1:]
	else:
		current = search[:]
	search.clear()
	if next not in current: 	#if the children are not already in our current path
		if(any(isinstance(i,list) for i in next)): 	#checks if the children cells are more than one
			temp.extend(current)
			for x in next:
				temp.append(x)
				search.append(temp[:])
				temp.remove(x)
		else:
			current.append(next)
			search.append(current)
	if(len(alternative)!=0):
		for x in alternative:
			search.append(x)
	return search


def creatingPath(maze,goal,search,currPath,visited,finalCost):
	while [goal[0],goal[1]] not in search:
		if len(currPath)-1<=finalCost: #cuts off any branch greater than the currently best branch	(here: branch means path)
			children = child(maze,currPath[-1],visited)	#we find the children of the last cell in the path
			if len(children) == 0:			 #if the next child was already visited in the same path
				for path in search:
					if len(path) >= finalCost:		#we ensure that no other path is greater or equal to the best path
						search.remove(path)
				currPath = search[0]
				return creatingPath(maze,goal,search,currPath,visited,finalCost) #we check the new first path in the searching front
			else:
				search = add(children,search)
				currPath = search[0]
				if any([goal[0],goal[1]] in path for path in search):
					for x in search:
						if [goal[0],goal[1]] in x:	#we search for the path leading to the goal cell
							path = x[:]
							search.remove(x)
					for x in reversed(search): #and we remove all the paths that are greater or equal to it
						if len(x) >= len(path):
							search.remove(x)
					print("\n PATH CREATION ENDED \n")
					finalCost = len(path) - 1
					return path,finalCost,search
		return creatingPath(maze,goal,search,currPath,visited,finalCost)	 #if we still haven't reached the goal cell we go on creating the path


def BnB(maze,init,goal):
	visited = [[False for i in range(len(maze[0]))] for i in range(len(maze))]
	search = [] 	#this will be the searching front
	visited[init[0]][init[1]] = True
	search.append([init[0],init[1]])
	currPath = []	#this will be the current state --> current path
	finalCost = math.inf

	print("The maze initially:")
	for elem in maze:
		print(' '.join(str(x) for x in elem))
	print("The initial cell is ["+str(init[0])+","+str(init[1])+"] and the goal cell is ["+str(goal[0])+","+str(goal[1])+"]\n")

	children = child(maze,init,visited)
	search = add(children,search)
	currPath = search[0]
	while len(search)!=0:
		print("Creating a path to the goal cell...")
		path,finalCost,search = creatingPath(maze,goal,search,currPath,visited,finalCost)
		print("The current cost is "+str(finalCost))
		print("The current best path is\n"+str(path))
		if(len(search)!=0): #if there are more alternative paths in the searching front
			currPath = search[0]
			visited = initializeVisited(currPath,visited)
		print("_________________________________________________________________________________________________________________________________________________________________________________________")

	print("\n BEST PATH FOUND\nThe searching front is empty, so every possible path was checked and the best path to take is the current path.")
	print("The best path to take from the cell ["+str(init[0])+","+str(init[1])+"] to the cell ["+str(goal[0])+","+str(goal[1])+"] is:\n"+str(path)+" with a cost of "+str(finalCost))
	maze = visualizeBestPath(path,maze)
	print("The best path to the Goal cell:")
	for elem in maze:
		print(' '.join(str(x) for x in elem))
	print("###########################################################################################################################################################################################\n")

#different maze examples

maze1 = [[0 for i in range(5)],
[0,1,1,1,0],
[0,1,0,1,1],
[0,1,0,1,0],
[1,1,1,1,0],
[0 for i in range(5)]]
BnB(maze1,[4,0],[2,4])
maze2 = [[0 for i in range(5)],
[0,1,1,1,0],
[0,1,0,1,0],
[0,1,0,1,0],
[0,1,1,1,1],
[0,1,0,0,0]]
BnB(maze2,[5,1],[4,4])
maze3 = [[0,1,0,0,0],
[0,1,1,1,0],
[0,1,0,1,0],
[0,1,0,1,0],
[0,1,1,1,0],
[0,1,0,0,0]]
BnB(maze3,[0,1],[5,1])
maze4 = [[1,1,1],
[1,0,1],
[1,1,1],
[1,0,1],
[1,0,1]]
BnB(maze4,[4,0],[4,2])
