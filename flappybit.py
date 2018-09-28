import microbit
from time import sleep
from random import randint
# from . import classes  # Relative imports don't work (TODO: workaround?)


# Global variables
level = 1
deaths = 0
meteors = []
deathmessages = {
	5: 'git gud',
	10: 'git gudder',
	20: 'never gonna give you up',
	21: 'never gonna let you down',
	22: 'never gonna run around and desert you',
	23: 'never gonna make you cry',
	24: 'never gonna say goodbye',
	25: 'never gonna tell a lie and hurt you',
	50: 'wow you\'re really trying'
}
startanimation1 = microbit.Image("99000:"
                                 "99900:"
                                 "09050:"
                                 "00525:"
                                 "00205")
startanimation2 = microbit.Image("99000:"
                                 "99900:"
                                 "09502:"
                                 "00550:"
                                 "00205")
startanimation3 = microbit.Image("99000:"
                                 "99900:"
                                 "09250:"
                                 "00505:"
                                 "00002")


class Movable:
	x = None
	y = None
	outside = False
	brightness = 9

	def move(self, oldx, oldy, x, y):
		self.x = x
		self.y = y
		microbit.display.set_pixel(oldx, oldy, 0)
		microbit.display.set_pixel(x, y, self.brightness)

	def move_relative(self, x, y):
		microbit.display.set_pixel(self.x, self.y, 0)
		if valid_coords(self.x + x, self.y + y):
			self.move(self.x, self.y, self.x + x, self.y + y)
		else:
			self.outside = True

	def render(self):
		microbit.display.set_pixel(self.x, self.y, self.brightness)


class Meteor(Movable):
	def __init__(self):
		self.x = randint(0, 4)
		self.y = 0
		self.brightness = 4
		self.render()


class Player(Movable):
	def __init__(self):
		self.x = 2
		self.y = 3
		self.alive = True
		self.render()


def valid_coords(x, y):  # Check if coords are on screen
	return 0 <= x <= 4 and 0 <= y <= 4  # Chained comparison fuckery


player = Player()
def player_loop():
	if microbit.button_a.was_pressed():
		player.move_relative(-1, 0)
	elif microbit.button_b.was_pressed():
		player.move_relative(1, 0)


# Object loops (TODO: clean up and move to object or main loop)
def meteor_loop():
	for meteor in meteors:
		if not meteor.outside:
			meteor.move_relative(0, 1)
			if meteor.x == player.x and meteor.y == player.y:  # Player hit: game over
				deaths += 1
				if deaths in deathmessages:
					microbit.display.scroll(deathmessages[deaths])
				microbit.reset()  # Restart the whole micro:bit, temporary solition as we will need to count deaths in the future. TODO: restart() function that clears all objects and respawns them
		else:
			meteor.move(meteor.x, meteor.y, randint(0, 4), 0)
			meteor.outside = False
	if len(meteors) < level:
		meteors.append(Meteor())


#homescreen
while not microbit.button_a.is_pressed() and not microbit.button_b.is_pressed():
    microbit.display.show(startanimation1)
    sleep(0.15)
    microbit.display.show(startanimation2)
    sleep(0.15)
    microbit.display.show(startanimation3)
    sleep(0.15)
microbit.display.clear()


# Main loop
while True:
	player_loop()
	sleep(0.33)
	meteor_loop()
	player_loop()
	sleep(0.33)
	player_loop()
	sleep(0.33)