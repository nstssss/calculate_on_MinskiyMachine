from tape import Tape
class Register:
    def __init__(self, input_list:list, name:str):
        self.tape = Tape(input_list)
        self.name = name

    def read(self):
        return self.tape.read()

    def read_all(self):
        return self.tape.read()

    def increment(self):
        self.tape.increment()

    def decrement(self):
        self.tape.decrement()