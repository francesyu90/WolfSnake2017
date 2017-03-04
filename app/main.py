import bottle
import os
import random

map=[[]]

def removeBadDirections(ourSnake):
	directions = ["up","down","left","right"]
	#safe places to move:
	#  any empty space without a head nearby
	#  any tail that has a head not beside food
	#  any empty space that has a head beside it with a smaller ize than our snake
	head = ourSnake["coords"][0]
	### DANGER: invalid coordinate (wall) and another snake's body
	if (mapValue(head[0]+1,head[1]) == "invalid") or (mapValue(head[0]+1,head[1]) == "body") or (mapValue(head[0]+1,head[1]) == "head"):
		directions.remove("right")
	if (mapValue(head[0]-1,head[1]) == "invalid") or (mapValue(head[0]-1,head[1]) == "body") or (mapValue(head[0]-1,head[1]) == "head"):
		directions.remove("left")
	if (mapValue(head[0],head[1]-1) == "invalid") or (mapValue(head[0],head[1]-1) == "body") or (mapValue(head[0],head[1]-1) == "head"):
		directions.remove("up")
	if (mapValue(head[0],head[1]+1) == "invalid") or (mapValue(head[0],head[1]+1) == "body") or (mapValue(head[0],head[1]+1) == "head"):
		directions.remove("down")
	
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
	if 'up' in moves: d = 'up'
	elif 'right' in moves: d = 'right'
	elif 'down' in moves: d = 'down'
	elif 'left' in moves: d = 'left'
	
	#take shortest path to food
	if goal[0]<self["coords"][0][0] and 'left' in moves:
		d='left'
	elif goal[0]>self["coords"][0][0] and 'right' in moves:
		d='right'
	elif goal[1]>self["coords"][0][1] and 'down' in moves:
		d='down'
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
	directions = removeBadDirections(self)
	
	
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
