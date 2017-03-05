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
	r=random.randint(0,len(dir)-1)
	return {
		'move': dir[r],
		'taunt': "AHHH!"
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
