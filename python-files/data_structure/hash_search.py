#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class HashTable(object):

    def __init__(self, size):
        self.elem = [None for i in range(size)]
        self.count = size

    def hash(self, key):
        return key % self.count

    def insert_hash(self, key):
        address = self.hash(key)
        while self.elem[address]:
            address = (address+1) % self.count
        self.elem[address] = key

    def search_hash(self, key):
        star = address = self.hash(key)
        while self.elem[address] != key:
            address = (address+1) % self.count
            if not self.elem[address] or address == star:
                return False
        return True, address


if __name__ == '__main__':
    list_a = [12, 67, 56, 16, 25, 37, 22, 29, 15, 47, 48, 34]
    hash_table = HashTable(12)
    for i in list_a:
        hash_table.insert_hash(i)
    for i in hash_table.elem:
        if i:
            print((i, hash_table.elem.index(i)), end=" ")
    print("\n")
    print(hash_table.search_hash(15))
    print(hash_table.search_hash(33))

