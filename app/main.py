import bottle
import os
import random

map=[[]]

def removeBadDirections(ourSnake):
	safeDirections = ["up","down","left","right"]
	riskDirections = []
	#safe places to move:
	#  any empty space without a head nearby
	#  any tail that has a head not beside food
	#  any empty space that has a head beside it with a smaller ize than our snake
	head = ourSnake["coords"][0]
	### DANGER: invalid coordinate (wall) and another snake's body
	
	temp = mapValue(head[0]+1,head[1])
	if (temp == "invalid") or (temp == "body") or (temp[:4] == "head"):
		safeDirections.remove("right")
	if (temp == "tail danger"):
		riskDirections.add("right")
	local = [mapValue(head[0]+2,head[1]),mapValue(head[0]+1,head[1]-1),mapValue(head[0]+1,head[1]+1)]
	localHeads = [x for x in local if x[:4] == "head"]
	localDanger = [x for x in localHeads if int(x[5:]) >= len(ourSnake["coords"])]
	if localDanger:
		if "right" in safeDirections:
			safeDirections.remove("right")
		if not "right" in riskDirections:
			riskDirections.add("right")
			
			
	temp = mapValue(head[0]-1,head[1])
	if (temp == "invalid") or (temp == "body") or (temp[:4] == "head"):
		safeDirections.remove("left")
	if (temp == "tail danger"):
		riskDirections.add("left")
	local = [mapValue(head[0]-2,head[1]),mapValue(head[0]-1,head[1]-1),mapValue(head[0]-1,head[1]+1)]
	localHeads = [x for x in local if x[:4] == "head"]
	localDanger = [x for x in localHeads if int(x[5:]) >= len(ourSnake["coords"])]
	if localDanger:
		if "left" in safeDirections:
			safeDirections.remove("left")
		if not "left" in riskDirections:
			riskDirections.add("left")
			
		
	temp = mapValue(head[0],head[1]-1)
	if (temp == "invalid") or (temp == "body") or (temp[:4] == "head"):
		safeDirections.remove("up")
	if (temp == "tail danger"):
		riskDirections.add("up")
	local = [mapValue(head[0],head[1]-2),mapValue(head[0]-1,head[1]-1),mapValue(head[0]+1,head[1]-1)]
	localHeads = [x for x in local if x[:4] == "head"]
	localDanger = [x for x in localHeads if int(x[5:]) >= len(ourSnake["coords"])]
	if localDanger:
		if "up" in safeDirections:
			safeDirections.remove("up")
		if not "up" in riskDirections:
			riskDirections.add("up")
			
		
	temp = mapValue(head[0],head[1]+1)
	if (temp == "invalid") or (temp == "body") or (temp[:4] == "head"):
		safeDirections.remove("down")
	if (temp == "tail danger"):
		riskDirections.add("down")
	local = [mapValue(head[0],head[1]+2),mapValue(head[0]-1,head[1]+1),mapValue(head[0]+1,head[1]+1)]
	localHeads = [x for x in local if x[:4] == "head"]
	localDanger = [x for x in localHeads if int(x[5:]) >= len(ourSnake["coords"])]
	if localDanger:
		if "down" in safeDirections:
			safeDirections.remove("down")
		if not "down" in riskDirections:
			riskDirections.add("down")
			
		
	return [safeDirections,riskDirections]
	
def mapValue(xCord,yCord):
	width = len(map[0])
	height = len(map)
	if xCord < 0 or yCord < 0 or xCord >= width or yCord >= height:
		return "invalid"
	return map[xCord][yCord]

