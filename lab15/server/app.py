from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Параметры БД
DB_CONFIG = {
    "host": "localhost",
    "database": "dance_studio",
    "user": "postgres",
    "password": "123",
}


def get_db():
    """Создает подключение к БД."""
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn


def get_user_by_login(login):
    """Находит пользователя по логину."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = %s", (login,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ========== AUTH ==========

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    """Регистрация нового пользователя."""
    data = request.get_json()

    if not data or not data.get("login") or not data.get("password") or not data.get("user_type"):
        abort(400, description="Укажите login, password и user_type")

    if data["user_type"] not in ("student", "teacher"):
        abort(400, description="user_type должен быть student или teacher")

    if get_user_by_login(data["login"]):
        abort(400, description="Логин уже занят")

    conn = get_db()
    cur = conn.cursor()

    # Создаем пользователя
    cur.execute(
        "INSERT INTO users (login, password, user_type) VALUES (%s, %s, %s) RETURNING *",
        (data["login"], data["password"], data["user_type"])
    )
    user = cur.fetchone()

    # Создаем профиль (student или teacher)
    if data["user_type"] == "student":
        cur.execute(
            "INSERT INTO students (name, user_id) VALUES (%s, %s) RETURNING *",
            (data.get("name", "Новый студент"), user["id"])
        )
        profile = cur.fetchone()
    else:
        cur.execute(
            "INSERT INTO teachers (name, user_id) VALUES (%s, %s) RETURNING *",
            (data.get("name", "Новый преподаватель"), user["id"])
        )
        profile = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"user": user, "profile": profile}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    """Вход в систему."""
    data = request.get_json()

    if not data or not data.get("login") or not data.get("password"):
        abort(400, description="Укажите login и password")

    user = get_user_by_login(data["login"])
    if not user or user["password"] != data["password"]:
        abort(401, description="Неверный логин или пароль")

    conn = get_db()
    cur = conn.cursor()

    # Загружаем профиль
    if user["user_type"] == "student":
        cur.execute("SELECT * FROM students WHERE user_id = %s", (user["id"],))
    else:
        cur.execute("SELECT * FROM teachers WHERE user_id = %s", (user["id"],))
    profile = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({"user": user, "profile": profile})


# ========== STUDENTS ==========

@app.route("/api/students", methods=["GET"])
def get_students():
    """Получить список всех студентов."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY name")
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(students)


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Получить данные студента."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()

    if not student:
        abort(404, description="Студент не найден")
    return jsonify(student)


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """Обновить данные студента."""
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE students SET name=%s, phone=%s, email=%s, sex=%s, age=%s "
        "WHERE id=%s RETURNING *",
        (data.get("name"), data.get("phone"), data.get("email"),
         data.get("sex"), data.get("age"), student_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        abort(404, description="Студент не найден")
    return jsonify(updated)


# ========== TEACHERS ==========

@app.route("/api/teachers/<int:teacher_id>", methods=["GET"])
def get_teacher(teacher_id):
    """Получить данные преподавателя."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
    teacher = cur.fetchone()
    cur.close()
    conn.close()

    if not teacher:
        abort(404, description="Преподаватель не найден")
    return jsonify(teacher)


@app.route("/api/teachers/<int:teacher_id>", methods=["PUT"])
def update_teacher(teacher_id):
    """Обновить данные преподавателя."""
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE teachers SET name=%s, phone=%s, email=%s, sex=%s, age=%s "
        "WHERE id=%s RETURNING *",
        (data.get("name"), data.get("phone"), data.get("email"),
         data.get("sex"), data.get("age"), teacher_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        abort(404, description="Преподаватель не найден")
    return jsonify(updated)


# ========== STYLES ==========

@app.route("/api/styles", methods=["GET"])
def get_styles():
    """Получить список стилей."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM styles ORDER BY name")
    styles = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(styles)


@app.route("/api/styles", methods=["POST"])
def create_style():
    """Создать новый стиль."""
    data = request.get_json()

    if not data or not data.get("name"):
        abort(400, description="Укажите name")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO styles (name) VALUES (%s) RETURNING *",
        (data["name"],)
    )
    new_style = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_style), 201


