import sqlite3
import re
from datetime import datetime
from minsky import MinskyMachine


class HistoryDB:
    def __init__(self, db_path="history.db"):
        self.db_path = db_path

    def add_record(self, operation_type, expression, result):
        """Добавление записи в базу данных с указанием типа операции"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO history (operation, numbers, result, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (operation_type, expression, str(result), timestamp))

        conn.commit()
        conn.close()

    def get_all_records(self):
        """Получение всех записей из базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT operation, numbers, result, timestamp
            FROM history
            ORDER BY timestamp DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def clear_history(self):
        """Очистка всей истории вычислений"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        conn.commit()
        conn.close()


class MinskyConsoleApp:
    def __init__(self):
        self.machine = MinskyMachine()
        self.history_db = HistoryDB()

    def detect_operation_type(self, tokens):
        """Определяет тип операции на основе используемых операторов"""
        operators = set(tokens[1::2])  # Берем только операторы

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

    def print_menu(self):
        """Вывод главного меню"""
        print("\n" + "=" * 50)
        print("       Машина Минского — Консольный калькулятор")
        print("=" * 50)
        print("1. Вычислить выражение")
        print("2. Показать историю вычислений")
        print("3. Очистить историю")
        print("4. Выход")
        print("-" * 50)

    def evaluate_expression(self):
        """Вычисление математического выражения"""
        expr = input("\nВведите выражение: ").strip()

        if not expr:
            print("Ошибка: выражение не может быть пустым.")
            return

        # Проверяем допустимые символы
        if not re.fullmatch(r"[0-9+\-*/\s]+", expr):
            print("Ошибка: разрешены только цифры и знаки + - * /")
            return

        # Разделяем на токены
        tokens = re.findall(r'\d+|[+\-*/]', expr)

        if len(tokens) < 3:
            print("Ошибка: выражение слишком короткое (пример: 5+3).")
            return

        try:
            # Определяем тип операции
            operation_type = self.detect_operation_type(tokens)

            # Вычисляем результат
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
                        print("Ошибка: деление на ноль!")
                        return
                    result = self.machine.div([result, num])
                i += 2

            print(f"\nРезультат: {result}")

            # Сохраняем в базу данных с типом операции
            self.history_db.add_record(operation_type, expr, result)
            print("Запись сохранена в историю.")

        except Exception as e:
            print(f"Ошибка при вычислении: {e}")

    def show_history(self):
        """Отображение истории вычислений"""
        rows = self.history_db.get_all_records()
        if not rows:
            print("\nИстория вычислений пуста.")
            return

        print("\n" + "=" * 70)
        print("                      ИСТОРИЯ ВЫЧИСЛЕНИЙ")
        print("=" * 70)
        print(f"{'Операция':<20} {'Выражение':<25} {'Результат':<10} {'Время':<15}")
        print("-" * 70)

        for op, expr, result, ts in rows:
            # Обрезаем длинные выражения для лучшего отображения
            display_expr = expr if len(expr) <= 23 else expr[:20] + "..."
            print(f"{op:<20} {display_expr:<25} {result:<10} {ts:<15}")

    def clear_history(self):
        """Очистка истории вычислений"""
        confirm = input("\nВы уверены, что хотите удалить всю историю вычислений? (y/n): ")
        if confirm.lower() == 'y':
            self.history_db.clear_history()
            print("История вычислений очищена.")
        else:
            print("Операция отменена.")

    def run(self):
        """Главный цикл приложения"""
        print("Добро пожаловать в калькулятор на Машине Минского!")

        while True:
            self.print_menu()
            choice = input("\nВыберите пункт меню (1-4): ").strip()

            if choice == "1":
                self.evaluate_expression()
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                self.clear_history()
            elif choice == "4":
                print("\nСпасибо за использование калькулятора! До свидания!")
                break
            else:
                print("Ошибка: выберите пункт от 1 до 4.")

            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    MinskyConsoleApp().run()