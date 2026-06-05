# Тестирование API танцевальной студии
# Запускать из корня проекта
# Перед запуском убедитесь что сервер запущен: python server/app.py

Write-Host "=== 1. Регистрация нового студента ===" -ForegroundColor Green
$body = @{login="test_student"; password="123"; user_type="student"; name="Тестов Студент"} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/auth/signup" -ContentType "application/json" -Body $body
$resp | ConvertTo-Json

Write-Host "`n=== 2. Регистрация нового преподавателя ===" -ForegroundColor Green
$body = @{login="test_teacher"; password="123"; user_type="teacher"; name="Тестов Учитель"} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/auth/signup" -ContentType "application/json" -Body $body
$resp | ConvertTo-Json

Write-Host "`n=== 3. Вход студента ===" -ForegroundColor Green
$body = @{login="andreev_student"; password="123"} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/auth/login" -ContentType "application/json" -Body $body
$resp | ConvertTo-Json

Write-Host "`n=== 4. Вход преподавателя ===" -ForegroundColor Green
$body = @{login="ivanov_teacher"; password="123"} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/auth/login" -ContentType "application/json" -Body $body
$resp | ConvertTo-Json

Write-Host "`n=== 5. Список стилей ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/styles"
$resp | ConvertTo-Json

Write-Host "`n=== 6. Создать стиль ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/styles" -ContentType "application/json" -Body '{"name":"Dancehall"}'
$resp | ConvertTo-Json

Write-Host "`n=== 7. Список групп ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/groups"
$resp | ConvertTo-Json

Write-Host "`n=== 8. Создать группу ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/groups" -ContentType "application/json" -Body '{"name":"Dancehall Kids","age_from":6,"age_to":12,"style_id":11}'
$resp | ConvertTo-Json

Write-Host "`n=== 9. Студенты группы 1 ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/groups/1/students"
$resp | ConvertTo-Json

Write-Host "`n=== 10. Добавить студента в группу ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/groups/1/students" -ContentType "application/json" -Body '{"student_id":1}'
$resp | ConvertTo-Json

Write-Host "`n=== 11. Список программ ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/programs"
$resp | ConvertTo-Json

Write-Host "`n=== 12. Создать программу ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/programs" -ContentType "application/json" -Body '{"name":"Dancehall Advanced","style_id":11,"track":"Продвинутый","duration":"60:00"}'
$resp | ConvertTo-Json

Write-Host "`n=== 13. Список уроков ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/lessons"
$resp | ConvertTo-Json

Write-Host "`n=== 14. Уроки по дате ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/lessons?date=2026-06-15"
$resp | ConvertTo-Json

Write-Host "`n=== 15. Создать урок ===" -ForegroundColor Green
$body = @{group_id=1; program_id=1; datetime_start="2026-06-22T10:00:00"; datetime_end="2026-06-22T10:45:00"} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/lessons" -ContentType "application/json" -Body $body
$resp | ConvertTo-Json

Write-Host "`n=== 16. Группы студента (user_id=11) ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/me/groups?user_id=11"
$resp | ConvertTo-Json

Write-Host "`n=== 17. Будущие уроки студента ===" -ForegroundColor Green
$resp = Invoke-RestMethod -Method Get -Uri "http://localhost:5000/api/me/lessons?user_id=11&period=future"
$resp | ConvertTo-Json

Write-Host "`n=== 18. Редактирование профиля студента ===" -ForegroundColor Green
$body = @{name="Андреев Максим Ильич"; phone="+7-911-111-11-11"; email="andreev@student.ru"; sex="male"; age=10} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Put -Uri "http://localhost:5000/api/students/1" -ContentType "application/json" -Body $body
$resp | ConvertTo-Json

Write-Host "`n=== 19. Удалить студента из группы ===" -ForegroundColor Green
try { $resp = Invoke-RestMethod -Method Delete -Uri "http://localhost:5000/api/groups/1/students/1"; $resp | ConvertTo-Json } catch { Write-Host "Уже удалён или не найден" -ForegroundColor Yellow }

Write-Host "`n=== 20. Удалить урок ===" -ForegroundColor Green
try { $resp = Invoke-RestMethod -Method Delete -Uri "http://localhost:5000/api/lessons/21"; $resp | ConvertTo-Json } catch { Write-Host "Уже удалён или не найден" -ForegroundColor Yellow }

Write-Host "`n=== Готово! ===" -ForegroundColor Green
