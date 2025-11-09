from register import Register
from transit import *

'''Реализация машины Минского и  калькулятора чисел на ней'''
class MinskyMachine:
    """конструктор класса"""
    def __init__(self, registers_count: int, new_register: bool):
        self.registers = [0] * registers_count
        self.current_index = 0
        self.registers_count = registers_count
        self.new_register = new_register

    """загрузка чисел в регистры"""
    def load_numbers(self, numbers: dict):
        if len(numbers) != self.registers_count and len(numbers) != self.registers_count - 1:
            return
        l_dict = list(numbers)
        l_values = list(numbers.values())

        for i in range(len(numbers)):
            key = l_dict[i]
            value = l_values[i]
            self.registers[i] = Register(value, key)

    def load_program(self, program: list):
        self.program = program

    """получение регистра"""
    def get_reg(self, name):
        for i in self.registers:
            if i.name == name:
                return i
        return None

    """шаг выполнения программы"""
    def step(self):
        instruction = self.program[self.current_index]
        register = instruction.register
        operation = instruction.type

        current_reg = self.get_reg(register)
        if operation == Operations.increment:
            current_reg.increment()
            self.current_index = instruction.move[0]
        elif operation == Operations.decrement:
            result = current_reg.decrement()
            if not result:
                self.current_index = instruction.move[1]
            else:
                self.current_index = instruction.move[0]

    """выполнение программы"""
    def run(self):
        while self.current_index != -1 and self.current_index <= (len(self.program) - 1):
            self.step()

        i = 0
        if self.new_register:
            i = len(self.registers) - 1

        binary_list = self.registers[i].read_all()
        return self.binary_to_number(binary_list)

    """перевод числа из 2-ой СС в 10"""
    def binary_to_number(self, binary_list: list) -> int:
        result = 0
        for bit in binary_list:
            result = result * 2 + bit
        return result

    """перевод числа из 10-ой СС в 2"""
    def number_to_binary(self, num: int) -> list:
        if num == 0:
            return [0]
        bits = []
        while num > 0:
            bits.append(num % 2)
            num //= 2
        return bits[::-1]

    """складывает числа на машине минского"""
    def add(self, numbers: list[int]) -> int:
        binaries = [self.number_to_binary(n) for n in numbers]
        #загрузка чисел в регистры
        self.registers_count = len(numbers)
        self.registers = [0] * self.registers_count
        register_names = [chr(ord('A') + i) for i in range(self.registers_count)]
        data = {register_names[i]: binaries[i] for i in range(len(numbers))}
        self.load_numbers(data)

        for i in range(1, self.registers_count):
            donor = register_names[i]  # что добавляем
            target = register_names[0]  # к чему добавляем

            # Программа: переносим все единицы из donor в target
            program = [
                Transition(0, donor, [1, -1], Operations.decrement),
                Transition(1, target, [0, 0], Operations.increment),
            ]

            self.load_program(program)
            self.current_index = 0

            # Выполняем до тех пор, пока donor не станет пустым
            self.run()
        #запись результата
        binary_result = self.registers[0].read_all()
        result = self.binary_to_number(binary_result)
        return result

    """операция вычитания двух чисел"""
    def sub(self, numbers: list[int]) -> int:

        self.registers = [0] * 2
        self.registers_count = 2
        a = numbers[0]
        b = numbers[1]
        bin_a = self.number_to_binary(a)
        bin_b = self.number_to_binary(b)
        self.load_numbers({"A": bin_a, "B": bin_b})

        #Программа:
        program = [
            Transition(0, "B", [1, -1], Operations.decrement),  # если B не ноль -> 1
            Transition(1, "A", [0, 0], Operations.decrement),  # уменьшаем A, возвращаемся
        ]
        self.load_program(program)
        self.current_index = 0
        self.run()
        binary_result = self.registers[0].read_all()
        result = self.binary_to_number(binary_result)
        return result
# Тест
if __name__ == "__main__":
    machine = MinskyMachine(2, True)
    print("2 + 3 + 5 =", machine.add([2, 3, 5, 5]))
    print("105 - 15 = ", machine.sub([105, 15]))
    # print("2 + 3 =", machine.add_numbers([2, 3]))
    # print("5 + 7 =", machine.add_numbers([5, 7]))
    # print("0 + 4 =", machine.add_numbers([0, 4]))
