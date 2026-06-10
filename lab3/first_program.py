"""
Занятие 3. Первая программа на Python.
Демонстрирует базовые конструкции языка:
ввод/вывод, условия, циклы, обработку ошибок.
"""

import random

def greet_user():
    """Приветствие и знакомство с пользователем."""
    print("=" * 40)
    print("  Добро пожаловать в мир Python!")
    print("=" * 40)

    name = input("\nВведитевашеимя: ")
    print(f"Приятно познакомиться, {name}!")
    return name


def calculator():
    """Простой калькулятор с обработкой ошибок."""
    print("\n--- Калькулятор ---")
    try:
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))
    except ValueError:
        print("Ошибка: введите корректное число!")
        return 
    
    operations = {
            "+": a + b,
            "-": a - b,
            "*": a * b,
        }

    # Деление с проверкой на ноль
    if b != 0:
        operations["/"] = a / b
    else:
        operations["/"] = "деление на ноль невозможно"

    print(f"\nРезультаты для {a} и {b}:")
    for op, result in operations.items():
        print(f"  {a} {op} {b} = {result}")


def number_game():
    """Игра: угадай число (демонстрация цикла while)."""
    

    print("\n--- Угадайчислоот 1 до 20 ---")
    secret = random.randint(1, 20)
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        try:
            guess = int(input(f"Попытка {attempts + 1}/{max_attempts}: "))
        except ValueError:
            print("Введитецелоечисло!")
            continue

        attempts += 1

        if guess == secret:
            print(f"Поздравляем! Угадали за {attempts} попыток!")
            return
        elif guess < secret:
            print("Больше!")
        else:
            print("Меньше!")

    print(f"Число было: {secret}. Попробуйте еще раз!")


def show_multiplication_table():
    """Таблица умножения (демонстрация вложенных циклов)."""
    print("\n--- Таблица умножения ---")
    try:
        n = int(input("Для какого числа (1-10): "))
    except ValueError:
        n = 5

    for i in range(1, 11):
        print(f"  {n} x {i:2d} = {n * i:3d}")


def main():
    name = greet_user()
    calculator()
    number_game()
    show_multiplication_table()
    print(f"\nСпасибо за работу, {name}! Довстречи!")


if __name__ == "__main__":
    main()
