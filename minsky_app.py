import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from minsky import MinskyMachine


class Minsky_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.machine = MinskyMachine(2, True)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Машина Минского")
        self.setGeometry(400, 150, 1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title = QLabel("Калькулятор на Машине Минского")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Добавляем вкладки
        self.tabs.addTab(self.create_tab("Сложение", "+"), "Сложение")
        self.tabs.addTab(self.create_tab("Вычитание", "-"), "Вычитание")
        self.tabs.addTab(self.create_tab("Умножение", "*"), "Умножение")
        self.tabs.addTab(self.create_tab("Деление", "/"), "Деление")

    def create_tab(self, name: str, op_symbol: str):
        """Создаёт вкладку для указанной операции"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        instruction = QLabel(f"Введите числа через пробел для операции {name.lower()}:")
        instruction.setFont(QFont("Arial", 11))
        layout.addWidget(instruction)

        input_field = QTextEdit()
        input_field.setPlaceholderText("Например: 20 5 4")
        input_field.setFixedHeight(60)
        layout.addWidget(input_field)

        button = QPushButton(f"Выполнить {name.lower()}")
        button.setFixedHeight(35)
        layout.addWidget(button)

        result_label = QLabel("Результат: ")
        result_label.setFont(QFont("Arial", 12))
        layout.addWidget(result_label)

        # Привязка события
        button.clicked.connect(lambda: self.run_operation(input_field, result_label, op_symbol))

        return tab

    """Обработка ввода и выполнение расчёта"""
    def run_operation(self, input_field, result_label, op_symbol):
        text = input_field.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка ввода", "Пустое поле")
            return

        try:
            numbers = list(map(int, text.split()))
            if (len(numbers) < 2):
                QMessageBox.warning(self, "Ошибка ввода", "Для выполнения операции должно быть минимум 2 числа")
                return
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Можно вводить только целые числа!")
            return

        if any(n < 0 for n in numbers):
            result_label.setText("Результат: Ошибка — отрицательные числа не поддерживаются.")
            return

        try:
            if op_symbol == '+':
                result = self.machine.add(numbers)
            elif op_symbol == '-':
                result = self.machine.sub(numbers)
            elif op_symbol == '*':
                result = self.machine.mul(numbers)
            elif op_symbol == '/':
                result = self.machine.div(numbers)
            else:
                raise ValueError("Неизвестная операция")

            result_label.setText(f"Результат: {result}")
        except ZeroDivisionError:
            QMessageBox.critical(self, "Ошибка", "Деление на ноль невозможно!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка выполнения", f"Произошла ошибка: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Minsky_app()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
