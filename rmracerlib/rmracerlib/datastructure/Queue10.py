#!/bin/usr/python3
class Queue10:
    '''
    A Stack that only holds 10 items, nothing more, nothing less
    '''
    def __init__(self, size):
        self._list = [0] * size
        self._index = 0
        self.size = size
        self.total = 0
        
    def put(self, value=0):
        self._list[self._index] = value
        self._increment()
        return self.total

    def _increment(self):
        if self._index == self.size - 1:
            self._index = 0
        else:
            self._index += 1
        self.total = sum(self._list)

    def clear(self):
        for x in range(0, self.size - 1):
            self.put(0)

    def sneaky(self):
        return self._list
