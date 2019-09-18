from random import random, randrange
from math import exp, sqrt
from graphics import *
from time import sleep

win = None

def genCities(numCities, dist):
	global win
	win = GraphWin("Annealing", dist, dist, False)
	cities = []
	for i in range(numCities):
		x = dist * random()
		y = dist * random()
		cities.append([x, y])
		Circle(Point(x, y), 3).draw(win)
	win.flush()
	return cities

def genPath(cities):
	path = []
	for i in range(len(cities)):
		path.append(cities[i])
	return path

def mutatePath(path):
	child = []
	for i in range(len(path)):
		child.append(path[i])
	i = randrange(len(path) - 1)
	j = randrange(len(path) - 1)
	child[i] = path[j]
	child[j] = path[i]
	return child

def getDist(city1, city2):
	return sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

lines = [];
def getCost(path):
	cost = 0
	for i in range(len(path) - 1):
		cost = cost + getDist(path[i], path[i + 1])
	return cost

def drawPath(path):
	drawing = [];
	for i in range(len(path) - 1):
		line = Line(
			Point(path[i][0], path[i][1]),
			Point(path[i + 1][0], path[i + 1][1])
		)
		drawing.append(line)
		line.draw(win)
	win.flush()
	sleep(0.01)
	return drawing

def undrawPath(drawing):
	for i in range(len(drawing)):
		drawing[i].undraw()

def anneal(desiredStability, startingTemp, cities):
	path = genPath(cities)
	drawing = drawPath(path)
	cost = getCost(path)
	sinceChange = 0
	temp = startingTemp
	while sinceChange < desiredStability:
		child = mutatePath(path)
		childCost = getCost(child)

		if childCost < cost:
			path = child
			cost = childCost
			undrawPath(drawing)
			drawing = drawPath(path)
			sinceChange = 0
		else:
			inside = (cost - childCost)/temp
			if random() < exp(inside):
				path = child
				cost = childCost
			else:
				sinceChange = sinceChange + 1
		temp = temp * 0.99
	sleep(1)
	undrawPath(drawing)
	return path, cost

dist = 800
numCities = 100
cities = genCities(numCities, dist)
for i in range(10):
	path, cost = anneal(1000, dist, cities)
	print(cost)