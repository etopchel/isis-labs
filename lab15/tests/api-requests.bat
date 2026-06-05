@echo off
REM Тестирование API танцевальной студии
REM Запускать из cmd.exe, убедитесь что сервер запущен: python server\app.py

echo === 1. Регистрация студента ===
curl -X POST http://localhost:5000/api/auth/signup -H "Content-Type: application/json" -d "{\"login\":\"test_student\",\"password\":\"123\",\"user_type\":\"student\",\"name\":\"Тестов Студент\"}"
echo.

echo === 2. Регистрация преподавателя ===
curl -X POST http://localhost:5000/api/auth/signup -H "Content-Type: application/json" -d "{\"login\":\"test_teacher\",\"password\":\"123\",\"user_type\":\"teacher\",\"name\":\"Тестов Учитель\"}"
echo.

echo === 3. Вход студента ===
curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d "{\"login\":\"andreev_student\",\"password\":\"123\"}"
echo.

echo === 4. Вход преподавателя ===
curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d "{\"login\":\"ivanov_teacher\",\"password\":\"123\"}"
echo.

echo === 5. Список стилей ===
curl http://localhost:5000/api/styles
echo.

echo === 6. Создать стиль ===
curl -X POST http://localhost:5000/api/styles -H "Content-Type: application/json" -d "{\"name\":\"Dancehall\"}"
echo.

echo === 7. Список групп ===
curl http://localhost:5000/api/groups
echo.

echo === 8. Создать группу ===
curl -X POST http://localhost:5000/api/groups -H "Content-Type: application/json" -d "{\"name\":\"Dancehall Kids\",\"age_from\":6,\"age_to\":12,\"style_id\":11}"
echo.

echo === 9. Студенты группы 1 ===
curl http://localhost:5000/api/groups/1/students
echo.

echo === 10. Добавить студента в группу ===
curl -X POST http://localhost:5000/api/groups/1/students -H "Content-Type: application/json" -d "{\"student_id\":1}"
echo.

echo === 11. Список программ ===
curl http://localhost:5000/api/programs
echo.

echo === 12. Создать программу ===
curl -X POST http://localhost:5000/api/programs -H "Content-Type: application/json" -d "{\"name\":\"Dancehall Advanced\",\"style_id\":11,\"track\":\"Продвинутый\",\"duration\":\"60:00\"}"
echo.

echo === 13. Список уроков ===
curl http://localhost:5000/api/lessons
echo.

echo === 14. Уроки по дате ===
curl "http://localhost:5000/api/lessons?date=2026-06-15"
echo.

echo === 15. Создать урок ===
curl -X POST http://localhost:5000/api/lessons -H "Content-Type: application/json" -d "{\"group_id\":1,\"program_id\":1,\"datetime_start\":\"2026-06-22T10:00:00\",\"datetime_end\":\"2026-06-22T10:45:00\"}"
echo.

echo === 16. Группы студента (user_id=11) ===
curl "http://localhost:5000/api/me/groups?user_id=11"
echo.

echo === 17. Будущие уроки студента ===
curl "http://localhost:5000/api/me/lessons?user_id=11&period=future"
echo.

echo === 18. Редактирование профиля студента ===
curl -X PUT http://localhost:5000/api/students/1 -H "Content-Type: application/json" -d "{\"name\":\"Андреев Максим Ильич\",\"phone\":\"+7-911-111-11-11\",\"email\":\"andreev@student.ru\",\"sex\":\"male\",\"age\":10}"
echo.

echo === 19. Удалить студента из группы ===
curl -X DELETE http://localhost:5000/api/groups/1/students/1
echo.

echo === 20. Удалить урок ===
curl -X DELETE http://localhost:5000/api/lessons/21
echo.

echo === Готово! ===
