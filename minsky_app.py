import sys
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QMessageBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QSplitter, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from minsky import MinskyMachine
import re


class HistoryDB:
    def __init__(self):
        pass

    def add_record(self, operation_type, expression, result):
        """Добавление новой записи в бд с указанием типа операции"""
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO history (operation, numbers, result, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (operation_type, expression, str(result), timestamp))
        conn.commit()
        conn.close()

    def get_all_records(self):
        """Получение всех записей"""
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT operation, numbers, result, timestamp 
            FROM history 
            ORDER BY timestamp DESC
        ''')
        records = cursor.fetchall()
        conn.close()
        return records

    def clear_history(self):
        """Очистка истории"""
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history')
        conn.commit()
        conn.close()


class MinskyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.machine = MinskyMachine()
        self.history_db = HistoryDB()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Машина Минского")
        self.setGeometry(200, 100, 1200, 600)

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Создаем разделитель для калькулятора и истории
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Левая панель - калькулятор
        calculator_widget = QWidget()
        calculator_layout = QVBoxLayout(calculator_widget)

        # Заголовок
        title = QLabel("Калькулятор на Машине Минского")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        calculator_layout.addWidget(title)

        # Инструкция
        instruction = QLabel("Введите выражение: ")
        instruction.setFont(QFont("Arial", 12))
        instruction.setAlignment(Qt.AlignCenter)
        calculator_layout.addWidget(instruction)

        # Поле ввода
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Consolas", 14))
        self.input_field.setFixedHeight(40)
        calculator_layout.addWidget(self.input_field)

        # Кнопка
        button = QPushButton("Вычислить")
        button.setFont(QFont("Arial", 12, QFont.Bold))
        button.setFixedHeight(40)
        button.clicked.connect(self.evaluate_expression)
        calculator_layout.addWidget(button)

        # Поле результата
        self.result_label = QLabel("Результат: ")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignCenter)
        calculator_layout.addWidget(self.result_label)

        calculator_layout.addStretch()

        # Правая панель - история
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)

        history_title = QLabel("История вычислений")
        history_title.setFont(QFont("Arial", 16, QFont.Bold))
        history_title.setAlignment(Qt.AlignCenter)
        history_layout.addWidget(history_title)

        # Таблица истории
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Операция", "Выражение", "Результат", "Время"])
        self.history_table.horizontalHeader().setStretchLastSection(True)

        # Настраиваем ширину колонок
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Операция по содержимому
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Выражение растягивается
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Результат по содержимому
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Время по содержимому

        history_layout.addWidget(self.history_table)

        # очистка истории
        history_buttons_layout = QHBoxLayout()

        self.clear_btn = QPushButton("Очистить историю")
        self.clear_btn.clicked.connect(self.clear_history)
        history_buttons_layout.addWidget(self.clear_btn)

        history_layout.addLayout(history_buttons_layout)

        # Добавляем панели в разделитель
        splitter.addWidget(calculator_widget)
        splitter.addWidget(history_widget)
        splitter.setSizes([500, 500])

        # Загружаем историю при запуске
        self.load_history()

    def evaluate_expression(self):
        expr = self.input_field.text().strip()
        if not expr:
            QMessageBox.warning(self, "Ошибка", "Введите выражение")
            return

        # Проверяем допустимые символы
        if not re.fullmatch(r"[0-9+\-*/\s]+", expr):
            QMessageBox.warning(self, "Ошибка", "Разрешены только цифры и знаки + - * /")
            return

        try:
            # Разделяем на части: числа и операторы
            tokens = re.findall(r'\d+|[+\-*/]', expr)
            if len(tokens) < 3:
                QMessageBox.warning(self, "Ошибка", "Введите корректное выражение (например 5+3)")
                return

            # Определяем тип операции на основе используемых операторов
            operation_type = self.detect_operation_type(tokens)

            # Начинаем с первого числа
            result = int(tokens[0])

            i = 1
            while i < len(tokens):
                op = tokens[i]
                num = int(tokens[i + 1])
                if op == '+':
                    result = self.machine.add([result, num])
                elif op == '-':
                    result = self.machine.sub([result, num])
                elif op == '*':
                    result = self.machine.mul([result, num])
                elif op == '/':
                    if num == 0:
                        raise ZeroDivisionError
                    result = self.machine.div([result, num])
                i += 2

            # Отображаем результат
            result_text = f"Результат: {result}"
            self.result_label.setText(result_text)

            # СОХРАНЯЕМ В БАЗУ ДАННЫХ С ТИПОМ ОПЕРАЦИИ
            self.history_db.add_record(operation_type, expr, result)

            # ОБНОВЛЯЕМ ТАБЛИЦУ ИСТОРИИ
            self.load_history()

        except ZeroDivisionError:
            QMessageBox.critical(self, "Ошибка", "Деление на ноль невозможно!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")

    def detect_operation_type(self, tokens):
        """Определяет тип операции на основе используемых операторов"""
        operators = set(tokens[1::2])  # Берем только операторы (каждый второй элемент начиная с 1)

        if len(operators) == 1:
            op = list(operators)[0]
            if op == '+':
                return "Сложение"
            elif op == '-':
                return "Вычитание"
            elif op == '*':
                return "Умножение"
            elif op == '/':
                return "Деление"

        # Если несколько разных операторов
        return "Комбинированное выражение"

    def load_history(self):
        """Загрузка истории в таблицу"""
        records = self.history_db.get_all_records()
        self.history_table.setRowCount(len(records))

        for row, record in enumerate(records):
            operation, expression, result, timestamp = record
            self.history_table.setItem(row, 0, QTableWidgetItem(operation))
            self.history_table.setItem(row, 1, QTableWidgetItem(expression))
            self.history_table.setItem(row, 2, QTableWidgetItem(result))
            self.history_table.setItem(row, 3, QTableWidgetItem(timestamp))

    def clear_history(self):
        """Очистка истории"""
        reply = QMessageBox.question(self, "Очистка истории",
                                     "Вы уверены, что хотите очистить всю историю вычислений?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.history_db.clear_history()
            self.load_history()
            QMessageBox.information(self, "История очищена", "История вычислений была успешно очищена.")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MinskyApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()