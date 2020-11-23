#!/bin/usr/python3
import heapq


class PQ():

    def __init__(self):
        self._list = []
        self._index = 0

    def __len__(self):
        return self._index

    def push(self, obj, weight):
        heapq.heappush(self._list, (weight, -self._index, obj))
        self._index += 1

    def pop(self):
        if self._index > 0:
            self._index -= 1
            return heapq.heappop(self._list)[-1]
        return

    def top(self):
        if self._index > 0:
            return heapq.heappop(self._list)[-1]
        return

    def sneaky(self):
        return self._list

    def size(self):
        return self._index

    def isEmpty(self):
        return (self._index == 0)

    def empty(self):
        for x in range(self._index):
            self.pop()

    def display(self):
        for element in self._list:
            print (element)

    def dump(self):
        for x in range(self._index):
            print (self.pop())
