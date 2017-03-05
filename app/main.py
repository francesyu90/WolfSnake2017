import bottle
import os
import random

		
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
		'taunt': "Good luck, my friends!!!",
		'head_url': head_url,
		'name': 'Nice Snake',
		'head_type': 'pixel',
		'tail_type': 'pixel',
		'secondary_color': "#FF00FF"
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	#find self
	self = [s for s in data["snakes"] if s["id"] == data["you"]][0]
	
	#threshold between avoidance strategy and seeking food
	food_threshold = 50
	
	
	dir = ['up','down','left','right']
	last = self["coords"][1]
	head = self["coords"][0]
	if head[0] > last[0]:
		dir = ['up','down','right']
	elif head[0] < last[0]:
		dir = ['up','down','left']
	elif head[1] > last[1]:
		dir = ['down','left','right']
	elif head[1] < last[1]:
		dir = ['up','left','right']
	left = head.copy()
	right=head.copy()
	up=head.copy()
	down=head.copy()
	left[0]-=1
	right[0]+=1
	up[1]-=1
	down[1]+=1
	for snake in data["snakes"]:
		if up in snake["coords"]:
			up = [-1,-1]
		if down in snake["coords"]:
			down = [-1,-1]
		if left in snake["coords"]:
			left = [-1,-1]
		if right in snake["coords"]:
			right = [-1,-1]
	if right[0] == data['height']:
		right == [-1,-1]
	if down[1] == data['height']:
		down == [-1,-1]
	mv =[]
	if not -1 in down and 'down' in dir:
		mv += ['down']
	
	if not -1 in right and 'right' in dir:
		mv += ['right']
	
	if not -1 in left and 'left' in dir:
		mv += ['left']
	
	if not -1 in up and 'up' in dir:
		mv += ['up']
	
	r=random.randint(0,len(mv))
	return {
		'move': mv[r],
		'taunt': "AHHH!"
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
