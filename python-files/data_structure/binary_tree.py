#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Node(object):

    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.item)

class Tree(object):

    def __init__(self):
        self.root = Node('root')

    def add(self, item):
        node = Node(item)
        if self.root is None:
            self.root = node
        else:
            q = [self.root]
            while True:
                pop_node = q.pop(0)
                if pop_node.left is None:
                    pop_node.left = node
                    return
                elif pop_node.right is None:
                    pop_node.right = node
                    return
                else:
                    q.append(pop_node.left)
                    q.append(pop_node.right)

    def get_parent(self, item):
        if self.root.item == item:
            return None
        tmp = [self.root]
        while tmp:
            pop_node = tmp.pop(0)
            if pop_node.left and pop_node.left.item == item:
                return pop_node
            if pop_node.right and pop_node.right.item == item:
                return pop_node
            if pop_node.left is not None:
                tmp.append(pop_node.left)
            if pop_node.right is not None:
                tmp.append(pop_node.right)
        return None

    def delete(self, item):
        if self.root is None:
            return False

        parent = self.get_parent(item)
        if parent:

