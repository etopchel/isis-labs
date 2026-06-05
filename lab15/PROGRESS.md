# PROGRESS

## [2026-06-05] Part 1 — База данных и документация

- [x] Создана структура папок: db/, docs/, server/, client/, tests/
- [x] db/create_tables.sql — 8 таблиц (users, teachers, students, styles, groups_, student_group, programs, lessons)
- [x] db/seed_data.sql — тестовые данные (20 студентов, 10 преподавателей, 10 стилей, 5 групп, 7 программ, 20 уроков)
- [x] docs/project-vision.txt — цели ИС на русском
- [x] db/generate_usecase.py + db/usecase.puml — Use Case диаграмма (10 прецедентов)
- [x] db/generate_er.py + db/er_diagram.puml — ER диаграмма (8 сущностей)

## [2026-06-05] Part 2 — Flask REST API

- [x] server/app.py — полный REST API:
  - Auth: signup, login
  - Profiles: GET/PUT для студентов и преподавателей
  - Styles: CRUD
  - Groups: CRUD + управление студентами в группах
  - Programs: CRUD
  - Lessons: CRUD с фильтром по дате
  - Student: свои группы и уроки (с фильтром future/past)
- [x] tests/api-requests.ps1 — тестовые запросы
