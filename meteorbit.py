import microbit
import math
from time import sleep
from random import randint


# Global variables
level = 1
deaths = 0
dodged_meteors = 0
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
startanimation1 = microbit.Image(
	"99000:"
	"99900:"
	"09050:"
	"00525:"
	"00205"
)
startanimation2 = microbit.Image(
	"99000:"
	"99900:"
	"09502:"
	"00550:"
	"00205"
)
startanimation3 = microbit.Image(
	"99000:"
	"99900:"
	"09250:"
	"00505:"
	"00002"
)
boomanimation1 = microbit.Image(
	"00000:"
	"00300:"
	"03030:"
	"00300:"
	"00000"
)
boomanimation2 = microbit.Image(
	"00200:"
	"02220:"
	"22022:"
	"02220:"
	"00200"
)
boomanimation3 = microbit.Image(
	"01110:"
	"10001:"
	"10001:"
	"10001:"
	"01110"
)


# Classes
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


# Game functions
def valid_coords(x, y):  # Check if coords are on screen
	return 0 <= x <= 4 and 0 <= y <= 4  # Chained comparison fuckery


def restart():
	del meteors[:]  # Delete everything in meteors list using Python magic
	global level
	level = 1
	global dodged_meteors
	dodged_meteors = 0
	player.x = 2
	player.y = 3
	player.alive = False
	player.render()


def special_ability():
	del meteors[:]
	microbit.display.clear()
	microbit.display.show(boomanimation1)
	sleep(0.1)
	microbit.display.show(boomanimation2)
	sleep(0.1)
	microbit.display.show(boomanimation3)
	sleep(0.1)
	microbit.display.clear()
	player.render()


# Object ticks
def meteor_tick():
	for meteor in meteors:
		if not meteor.outside:
			meteor.move_relative(0, 1)
		else:
			meteor.move(meteor.x, meteor.y, randint(0, 4), 0)
			meteor.outside = False
			global dodged_meteors
			dodged_meteors += 1
	if len(meteors) < level:
		meteors.append(Meteor())


player = Player()
def player_tick():
	button_a = microbit.button_a.was_pressed()  # This function resets to False every time it's called, which means we have to store it into a variable in order to check it multiple times
	button_b = microbit.button_b.was_pressed()

	if microbit.button_a.is_pressed() and microbit.button_b.is_pressed():
		special_ability()
	elif button_a:
		if valid_coords(player.x - 1, player.y):
			player.move_relative(-1, 0)
	elif button_b:
		if valid_coords(player.x + 1, player.y):
			player.move_relative(1, 0)

	for meteor in meteors:
		if meteor.x == player.x and meteor.y == player.y:  # Player hit: game over
			global deaths  # Make the deaths variable accessible in this scope
			deaths += 1
			microbit.display.clear()
			sleep(0.5)
			microbit.display.scroll(dodged_meteors)
			sleep(1)
			microbit.display.clear()
			if deaths in deathmessages:
				microbit.display.scroll(deathmessages[deaths])
				sleep(0.5)
			restart()


# Starting screen
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
	# Tl;DR: One loop is 1 second. The player tick runs three times, meteor tick once.
	player_tick()
	sleep(0.2)
	meteor_tick()
	player_tick()
	sleep(0.2)
	player_tick()
	sleep(0.2)
	if level <= 10:
		level += 0.05