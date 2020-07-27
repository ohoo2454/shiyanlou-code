#!/usr/bin/env python3
#-*- coding: utf-8-*-

import random


class Matrix(object):
    def __init__(self, matrix, w, h):
        self.__matrix = matrix
        self.__width = w
        self.__height = h

    def __str__(self):
        ans = ""
        for i in range(self.__height):
            ans += "|"
            for j in range(self.__width):
                if j < self.__width - 1:
                    ans += str(self.__matrix[i][j]) + ","
                else:
                    ans += str(self.__matrix[i][j]) + "|\n"
        return ans

    def changeComponent(self, x, y, value):
        if x >= 0 and x < self.__height and y >= 0 and y <= self.__width:
            self.__matrix[x][y] = value
        else:
            raise Exception("changeComponent: indices out of bounds")

    def component(self, x, y):
        if x >= 0 and x < self.__height and y >= 0 and y <= self.__width:
            return self.__matrix[x][y]
        else:
            raise Exception("component: indices out of bounds")

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def __mul__(self, other):
        if isinstance(other, Vector):
            if (len(other) == self.__width):
                ans = zeroVector(self.__height)
                for i in range(self.__height):
                    summe = 0
                    for j in range(self.__width):
                        summe += other.component(j) * self.__matrix[i][j]
                    ans.changeComponent(i, summe)
                    summe = 0
                return ans
            else:
                raise Exception("vector must have the same size as the " + "number of columns of the matrix!")
        elif isinstance(other, int) or isinstance(other, float):
            matrix = [[self.__matrix[i][j] * other for j in range(self.__width)] for i in range(self.__height)]
            return Matrix(matrix, self.__width, self.__height)

    def __add__(self, other):
        if (self.__width == other.width() and self.__height == other.height()):
            matrix = []
            for i in range(self.__height):
                row = []
                for j in range(self.__width):
                    row.append(self.__matrix[i][j] + other.component(i, j))
                matrix.append(row)
            return Matrix(matrix, self.__width, self.__height)
        else:
            raise Exception("matrix must have the same dimension!")

    def __sub__(self, other):
        if (self.__width == other.width() and self.__height == other.height()):
            matrix = []
            for i in range(self.__height):
                row = []
                for j in range(self.__width):
                    row.append(self.__matrix[i][j] - other.component(i, j))
                matrix.append(row)
            return Matrix(matrix, self.__width, self.__height)
        else:
            raise Exception("matrix must have the same dimension!")

    def randomMatrix(W, H, a, b):
        random.seed(None)
        matrix = [[random.randint(a, b) for j in range(W)] for i in range(H)]
        return Matrix(matrix, W, H)

