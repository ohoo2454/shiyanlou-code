#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *


def move_box(level, i):
	if level[i] == '-' or level[i] == '@':
		level[i] = '$'
	else:
		level[i] = '*'


def move_man(level, i):
	if level[i] == '-' or level[i] == '$':
		level[i] = '@'
	else:
		level[i] = '+'


def move_floor(level, i):
	if level[i] == '@' or level[i] == '$':
		level[i] = '-'
	else:
		level[i] = '.'


def get_offset(d, width):
	offset_map = {'l': -1, 'u': -width, 'r': 1, 'd': width}
	return offset_map[d.lower()]


class Sokoban(object):

	def __init__(self):
		self.level = list(
			"----#####----------"
			"----#---#----------"
			"----#$--#----------"
			"--###--$##---------"
			"--#--$-$-#---------"
			"###-#-##-#---######"
			"#---#-##-#####--..#"
			"#-$--$----------..#"
			"#####-###-#@##--..#"
			"----#-----#########"
			"----#######--------")
		self.w = 19
		self.h = 11
		self.man = 163
		self.solution = []
		self.push = 0
		self.todo = []

	def draw(self, screen, skin):
		w = skin.get_width() / 4
		for i in range(0, self.w):
			for j in range(0, self.h):
				item = self.level[j*self.w + i]
				if item == '#':
					screen.blit(skin, (i*w, j*w), (0, 2*w, w, w))
				elif item == '-':
					screen.blit(skin, (i*w, j*w), (0, 0, w, w))
				elif item == '@':
					screen.blit(skin, (i*w, j*w), (w, 0, w, w))
				elif item == '$':
					screen.blit(skin, (i*w, j*w), (2*w, 0, w, w))
				elif item == '.':
					screen.blit(skin, (i*w, j*w), (0, w, w, w))
				elif item == '+':
					screen.blit(skin, (i*w, j*w), (w, w, w, w))
				elif item == '*':
					screen.blit(skin, (i*w, j*w), (2*w, w, w, w))

	def move(self, d):
		self._move(d)
		self.todo = []

	def _move(self, d):
		h = get_offset(d, self.w)
		if self.level[self.man + h] == '-' or self.level[self.man + h] == '.':
			move_man(self.level, self.man + h)
			move_floor(self.level, self.man)
			self.man += h
			self.solution += d
		elif self.level[self.man + h] == '*' or \
				self.level[self.man + h] == '$':
			h2 = h * 2
			if self.level[self.man + h2] == '-' or \
					self.level[self.man + h2] == '.':
				move_box(self.level, self.man + h2)
				move_man(self.level, self.man + h)
				move_floor(self.level, self.man)
				self.man += h
				self.solution += d.upper()
				self.push += 1

	def undo(self):
		if self.solution.__len__() > 0:
			self.todo.append(self.solution[-1])
			self.solution.pop()
			h = get_offset(self.todo[-1], self.w) * -1
			if self.todo[-1].islower():
				move_man(self.level, self.man + h)
				move_floor(self.level, self.man)
				self.man += h
			else:
				move_floor(self.level, self.man - h)
				move_box(self.level, self.man)
				move_man(self.level, self.man + h)
				self.man += h
				self.push -= 1

	def redo(self):
		if self.todo.__len__() > 0:
			self._move(self.todo[-1].lower())
			self.todo.pop()


def main():
	pygame.init()
	screen = pygame.display.set_mode((400, 300))
	skinfilename = os.path.join('borgar.png')
	try:
		skin = pygame.image.load(skinfilename)
	except pygame.error as msg:
		print('cannot load skin.')
		raise SystemExit(msg)
	skin = skin.convert()
	screen.fill(skin.get_at((0, 0)))
	pygame.display.set_caption('Sokoban')
	skb = Sokoban()
	skb.draw(screen, skin)
	clock = pygame.time.Clock()
	pygame.key.set_repeat(200, 50)
	while True:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					skb.move('l')
					skb.draw(screen, skin)
				elif event.key == K_UP:
					skb.move('u')
					skb.draw(screen, skin)
				elif event.key == K_RIGHT:
					skb.move('r')
					skb.draw(screen, skin)
				elif event.key == K_DOWN:
					skb.move('d')
					skb.draw(screen, skin)
				elif event.key == K_BACKSPACE:
					skb.undo()
					skb.draw(screen, skin)
				elif event.key == K_SPACE:
					skb.redo()
					skb.draw(screen, skin)
		pygame.display.update()
		pygame.display.set_caption(skb.solution.__len__().__str__() + 
			'/' + skb.push.__str__() + ' - Sokoban')


if __name__ == '__main__':
	main()
