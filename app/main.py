import bottle
import os
import random
import pprint

DEBUG = True

taunts = [
  "Don't tread on me!",
  "Full of MSG!",
  "ABCDEFG",
  "testing!"
]

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    if (DEBUG):
        print "/start"
        pprint.pprint(data)

    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00FF00',
        'taunt': random.choice(taunts),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }

def find_our_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id : return snake

def find_distance_from_walls(snake, board_height, board_width):
    snake_head_pos = snake['coords'][0]
    return {
        'north': snake_head_pos[1],
        'east': board_width - snake_head_pos[0] - 1,
        'south': board_height - snake_head_pos[1],
        'west': snake_head_pos[0],
    }

@bottle.post('/move')
def move():
    data = bottle.request.json

    if (DEBUG):
        print "/move"
        pprint.pprint(data)

    board_width = data['width']
    board_height = data['height']

    directions = ['up', 'down', 'left', 'right']
    valid_direction = False
    our_snake = find_our_snake(data['you'], data['snakes'])
    wall_distances = find_distance_from_walls(our_snake, board_height, board_width)
    chosen_direction = None

    while valid_direction == False:
        chosen_direction = random.choice(directions)
        if chosen_direction == 'up':
            if wall_distances['north'] > 0:
                valid_direction = True
        elif chosen_direction == 'right':
            if wall_distances['east'] > 0:
                valid_direction = True
        elif chosen_direction == 'down':
            if wall_distances['south'] > 0:
                valid_direction = True
        else:
            if wall_distances['west'] > 0:
                valid_direction = True

    return {
        'move': chosen_direction,
        'taunt': 'battlesnake-python!'
    }
\
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
