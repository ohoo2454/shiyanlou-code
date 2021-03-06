#!/usr/bin/env python3
# coding:utf-8


class Stack(object):
    def __init__(self, limit=10):
        self.stack = []
        self.limit = limit

    def push(self, data):
        if (len(self.stack) >= self.limit):
            raise IndexError('Out of the range of the stack limit!')
        self.stack.append(data)

    def pop(self):
        if (self.stack):
            return self.stack.pop()
        else:
            raise IndexError('Pop from an empty stack!')

    def peek(self):
        if (self.stack):
            return self.stack[-1]

    def is_empty(self):
        return not bool(self.stack)

    def size(self):
        return len(self.stack)


def balanced_parentheses(parentheses):
    stack = Stack(len(parentheses))
    for parenthese in parentheses:
        if (parenthese == '('):
            stack.push(parenthese)
        elif (parenthese == ')'):
            if (stack.is_empty()):
                return False
            stack.pop()
    return stack.is_empty()


if (__name__ == '__main__'):
    examples = ['((()))', '((())', '(()))']
    print('Balanced parentheses demonstration:\n')
    for example in examples:
        print(example + ': ' + str(balanced_parentheses(example)))

