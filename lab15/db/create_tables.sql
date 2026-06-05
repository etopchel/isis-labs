-- Создание базы данных
CREATE DATABASE dance_studio;

\c dance_studio;

-- Таблица пользователей для авторизации
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_type VARCHAR(10) NOT NULL CHECK (user_type IN ('student', 'teacher'))
);

-- Таблица преподавателей
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    sex VARCHAR(10) CHECK (sex IN ('male', 'female')),
    age INTEGER CHECK (age > 0 AND age < 120),
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE
);

-- Таблица студентов
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    sex VARCHAR(10) CHECK (sex IN ('male', 'female')),
    age INTEGER CHECK (age > 0 AND age < 120),
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE
);

-- Таблица стилей танца
CREATE TABLE styles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица групп
CREATE TABLE groups_ (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age_from INTEGER CHECK (age_from IS NULL OR (age_from >= 0 AND age_from < 120)),
    age_to INTEGER CHECK (age_to IS NULL OR (age_to >= 0 AND age_to < 120)),
    style_id INTEGER NOT NULL REFERENCES styles(id) ON DELETE CASCADE
);

-- Связь студент-группа (многие ко многим)
CREATE TABLE student_group (
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL REFERENCES groups_(id) ON DELETE CASCADE,
    PRIMARY KEY (student_id, group_id)
);

-- Таблица программ
CREATE TABLE programs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    style_id INTEGER NOT NULL REFERENCES styles(id) ON DELETE CASCADE,
    track VARCHAR(100),
    duration VARCHAR(5)  -- формат mm:ss
);

-- Таблица уроков
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups_(id) ON DELETE CASCADE,
    program_id INTEGER NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
    datetime_start TIMESTAMP NOT NULL,
    datetime_end TIMESTAMP NOT NULL,
    CHECK (datetime_end > datetime_start)
);
