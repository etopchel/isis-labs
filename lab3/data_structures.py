"""
Занятие 3. Работа с коллекциями данных Python.
Списки, словари, множества, генераторы.
"""


def demo_lists():
    """Демонстрация работы со списками."""
    print("=== Списки ===")

    students = ["Иванов", "Петров", "Сидоров", "Козлова", "Новикова"]
    print(f"Студенты: {students}")
    print(f"Количество: {len(students)}")
    print(f"Первый: {students[0]}, Последний: {students[-1]}")

    # Добавление и удаление
    students.append("Морозов")
    students.insert(0, "Алексеев")
    print(f"После добавления: {students}")

    # Срезы
    print(f"Первые три: {students[:3]}")

    # Сортировка
    students.sort()
    print(f"Отсортированные: {students}")

    # Генераторсписка
    lengths = [len(s) for s in students]
    print(f"Длиныфамилий: {lengths}")


def demo_dicts():
    """Демонстрация работы со словарями."""
    print("\n=== Словари ===")

    grades = {
        "Иванов": [5, 4, 5, 3, 5],
        "Петров": [4, 4, 4, 4, 5],
        "Сидоров": [3, 3, 4, 3, 3],
    }
    print("Средниеоценки:")
    for student, marks in grades.items():
        avg = sum(marks) / len(marks)
    print(f"  {student}: {avg:.2f}")

    # Фильтрация: студенты со средним >= 4
    good_students = {
        name: marks 
        for name, marks in grades.items()
        if sum(marks) / len(marks) >= 4
    }
    print(f"Хорошисты и отличники: {list(good_students.keys())}")


def demo_sets():
    """Демонстрация работы с множествами."""
    print("\n=== Множества ===")

    group_a = {"Python", "JavaScript", "SQL", "HTML"}
    group_b = {"Java", "Python", "C++", "SQL"}

    print(f"Группа A: {group_a}")
    print(f"Группа B: {group_b}")
    print(f"Общие: {group_a&group_b}")
    print(f"Всевместе: {group_a | group_b}")
    print(f"Тольков A: {group_a - group_b}")


if __name__ == "__main__":
    demo_lists()
    demo_dicts()
    demo_sets()
