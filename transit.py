from enum import Enum
class Operations(Enum):
    increment = 1
    decrement = 2

'''класс, представляющий инструкцию перехода в ММ'''
class Transition:
    def __init__(self, index: int, register : str, move:list, operation : Operations):
        self.index = index
        self.register = register
        self.move = move
        self.type = operation

