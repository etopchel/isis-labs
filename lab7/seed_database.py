"""
Занятие 7. Заполнение базы данных тестовыми данными.
Подключение к PostgreSQL и выполнение SQL-запросов.
"""
import psycopg2
from datetime import date, timedelta
import random
 
 
# Параметры подключения (измените под свою БД)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "student_db",
    "user": "postgres",
    "password": "123",
}
 
 
def create_tables(cursor):
    """Создание таблиц."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            year INTEGER NOT NULL
        );
 
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            group_id INTEGER REFERENCES groups(id),
            email VARCHAR(255)
        );
 
        CREATE TABLE IF NOT EXISTS subjects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            hours INTEGER NOT NULL
        );
 
        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(id),
            subject_id INTEGER REFERENCES subjects(id),
            grade INTEGER CHECK (grade BETWEEN 2 AND 5),
            date DATE NOT NULL
        );
    """)
    print("Таблицы созданы.")
 
 
def seed_data(cursor):
    """Заполнение тестовыми данными."""
    # Группы
    groups_data = [("ИС-21", 2021), ("ИС-22", 2022), ("ИС-23", 2023)]
    for name, year in groups_data:
        cursor.execute(
            "INSERT INTO groups (name, year) VALUES (%s, %s)",
            (name, year)
        )
 
    # Студенты
    last_names = ["Иванов", "Петров", "Сидоров", "Козлова",
                  "Новикова", "Морозов", "Волкова", "Алексеев",
                  "Лебедева", "Кузнецов"]
    first_names = ["Алексей", "Мария", "Дмитрий", "Анна",
                   "Елена", "Сергей", "Ольга", "Павел",
                   "Ирина", "Андрей"]
 
    for i in range(10):
        cursor.execute(
            "INSERT INTO students (last_name, first_name, "
            "group_id, email) VALUES (%s, %s, %s, %s)",
            (last_names[i], first_names[i],
             random.randint(1, 3),
             f"{last_names[i].lower()}@student.edu")
        )
 
    # Предметы
    subjects_data = [
        ("Инструментальные средства ИС", 72),
        ("Базы данных", 108),
        ("Программирование на Python", 144),
    ]
    for name, hours in subjects_data:
        cursor.execute(
            "INSERT INTO subjects (name, hours) VALUES (%s, %s)",
            (name, hours)
        )
 
    # Оценки (случайные)
    base_date = date(2025, 9, 1)
    for student_id in range(1, 11):
        for subject_id in range(1, 4):
            cursor.execute(
                "INSERT INTO grades (student_id, subject_id, "
                "grade, date) VALUES (%s, %s, %s, %s)",
                (student_id, subject_id,
                 random.choice([3, 4, 4, 5, 5]),
                 base_date + timedelta(days=random.randint(0, 90)))
            )
 
    print("Данные загружены.")
 
 
def show_sample_queries(cursor):
    """Примеры SQL-запросов."""
    print("\n--- Все студенты группы ИС-22 ---")
    cursor.execute("""
        SELECT s.last_name, s.first_name, g.name as group_name
        FROM students s
        JOIN groups g ON s.group_id = g.id
        WHERE g.name = 'ИС-22'
        ORDER BY s.last_name
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]} {row[1]} ({row[2]})")
 
    print("\n--- Средние оценки по предметам ---")
    cursor.execute("""
        SELECT sub.name, ROUND(AVG(gr.grade), 2) as avg_grade
        FROM grades gr
        JOIN subjects sub ON gr.subject_id = sub.id
        GROUP BY sub.name
        ORDER BY avg_grade DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
 
 
def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
 
    create_tables(cursor)
    seed_data(cursor)
    show_sample_queries(cursor)
 
    cursor.close()
    conn.close()
    print("\nГотово!")
 
 
if __name__ == "__main__":
    main()

