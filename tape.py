'''класс представляющий бесконечную ленту в одну сторону'''
class Tape:
    '''конструктор класса'''
    def __init__(self, input_list:list):
        self.tape = input_list # список чисел
        self.head = 0 # каретка
    '''чтение текущего значения'''
    def read(self):
        return self.tape[self.head]
    '''чтение всей ленты'''
    def read_all_tape(self):
        return self.tape
    '''проверка на возможность сдвига влево'''
    def can_left(self):
        if self.head == 0:
            return False
        return True
    '''сдвиг влево'''
    def left(self):
        if not self.can_left():
            return False
        self.head -=1
        return True
    '''сдвиг вправо'''
    def right(self):
        self.head +=1
    '''декремент для текущего значения ячейки'''
    def raw_decrement(self):
        self.tape[self.head] -= 1
    '''инкремент для текущего значения ячейки'''
    def raw_increment(self):
        self.tape[self.head] += 1
    '''операция декремент'''
    def decrement(self):
        s = set(self.tape)
        if len(s) == 1 and s.pop() == 0:
            return False
        while self.head != len(self.tape)-1:
            self.right()
        while self.read() == 0:
            self.raw_increment()
            if not self.can_left():
                return False
            else:
                self.left()
        self.tape[self.head] -= 1
        if 1 in self.tape:
            self.tape = self.tape[self.tape.index(1):]
        return True

    '''операция инкримент'''
    def increment(self):
        self.head = 0
        while self.head != len(self.tape)-1:
            self.right()
        while self.read() > 0:
            if not self.can_left():
                self.tape.extend([0])
                self.head = 0
                return
            else:
                self.raw_decrement()
                self.left()
        self.tape[self.head] += 1

