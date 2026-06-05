from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
 
app = Flask(__name__)
CORS(app)  # Разрешить кросс-доменные запросы
 
# Параметры БД (измените под свои)
DB_CONFIG = {
    "host": "localhost",
    "database": "student_db",
    "user": "postgres",
    "password": "your_password",
}
 
 
def get_db():
    """Создает подключение к БД."""
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn
 
 
# ========== STUDENTS API ==========
 
@app.route("/api/students", methods=["GET"])
def get_students():
    """Получить список всех студентов."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.last_name, s.first_name,
               s.email, g.name as group_name
        FROM students s
        LEFT JOIN groups g ON s.group_id = g.id
        ORDER BY s.last_name
    """)
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(students)
 
 
@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Получить студента по ID."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
 
    if not student:
        abort(404, description="Студент не найден")
    return jsonify(student)
 
 
@app.route("/api/students", methods=["POST"])
def create_student():
    """Создать нового студента."""
    data = request.get_json()
 
    if not data or not data.get("last_name") or not data.get("first_name"):
        abort(400, description="Укажите last_name и first_name")
 
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (last_name, first_name, group_id, email) "
        "VALUES (%s, %s, %s, %s) RETURNING *",
        (data["last_name"], data["first_name"],
         data.get("group_id"), data.get("email"))
    )
    new_student = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_student), 201
 
 
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """Обновить данные студента."""
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET last_name=%s, first_name=%s, "
        "group_id=%s, email=%s WHERE id=%s RETURNING *",
        (data.get("last_name"), data.get("first_name"),
         data.get("group_id"), data.get("email"), student_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
 
    if not updated:
        abort(404, description="Студент не найден")
    return jsonify(updated)
 
 
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Удалить студента."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s RETURNING id",
                (student_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
 
    if not deleted:
        abort(404, description="Студент не найден")
    return jsonify({"message": "Удалено", "id": student_id})
 
 
# ========== GRADES API ==========
 
@app.route("/api/students/<int:student_id>/grades", methods=["GET"])
def get_student_grades(student_id):
    """Получить оценки студента."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT g.id, g.grade, g.date,
               s.name as subject_name
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        ORDER BY g.date DESC
    """, (student_id,))
    grades = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(grades)
 
 
# ========== ERROR HANDLERS ==========
 
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e.description)}), 404
 
 
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e.description)}), 400
 
 
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500
 
 
if __name__ == "__main__":
    print("Запуск сервера: http://localhost:5000")
    app.run(debug=True, port=5000)