@app.route("/api/styles/<int:style_id>", methods=["PUT"])
def update_style(style_id):
    """Обновить стиль."""
    data = request.get_json()

    if not data or not data.get("name"):
        abort(400, description="Укажите name")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE styles SET name=%s WHERE id=%s RETURNING *",
        (data["name"], style_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        abort(404, description="Стиль не найден")
    return jsonify(updated)


@app.route("/api/styles/<int:style_id>", methods=["DELETE"])
def delete_style(style_id):
    """Удалить стиль."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM styles WHERE id=%s RETURNING id", (style_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        abort(404, description="Стиль не найден")
    return jsonify({"message": "Удалено", "id": style_id})


# ========== GROUPS ==========

@app.route("/api/groups", methods=["GET"])
def get_groups():
    """Получить список групп (с названием стиля)."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT g.*, s.name as style_name
        FROM groups_ g
        LEFT JOIN styles s ON g.style_id = s.id
        ORDER BY g.name
    """)
    groups = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(groups)


@app.route("/api/groups", methods=["POST"])
def create_group():
    """Создать новую группу."""
    data = request.get_json()

    if not data or not data.get("name"):
        abort(400, description="Укажите name")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO groups_ (name, age_from, age_to, style_id) "
        "VALUES (%s, %s, %s, %s) RETURNING *",
        (data["name"], data.get("age_from"), data.get("age_to"), data.get("style_id"))
    )
    new_group = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_group), 201


@app.route("/api/groups/<int:group_id>", methods=["PUT"])
def update_group(group_id):
    """Обновить группу."""
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE groups_ SET name=%s, age_from=%s, age_to=%s, style_id=%s "
        "WHERE id=%s RETURNING *",
        (data.get("name"), data.get("age_from"), data.get("age_to"),
         data.get("style_id"), group_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        abort(404, description="Группа не найдена")
    return jsonify(updated)


@app.route("/api/groups/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    """Удалить группу."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM groups_ WHERE id=%s RETURNING id", (group_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        abort(404, description="Группа не найдена")
    return jsonify({"message": "Удалено", "id": group_id})


# ========== STUDENTS IN GROUPS ==========

@app.route("/api/groups/<int:group_id>/students", methods=["GET"])
def get_group_students(group_id):
    """Получить список студентов группы."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.name, s.phone, s.email, s.age
        FROM students s
        JOIN student_group sg ON s.id = sg.student_id
        WHERE sg.group_id = %s
        ORDER BY s.name
    """, (group_id,))
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(students)


@app.route("/api/groups/<int:group_id>/students", methods=["POST"])
def add_student_to_group(group_id):
    """Добавить студента в группу."""
    data = request.get_json()

    if not data or not data.get("student_id"):
        abort(400, description="Укажите student_id")

    conn = get_db()
    cur = conn.cursor()

    # Проверяем что группа существует
    cur.execute("SELECT id FROM groups_ WHERE id = %s", (group_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        abort(404, description="Группа не найдена")

    # Проверяем что студент существует
    cur.execute("SELECT id FROM students WHERE id = %s", (data["student_id"],))
    if not cur.fetchone():
        cur.close()
        conn.close()
        abort(404, description="Студент не найден")

    try:
        cur.execute(
            "INSERT INTO student_group (student_id, group_id) VALUES (%s, %s) RETURNING *",
            (data["student_id"], group_id)
        )
        result = cur.fetchone()
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        cur.close()
        conn.close()
        abort(400, description="Студент уже в этой группе")

    cur.close()
    conn.close()
    return jsonify(result), 201


@app.route("/api/groups/<int:group_id>/students/<int:student_id>", methods=["DELETE"])
def remove_student_from_group(group_id, student_id):
    """Удалить студента из группы."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM student_group WHERE student_id=%s AND group_id=%s RETURNING *",
        (student_id, group_id)
    )
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        abort(404, description="Студент не найден в этой группе")
    return jsonify({"message": "Удалено"})


# ========== PROGRAMS ==========

@app.route("/api/programs", methods=["GET"])
def get_programs():
    """Получить список программ (с названием стиля)."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*, s.name as style_name
        FROM programs p
        LEFT JOIN styles s ON p.style_id = s.id
        ORDER BY p.name
    """)
    programs = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(programs)


@app.route("/api/programs", methods=["POST"])
def create_program():
    """Создать новую программу."""
    data = request.get_json()

    if not data or not data.get("name"):
        abort(400, description="Укажите name")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO programs (name, style_id, track, duration) "
        "VALUES (%s, %s, %s, %s) RETURNING *",
        (data["name"], data.get("style_id"), data.get("track"), data.get("duration"))
    )
    new_program = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_program), 201


@app.route("/api/programs/<int:program_id>", methods=["PUT"])
def update_program(program_id):
    """Обновить программу."""
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE programs SET name=%s, style_id=%s, track=%s, duration=%s "
        "WHERE id=%s RETURNING *",
        (data.get("name"), data.get("style_id"), data.get("track"),
         data.get("duration"), program_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        abort(404, description="Программа не найдена")
    return jsonify(updated)


@app.route("/api/programs/<int:program_id>", methods=["DELETE"])
def delete_program(program_id):
    """Удалить программу."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM programs WHERE id=%s RETURNING id", (program_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        abort(404, description="Программа не найдена")
    return jsonify({"message": "Удалено", "id": program_id})


# ========== LESSONS ==========

@app.route("/api/lessons", methods=["GET"])
def get_lessons():
    """Получить список уроков с фильтром по дате."""
    date_filter = request.args.get("date")

    conn = get_db()
    cur = conn.cursor()

    if date_filter:
        cur.execute("""
            SELECT l.*, g.name as group_name, p.name as program_name
            FROM lessons l
            LEFT JOIN groups_ g ON l.group_id = g.id
            LEFT JOIN programs p ON l.program_id = p.id
            WHERE DATE(l.datetime_start) = %s
            ORDER BY l.datetime_start
        """, (date_filter,))
    else:
        cur.execute("""
            SELECT l.*, g.name as group_name, p.name as program_name
            FROM lessons l
            LEFT JOIN groups_ g ON l.group_id = g.id
            LEFT JOIN programs p ON l.program_id = p.id
            ORDER BY l.datetime_start
        """)

    lessons = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lessons)


@app.route("/api/lessons", methods=["POST"])
def create_lesson():
    """Создать новый урок."""
    data = request.get_json()

    if not data or not data.get("group_id") or not data.get("program_id"):
        abort(400, description="Укажите group_id и program_id")
    if not data.get("datetime_start") or not data.get("datetime_end"):
        abort(400, description="Укажите datetime_start и datetime_end")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lessons (group_id, program_id, datetime_start, datetime_end) "
        "VALUES (%s, %s, %s, %s) RETURNING *",
        (data["group_id"], data["program_id"],
         data["datetime_start"], data["datetime_end"])
    )
    new_lesson = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_lesson), 201


@app.route("/api/lessons/<int:lesson_id>", methods=["PUT"])
def update_lesson(lesson_id):
    """Обновить урок."""
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE lessons SET group_id=%s, program_id=%s, "
        "datetime_start=%s, datetime_end=%s WHERE id=%s RETURNING *",
        (data.get("group_id"), data.get("program_id"),
         data.get("datetime_start"), data.get("datetime_end"), lesson_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        abort(404, description="Урок не найден")
    return jsonify(updated)


@app.route("/api/lessons/<int:lesson_id>", methods=["DELETE"])
def delete_lesson(lesson_id):
    """Удалить урок."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM lessons WHERE id=%s RETURNING id", (lesson_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        abort(404, description="Урок не найден")
    return jsonify({"message": "Удалено", "id": lesson_id})


# ========== STUDENT: МОИ ГРУППЫ И УРОКИ ==========

@app.route("/api/me/groups", methods=["GET"])
def get_my_groups():
    """Получить группы студента (по user_id)."""
    user_id = request.args.get("user_id")

    if not user_id:
        abort(400, description="Укажите user_id")

    conn = get_db()
    cur = conn.cursor()

    # Находим студента по user_id
    cur.execute("SELECT id FROM students WHERE user_id = %s", (user_id,))
    student = cur.fetchone()
    if not student:
        cur.close()
        conn.close()
        abort(404, description="Студент не найден")

    cur.execute("""
        SELECT g.*, s.name as style_name
        FROM groups_ g
        JOIN student_group sg ON g.id = sg.group_id
        LEFT JOIN styles s ON g.style_id = s.id
        WHERE sg.student_id = %s
        ORDER BY g.name
    """, (student["id"],))
    groups = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(groups)


@app.route("/api/me/lessons", methods=["GET"])
def get_my_lessons():
    """Получить уроки студента (по user_id), опционально фильтр future/past."""
    user_id = request.args.get("user_id")
    period = request.args.get("period")  # future или past

    if not user_id:
        abort(400, description="Укажите user_id")

    conn = get_db()
    cur = conn.cursor()

    # Находим студента по user_id
    cur.execute("SELECT id FROM students WHERE user_id = %s", (user_id,))
    student = cur.fetchone()
    if not student:
        cur.close()
        conn.close()
        abort(404, description="Студент не найден")

    query = """
        SELECT l.*, g.name as group_name, p.name as program_name
        FROM lessons l
        JOIN groups_ g ON l.group_id = g.id
        JOIN programs p ON l.program_id = p.id
        JOIN student_group sg ON g.id = sg.group_id
        WHERE sg.student_id = %s
    """
    params = [student["id"]]

    if period == "future":
        query += " AND l.datetime_start > NOW()"
    elif period == "past":
        query += " AND l.datetime_start < NOW()"

    query += " ORDER BY l.datetime_start"

    cur.execute(query, params)
    lessons = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lessons)


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e.description)}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e.description)}), 400


@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": str(e.description)}), 401


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == "__main__":
    print("Server running: http://localhost:5000")
    app.run(debug=True, port=5000)
