#!/usr/bin/env python3
#coding:utf-8


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Linked_List:
    def __init__(self, head=None):
        self.head = head

    def append(self, new_element):
        current = self.head
        if (self.head):
            while (current.next):
                current = current.next
            current.next = new_element
        else:
            self.head = new_element

    def is_empty(self):
        return not self.head

    def get_length(self):
        temp = self.head
        length = 0
        while (temp != None):
            length += 1
            temp = temp.next
        return length

    def insert(self, position, new_element):
        if (position < 0 or position > self.get_length()):
            raise IndexError('when insert, key out of range.')
        temp = self.head
        if (position == 0):
            new_element.next, self.head = temp, new_element
            return
        i = 0
        while (i < position):
            pre, temp = temp, temp.next
            i += 1
        pre.next, new_element.next = new_element, temp

    def print_list(self):
        print('linked_list: ')
        temp = self.head
        new_list = []
        while (temp is not None):
            new_list.append(temp.data)
            temp = temp.next
        print(new_list)

    def remove(self, position):
        if (position < 0 or position > self.get_length()-1):
            raise IndexError('when remove, key out of range.')
        i = 0
        temp = self.head
        while (temp != None):
            if (position == 0):
                self.head = temp.next
                temp.next = None
                return True
            pre, temp = temp, temp.next
            i += 1
            if (i == position):
                pre.next, temp.next = temp.next, None
                return

    def reverse(self):
        prev = None
        current = self.head
        while (current):
            next_node, current.next = current.next, prev
            prev, current = current, next_node
        self.head = prev

    def initlist(self, data_list):
        self.head = Node(data_list[0])
        temp = self.head
        for i in data_list[1:]:
            node = Node(i)
            temp.next = node
            temp = temp.next

