import pytest
from minsky import MinskyMachine

@pytest.fixture
def machine():
    return MinskyMachine()

'''Тесты со стандартными значениями'''
class Test_base:
    """ тесты операции сложения"""
    def test_add(self, machine):
        assert(machine.add([5, 4, 5, 2]) == 16)
        assert(machine.add([0, 10, 30, 40, 50, 60]) == 190)
        assert(machine.add([100, 200, 0, 300, 1000]) == 1600)

    """ тесты операции вычитания"""
    def test_sub(self, machine):
        assert machine.sub([1000, 7]) == 993
        assert(machine.sub([90, 10, 5, 5]) == 70)
        assert machine.sub([333, 222, 111])== 0

    """ тесты операции умножения """
    def test_mul(self ,machine):
        assert(machine.mul([5, 4, 5, 2]) == 200)
        assert machine.mul([0, 10, 30, 40, 50, 0]) == 0
        assert machine.mul([1, 2, 3, 4, 5]) == 120

    """ тесты операции деления """
    def test_div(self, machine):
        assert machine.div([50, 5, 10]) == 1
        assert machine.div([100, 20, 5]) == 1
        assert machine.div([900, 5, 2]) == 90

''' Тесты на граничных значениях'''
class Test_limits:
    """ тесты для операции сложенич"""
    def test_add(self, machine):
        assert machine.add([20000000, 20000000]) == 40000000
        assert machine.add([15233456, 2134567, 1000000, 345634]) == 18713657

    """ тесты для операции вычитания"""
    def test_sub(self, machine):
        assert machine.sub([20000000, 20000000]) == 0
        assert  machine.sub([9876543, 1234567, 1593575]) == 7048401

    """ тесты для операуии умножения"""
    def test_mul(self, machine):
        assert machine.mul([10000, 2000]) == 20000000
        assert machine.mul([5000, 4000]) == 20000000

    """ тесты для операции деления"""
    def test_div(self, machine):
        assert machine.div([20000000, 2000000]) == 10
        assert machine.div([19232322, 2351]) == 8180

''' Тесты для исключельных значений'''
class Test_exceptions:
    """ тесты для операции сложения"""
    def test_add(self, machine):
        assert machine.add([-114, -11, -110, -120]) == None
        assert machine.add([-12, -300, -200]) == None
        assert machine.add([200.5, 300.5]) == None
        assert machine.add([20, 11.5, 5, 5]) == None

    """ тесты для операции вычитания"""
    def test_sub(self, machine):
        assert machine.sub([-1, -11, -110, -120]) == None
        assert machine.sub([-12, -300, -200]) == None
        assert machine.div([200.5, 300.5]) == None
        assert machine.div([20, 10, 20]) == 0

    """ тесты для операции  умножения"""
    def test_mul(self, machine):
        assert machine.mul([-114, -11, -110, -120]) == None
        assert machine.mul([-12, -300, -200]) == None
        assert machine.mul([200.5, 300.5]) == None
        assert machine.mul([20, 11.5, 5, 5]) == None

    """ тесты для операции деления"""
    def test_div(self, machine):
        assert machine.div([-1, -11, -110, -120]) == None
        assert machine.div([-12, -300, -200]) == None
        assert machine.div([200.5, 300.5]) == None
        assert machine.div([2, 5, 5, 5]) == 0
        assert machine.div([28, 8]) == 3




