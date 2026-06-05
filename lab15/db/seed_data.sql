-- Заполнение тестовыми данными
\c dance_studio;

-- ========== СТИЛИ ==========
INSERT INTO styles (name) VALUES
('Hip-Hop'),
('Contemporary'),
('Бальные танцы'),
('Salsa'),
('Балет'),
('Jazz'),
('Breakdance'),
('Tango'),
('Latin'),
('Street Dance');

-- ========== ГРУППЫ ==========
INSERT INTO groups_ (name, age_from, age_to, style_id) VALUES
('Начинающие Hip-Hop', 6, 10, 1),
('Продвинутый Contemporary', 12, 18, 2),
('Ballroom Adults', 18, NULL, 3),
('Salsa Kids', 8, 14, 4),
('Ballet Teens', 10, 16, 5);

-- ========== ПРОГРАММЫ ==========
INSERT INTO programs (name, style_id, track, duration) VALUES
('Основы Hip-Hop', 1, 'Базовый', '45:00'),
('Contemporary Improvisation', 2, 'Продвинутый', '60:00'),
('Ballroom Standard', 3, 'Стандарт', '55:00'),
('Salsa Basics', 4, 'Базовый', '50:00'),
('Ballet Technique', 5, 'Классика', '90:00'),
('Street Dance Choreography', 10, 'Хореография', '60:00'),
('Latin Solo', 9, 'Соло', '45:00');

-- ========== ПОЛЬЗОВАТЕЛИ (преподаватели) ==========
INSERT INTO users (login, password, user_type) VALUES
('ivanov_teacher', '123', 'teacher'),
('petrova_teacher', '123', 'teacher'),
('sidorov_teacher', '123', 'teacher'),
('smirnova_teacher', '123', 'teacher'),
('volkov_teacher', '123', 'teacher'),
('fedotova_teacher', '123', 'teacher'),
('morozov_teacher', '123', 'teacher'),
('kuznetsova_teacher', '123', 'teacher'),
('popov_teacher', '123', 'teacher'),
('lebedeva_teacher', '123', 'teacher');

INSERT INTO teachers (name, phone, email, sex, age, user_id) VALUES
('Иванов Алексей Петрович', '+7-901-111-11-11', 'ivanov@dance.ru', 'male', 35, 1),
('Петрова Екатерина Сергеевна', '+7-902-222-22-22', 'petrova@dance.ru', 'female', 28, 2),
('Сидоров Дмитрий Олегович', '+7-903-333-33-33', 'sidorov@dance.ru', 'male', 42, 3),
('Смирнова Анна Викторовна', '+7-904-444-44-44', 'smirnova@dance.ru', 'female', 31, 4),
('Волков Максим Андреевич', '+7-905-555-55-55', 'volkov@dance.ru', 'male', 25, 5),
('Федотова Ольга Игоревна', '+7-906-666-66-66', 'fedotova@dance.ru', 'female', 29, 6),
('Морозов Кирилл Денисович', '+7-907-777-77-77', 'morozov@dance.ru', 'male', 38, 7),
('Кузнецова Татьяна Романовна', '+7-908-888-88-88', 'kuznetsova@dance.ru', 'female', 33, 8),
('Попов Артем Владиславович', '+7-909-999-99-99', 'popov@dance.ru', 'male', 27, 9),
('Лебедева Мария Алексеевна', '+7-910-000-00-00', 'lebedeva@dance.ru', 'female', 24, 10);

-- ========== ПОЛЬЗОВАТЕЛИ (студенты) ==========
INSERT INTO users (login, password, user_type) VALUES
('andreev_student', '123', 'student'),
('belyaeva_student', '123', 'student'),
('vasiliev_student', '123', 'student'),
('grigoryeva_student', '123', 'student'),
('dmitriev_student', '123', 'student'),
('eliseeva_student', '123', 'student'),
('zhukov_student', '123', 'student'),
('zaytseva_student', '123', 'student'),
('ivanov_student', '123', 'student'),
('kuzmin_student', '123', 'student'),
('lukina_student', '123', 'student'),
('mikhailov_student', '123', 'student'),
('nikolaeva_student', '123', 'student'),
('orlov_student', '123', 'student'),
('pavlova_student', '123', 'student'),
('romanov_student', '123', 'student'),
('sokolova_student', '123', 'student'),
('trofimov_student', '123', 'student'),
('ustinova_student', '123', 'student'),
('filippov_student', '123', 'student');

