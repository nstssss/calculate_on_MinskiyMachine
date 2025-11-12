from enum import Enum
'''перечисление операций мащины Минского'''
class Operations(Enum):
    increment = 1
    decrement = 2

'''класс, представляющий инструкцию перехода в ММ'''
class Transition:
    def __init__(self, index: int, register : str, move:list, operation : Operations):
        self.index = index # номер шага в программе
        self.register = register # регистр, к которому применяется операция
        self.move = move # перемещение
        self.type = operation # тип операции