def generateMap(data):
	# might be nice to store the snake length in the head, and the local proximity to food in the tail
	map = [[]]*data["height"]
	for row in map:
		row = [""]*data["width"]
		
	for pellet in data["food"]:
		map[pellet[0]][pellet[1]] = "food"
		
	for snake in data["snakes"]:
		for coord in snake["coords"]:
			map[coord[0]][coord[1]] = "body"
		# store the body of the snake
		map[snake["coords"][0][0]][snake["coords"][0][1]] = "head %d".format(len(snake["coords"]))
		map[snake["coords"][-1][0]][snake["coords"][-1][1]] = "tail"
		# mark a snake as dangerous
		if mapValue(snake["coords"][0][0]+1,snake["coords"][0][1])=="food":
			map[snake["coords"][-1][0]][snake["coords"][-1][1]] = "tail danger"
		elif mapValue(snake["coords"][0][0]-1,snake["coords"][0][1])=="food":
			map[snake["coords"][-1][0]][snake["coords"][-1][1]] = "tail danger"
		elif mapValue(snake["coords"][0][0],snake["coords"][0][1]+1)=="food":
			map[snake["coords"][-1][0]][snake["coords"][-1][1]] = "tail danger"
		elif mapValue(snake["coords"][0][0],snake["coords"][0][1]-1)=="food":
			map[snake["coords"][-1][0]][snake["coords"][-1][1]] = "tail danger"

def shortestPath(moves, goal, self):
	#set default movement
	r = random.randint(0,len(moves))
	d = moves[r]
	
	#see if further horizontally or vertically
	if(abs(goal[0]-self["coords"][0][0]) < abs(goal[1]-self["coords"][0][1])):
		#move vertically
		if goal[1] > self["coords"][0][1] and 'down' in moves:
			d='down'
		elif goal[1] < self["coords"][0][1] and 'up' in moves:
			d='up'
	else:
		#move horizontally
		if goal[0] < self["coords"][0][0] and 'left' in moves:
			d='left'
		elif goal[0] > self["coords"][0][0] and 'right' in moves:
			d='right'
	return d
	
		
@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
	data = bottle.request.json
	game_id = data['game_id']
	board_width = data['width']
	board_height = data['height']

	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	# TODO: Do things with data

	return {
		'color': '#00FF00',
		'taunt': "Good luck, my friends!",
		'head_url': head_url,
		'name': 'Nice Snake',
		'head_type': 'pixel',
		'tail_type': 'pixel',
		'secondary_color': "#FF00FF"
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	
	'''#testing code
	d = ['up','down','left','right']
	r = random.randint(0,3)
	return {
		'move': d[r],
		'taunt': d[r]
	}'''
	
	#find self
	self = [s for s in data["snakes"] if s["id"] == data["you"]][0]
	
	#threshold between avoidance strategy and seeking food
	food_threshold = 50
	
	#eliminate impossible directions & choose random default move
	# step 1 - build game map
	generateMap(data)
	safeDirections, riskDirections = removeBadDirections(self)
	#temporary, combine the two lists
	mv = safeDirections+[x for x in riskDirections if not x in safeDirections]
	
	if(self["health_points"] > threshold or not data["food"]):
		#move to tail
		direction = shortestPath(mv, self["coords"][-1], self)
		
	else:
		#move to closest food
		#find closest food
		closest_food=data["food"][0]
		td0=10,000
		for pellet in data["food"]:
			hd1=pellet[0]-self["coords"][0][0]
			vd1=pellet[1]-self["coords"][0][1]
			td1=((hd1*hd1)+(vd1*vd1))
			if td1<td0:
				closest_food=pellet
				td0=td1

		direction = shortestPath(mv, pellet, self)
		#end of hungry
	
	#set taunt
	if data['turn']%4==0:
		tnta=[["This is so fun!"],["What a great day :)"],["All my fave snakes are here!"],["We'll all be dead eventually :)"],
			["I'm a loversnake, not a battlesnake <3"],["Battlesnakes? More like PARTYsnakes!"],["Thank you to the sponsors!"],
			[":D"],["Everyone here is so clever..."],["Golly!"],["What pretty snakes we have here today!"],["I should have prepared for this ahead of time..."],
			["Good job everybody!"]]
		t=random.randint(0,len(tnta))
		tnt=tnta[t]
	if data['turn'] < 4:
		tnt = "Good luck, my friends!"

	return {
		'move': direction,
		'taunt': tnt
	}

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