INSERT INTO students (name, phone, email, sex, age, user_id) VALUES
('Андреев Максим Ильич', '+7-911-111-11-11', 'andreev@student.ru', 'male', 9, 11),
('Беляева Алиса Дмитриевна', '+7-912-222-22-22', 'belyaeva@student.ru', 'female', 14, 12),
('Васильев Иван Сергеевич', '+7-913-333-33-33', 'vasiliev@student.ru', 'male', 8, 13),
('Григорьева Полина Андреевна', '+7-914-444-44-44', 'grigoryeva@student.ru', 'female', 16, 14),
('Дмитриев Артём Павлович', '+7-915-555-55-55', 'dmitriev@student.ru', 'male', 12, 15),
('Елисеева София Алексеевна', '+7-916-666-66-66', 'eliseeva@student.ru', 'female', 11, 16),
('Жуков Тимофей Евгеньевич', '+7-917-777-77-77', 'zhukov@student.ru', 'male', 7, 17),
('Зайцева Варвара Олеговна', '+7-918-888-88-88', 'zaytseva@student.ru', 'female', 15, 18),
('Иванов Матвей Романович', '+7-919-999-99-99', 'ivanovstud@student.ru', 'male', 10, 19),
('Кузьмин Денис Артурович', '+7-920-000-00-00', 'kuzmin@student.ru', 'male', 13, 20),
('Лукина Ангелина Кирилловна', '+7-921-111-11-11', 'lukina@student.ru', 'female', 17, 21),
('Михайлов Георгий Владимирович', '+7-922-222-22-22', 'mikhailov@student.ru', 'male', 9, 22),
('Николаева Ева Тимуровна', '+7-923-333-33-33', 'nikolaeva@student.ru', 'female', 12, 23),
('Орлов Степан Игоревич', '+7-924-444-44-44', 'orlov@student.ru', 'male', 20, 24),
('Павлова Александра Денисовна', '+7-925-555-55-55', 'pavlova@student.ru', 'female', 22, 25),
('Романов Константин Петрович', '+7-926-666-66-66', 'romanov@student.ru', 'male', 19, 26),
('Соколова Арина Даниловна', '+7-927-777-77-77', 'sokolova@student.ru', 'female', 14, 27),
('Трофимов Ярослав Сергеевич', '+7-928-888-88-88', 'trofimov@student.ru', 'male', 11, 28),
('Устинова Милана Максимовна', '+7-929-999-99-99', 'ustinova@student.ru', 'female', 16, 29),
('Филиппов Лев Арсентьевич', '+7-930-000-00-00', 'filippov@student.ru', 'male', 21, 30);

-- ========== СВЯЗИ СТУДЕНТОВ И ГРУПП ==========
INSERT INTO student_group (student_id, group_id) VALUES
-- Группа 1: Начинающие Hip-Hop (6-10 лет) — student_ids: 1,3,7,9,12
(1, 1), (3, 1), (7, 1), (9, 1), (12, 1),
-- Группа 2: Продвинутый Contemporary (12-18) — student_ids: 2,4,5,8,11,13,17,19
(2, 2), (4, 2), (5, 2), (8, 2), (11, 2), (13, 2), (17, 2), (19, 2),
-- Группа 3: Ballroom Adults (18+) — student_ids: 14,15,16,18,20
(14, 3), (15, 3), (16, 3), (18, 3), (20, 3),
-- Группа 4: Salsa Kids (8-14) — student_ids: 5,6,9,10,13
(5, 4), (6, 4), (9, 4), (10, 4), (13, 4),
-- Группа 5: Ballet Teens (10-16) — student_ids: 2,4,6,8,11,17,19
(2, 5), (4, 5), (6, 5), (8, 5), (11, 5), (17, 5), (19, 5);

-- ========== УРОКИ ==========
INSERT INTO lessons (group_id, program_id, datetime_start, datetime_end) VALUES
-- Прошедшие уроки
(1, 1, '2026-05-10 10:00:00', '2026-05-10 10:45:00'),
(2, 2, '2026-05-10 11:00:00', '2026-05-10 12:00:00'),
(3, 3, '2026-05-11 15:00:00', '2026-05-11 15:55:00'),
(4, 4, '2026-05-11 16:00:00', '2026-05-11 16:50:00'),
(5, 5, '2026-05-12 09:00:00', '2026-05-12 10:30:00'),
(1, 6, '2026-05-12 10:00:00', '2026-05-12 11:00:00'),
(2, 7, '2026-05-13 11:00:00', '2026-05-13 11:45:00'),
(3, 3, '2026-05-13 15:00:00', '2026-05-13 15:55:00'),
(4, 4, '2026-05-14 16:00:00', '2026-05-14 16:50:00'),
(5, 5, '2026-05-14 09:00:00', '2026-05-14 10:30:00'),
-- Будущие уроки
(1, 1, '2026-06-15 10:00:00', '2026-06-15 10:45:00'),
(2, 2, '2026-06-15 11:00:00', '2026-06-15 12:00:00'),
(3, 3, '2026-06-16 15:00:00', '2026-06-16 15:55:00'),
(4, 4, '2026-06-16 16:00:00', '2026-06-16 16:50:00'),
(5, 5, '2026-06-17 09:00:00', '2026-06-17 10:30:00'),
(1, 6, '2026-06-17 10:00:00', '2026-06-17 11:00:00'),
(2, 7, '2026-06-18 11:00:00', '2026-06-18 11:45:00'),
(3, 3, '2026-06-18 15:00:00', '2026-06-18 15:55:00'),
(4, 4, '2026-06-19 16:00:00', '2026-06-19 16:50:00'),
(5, 5, '2026-06-19 09:00:00', '2026-06-19 10:30:00');
