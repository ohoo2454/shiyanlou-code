#!/usr/bin/env python3
#coding:utf-8

import curses
from random import randrange, choice
from collections import defaultdict


class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = 2048
        self.score = 0
        self.highscore = 0
        self.reset()

    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2

        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height)
                 if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):
        if (self.score > self.highscore):
            self.highscore = self.score
        self.score = 0

        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()


def get_user_action(keyboard):
    char = 'N'
    while (char not in actions_dict):
        char = keyboard.getch()

    return actions_dict[char]





def main(stdsrc):

    def init():
        game_field.reset()
        return 'Game'

    def not_game(state):
        game_field.draw(stdsrc)
        action = get_user_action(stdsrc)
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    def game():
        game_field.draw(stdsrc)
        action = get_user_action(stdsrc)

        if (action == 'Restart'):
            return 'Init'
        if (action == 'Exit'):
            return 'Exit'
        if (game_field.move(action)):
            if (game_field.is_win()):
                return 'Win'
            if (game_field.is_gameover()):
                return 'Gameover'
        return 'Game'


    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gamwover'),
            'Game': game
            }

    curses.use_default_colors()

    game_field = GameField(win=2048)


    state = 'Init'

    while (state != 'Exit'):
        state = state_actions[state]()

curses.wrapper(main)

