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
		'taunt': "YOU'RE GOING UP!",
		'head_url': head_url,
		'name': 'Nice Snake',
		'head_type': 'pixel',
		'tail_type': 'pixel',
		'secondary_color': "#FF00FF"
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	
	#testing code
	d = ['up','down','left','right']
	r = random.randint(0,3)
	return {
		'move': d[r],
		'taunt': d[r]
	}
	
	#find self
	for wolf in data["snakes"]:
		if wolf["id"]=="afdccc0a-2f55-4092-b5b7-b65ab9a30b1e":
			self=wolf
	
	#threshold between avoidance strategy and seeking food
	food_threshold = 50

	# TODO: Do things with datax
	r=random.randint(0,3)
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
	
	if data['turn']%4==0:
		tnta=[["This is so fun!"],["What a great day :)"],["All my fave snakes are here!"],["We'll all be dead eventually :)"],
			["I'm a loversnake, not a battlesnake <3"],["Battlesnakes? More like PARTYsnakes!"],["Thank you to the sponsors!"],
			[":D"],["Everyone here is so clever..."],["Golly!"],["What pretty snakes we have here today!"],["I should have prepared for this ahead of time..."],
			["Good job everybody!"]]
		t=random.randint(0,t.length)
		tnt=tnta[t]
	if data['turn'] < 4:
		tnt = "Good luck, my friends!"
		
	if self['coords'][0][0]==0:
		mv.remove('left')
	elif self['coords'][0][0]==data["width"]-1:
		mv.remove('right')
	elif self['coords'][0][1]==0:
		mv.remove('up')
	elif self['coords'][0][1]==data["height"]-1:
		mv.remove('down')
					
	if not data["food"]:
		return{
			'move': mv[r],
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

	if 'up' in mv: direction = 'up'
	elif 'right' in mv: direction = 'right'
	elif 'down' in mv: direction = 'down'
	elif 'left' in mv: direction = 'left'
	
	if closest_food[0]<self["coords"][0][0] and 'left' in mv:
		direction='left'
	elif closest_food[0]>self["coords"][0][0] and 'right' in mv:
		direction='right'
	elif closest_food[1]>self["coords"][0][1] and 'down' in mv:
		direction='down'


	return {
		'move': direction,
		'taunt': tnt
	}

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
