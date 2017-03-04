import bottle
import os
import random

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = 'http://wallpapersinhq.pw/images/big/scarface-148756.jpg' 
    #'%s://%s/static/head.png' % (
     #   bottle.request.urlparts.scheme,
      #  bottle.request.urlparts.netloc
    #)

    return {
        'color': '#000048',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': "I'm hangry!"
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    
    #find self
    for wolf in data["snakes"]:
        if wolf["id"]=="afdccc0a-2f55-4092-b5b7-b65ab9a30b1e":
            self=wolf
    


    # TODO: Do things with datax
    r=random.randint(0,3)
    mv=['north','east','south','west']
    for snake in data['snakes']:
        for square in snake['coords']:
            if square[1]==self['coords'][0][1]:#neck is not above or below head
                if square[0]+1==self['coords'][0][0]:#neck is west of head
                    mv.remove('west')
                elif square[0]-1==self['coords'][0][0]:#neck is east of head
                    mv.remove('east')
            elif square[0]==self["coords"][0][0] and square[1]+1==self['coords'][0][1]:#neck is north of head
                mv.remove('north')
            elif square[0]==self["coords"][0][0] and square[1]-1==self['coords'][0][1]:#neck is south of head
                mv.remove('south')
    
    if data['turn']%5==0:
        t=random.randint(0,7)
        tnta=[["You're going up!"],['Baaaaa'],['You look in a mirror. You see me'],['haHAAAA!'],['What is looove?'],["Baby don't hurt meeeee"],['Predicting your loss is easy'],['I will never truly die']]
        tnt=tnta[t]
        
    if self['coords'][0][0]==0:
        mv.remove('west')
    elif self['coords'][0][0]==data["width"]-1:
        mv.remove('east')
    elif self['coords'][0][1]==0:
        mv.remove('north')
    elif self['coords'][0][1]==data["height"]-1:
        mv.remove('south')
                    
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

    if 'north' in mv: direction = 'north'
    elif 'east' in mv: direction = 'east'
    elif 'south' in mv: direction = 'south'
    elif 'west' in mv: direction = 'west'
    
    if closest_food[0]<self["coords"][0][0] and 'west' in mv:
        direction='west'
    elif closest_food[0]>self["coords"][0][0] and 'east' in mv:
        direction='east'
    elif closest_food[1]>self["coords"][0][1] and 'south' in mv:
        direction='south'


    return {
        'move': direction,
        'taunt': tnt
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': "It's all over!"
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
