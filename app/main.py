import bottle
import os
import random

map=[[]]

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
		map[snake["coords"][0][0]][snake["coords"][0][1]] = "head %d".format(len(snake["coords"]))
		map[snake["coords"][-1][0]][snake["coords"][-1][1]] = "tail"

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
	
	#safe places to move:
	#  any empty space without a head nearby
	#  any tail that has a head not beside food
	#  any empty space that has a head beside it with a smaller size than our snake
	
	if(self["health_points"] > threshold):
		#move to tail
		direction = shortestPath(mv, self["coords"][-1], self)
		
	else:
		#move to closest food
		if not data["food"]:
			return{
				'move': mv[r], #THIS HAS TO CHANGE
				'taunt':tnt
			}

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

	# TODO: Do things with datax
	mv=['up','right','down','left']
	for snake in data['snakes']:
		for square in snake['coords']:
			if square[1]==self['coords'][0][1]:#neck is not above or below head
				if square[0]+1==self['coords'][0][0]:#neck is left of head
					mv.remove('left')
				elif square[0]-1==self['coords'][0][0]:#neck is right of head
					mv.remove('right')
			elif square[0]==self["coords"][0][0] and square[1]+1==self['coords'][0][1]:#neck is up of head
				mv.remove('up')
			elif square[0]==self["coords"][0][0] and square[1]-1==self['coords'][0][1]:#neck is down of head
				mv.remove('down')
	
		
	if self['coords'][0][0]==0:
		mv.remove('left')
	elif self['coords'][0][0]==data["width"]-1:
		mv.remove('right')
	elif self['coords'][0][1]==0:
		mv.remove('up')
	elif self['coords'][0][1]==data["height"]-1:
		mv.remove('down')
					
	
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
