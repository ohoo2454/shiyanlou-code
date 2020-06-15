#!/usr/bin/env python3
#coding:utf-8

import curses
from random import randrange, choice
from collections import defaultdict

def main(stdsrc):

    def init():
        return 'Game'

    def not_game(state):
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    def game():
        if (action == 'Restart'):
            return 'Init'
        if (action == 'Exit'):
            return 'Exit'

            if (shengle):
                return 'Win'
            if (baile):
                return 'Gameover'
        return 'Game'


    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gamwover'),
            'Game': game
            }

    state = 'Init'

    while (state != 'Exit'):
        state = state_actions[state]()

