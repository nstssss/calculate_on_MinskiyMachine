from tape import Tape
'''класс регистра ММ'''
class Register:
    def __init__(self, input_list:list, name:str):
        self.tape = Tape(input_list) # содержимое регистра
        self.name = name # название регистра

    """ чтение текущего значения регистра"""
    def read(self):
        return self.tape.read()

    """ чтение всего содержимого регистра"""
    def read_all(self):
        return self.tape.read_all_tape()

    """ операция инкримент"""
    def increment(self):
        self.tape.increment()

    """операция декримент"""
    def decrement(self):
        return self.tape.decrement()