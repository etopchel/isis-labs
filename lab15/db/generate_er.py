"""
Занятие 6. Генерация ER-диаграммы в PlantUML.
Адаптировано для ИС "Танцевальная студия"
"""


class Entity:
    """Описание сущности (таблицы) БД."""

    def __init__(self, name, table_name):
        self.name = name
        self.table_name = table_name
        self.attributes = []

    def add_attr(self, name, dtype, pk=False, fk=None, not_null=True):
        self.attributes.append({
            "name": name, "type": dtype,
            "pk": pk, "fk": fk, "not_null": not_null
        })
        return self


class ERDiagram:
    """Генератор ER-диаграмм."""

    def __init__(self, title):
        self.title = title
        self.entities = {}
        self.relations = []

    def add_entity(self, entity):
        self.entities[entity.table_name] = entity

    def add_relation(self, from_t, to_t, label, cardinality):
        self.relations.append((from_t, to_t, label, cardinality))

    def generate_puml(self, filename):
        lines = ["@startuml", f"title {self.title}", ""]

        for ent in self.entities.values():
            lines.append(f"entity \"{ent.name}\" as {ent.table_name} {{")
            for a in ent.attributes:
                prefix = "*" if a["pk"] else " "
                fk_mark = " (FK)" if a["fk"] else ""
                lines.append(
                    f"  {prefix} {a['name']} : {a['type']}{fk_mark}"
                )
            lines.append("}")
            lines.append("")

        card_map = {"1--1": "||--||", "1--*": "||--|{", "*--*": "}|--|{"}
        for f, t, label, card in self.relations:
            arrow = card_map.get(card, "||--|{")
            lines.append(f"{f} {arrow} {t} : {label}")

        lines.append("@enduml")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"ER diagram: {filename}")


if __name__ == "__main__":
    er = ERDiagram("ER-диаграмма: Танцевальная студия")

    # Сущности
    users = Entity("Пользователи", "users")
    users.add_attr("id", "SERIAL", pk=True)
    users.add_attr("login", "VARCHAR(50)")
    users.add_attr("password", "VARCHAR(255)")
    users.add_attr("user_type", "VARCHAR(10)")
    er.add_entity(users)

    teachers = Entity("Преподаватели", "teachers")
    teachers.add_attr("id", "SERIAL", pk=True)
    teachers.add_attr("name", "VARCHAR(100)")
    teachers.add_attr("phone", "VARCHAR(20)", not_null=False)
    teachers.add_attr("email", "VARCHAR(255)", not_null=False)
    teachers.add_attr("sex", "VARCHAR(10)", not_null=False)
    teachers.add_attr("age", "INTEGER", not_null=False)
    teachers.add_attr("user_id", "INTEGER", fk=("users", "id"))
    er.add_entity(teachers)

    students = Entity("Студенты", "students")
    students.add_attr("id", "SERIAL", pk=True)
    students.add_attr("name", "VARCHAR(100)")
    students.add_attr("phone", "VARCHAR(20)", not_null=False)
    students.add_attr("email", "VARCHAR(255)", not_null=False)
    students.add_attr("sex", "VARCHAR(10)", not_null=False)
    students.add_attr("age", "INTEGER", not_null=False)
    students.add_attr("user_id", "INTEGER", fk=("users", "id"))
    er.add_entity(students)

    styles = Entity("Стили танца", "styles")
    styles.add_attr("id", "SERIAL", pk=True)
    styles.add_attr("name", "VARCHAR(100)")
    er.add_entity(styles)

    groups = Entity("Группы", "groups_")
    groups.add_attr("id", "SERIAL", pk=True)
    groups.add_attr("name", "VARCHAR(100)")
    groups.add_attr("age_from", "INTEGER", not_null=False)
    groups.add_attr("age_to", "INTEGER", not_null=False)
    groups.add_attr("style_id", "INTEGER", fk=("styles", "id"))
    er.add_entity(groups)

    student_group = Entity("Студент-Группа", "student_group")
    student_group.add_attr("student_id", "INTEGER", pk=True, fk=("students", "id"))
    student_group.add_attr("group_id", "INTEGER", pk=True, fk=("groups_", "id"))
    er.add_entity(student_group)

    programs = Entity("Программы", "programs")
    programs.add_attr("id", "SERIAL", pk=True)
    programs.add_attr("name", "VARCHAR(200)")
    programs.add_attr("style_id", "INTEGER", fk=("styles", "id"))
    programs.add_attr("track", "VARCHAR(100)", not_null=False)
    programs.add_attr("duration", "VARCHAR(5)", not_null=False)
    er.add_entity(programs)

    lessons = Entity("Уроки", "lessons")
    lessons.add_attr("id", "SERIAL", pk=True)
    lessons.add_attr("group_id", "INTEGER", fk=("groups_", "id"))
    lessons.add_attr("program_id", "INTEGER", fk=("programs", "id"))
    lessons.add_attr("datetime_start", "TIMESTAMP")
    lessons.add_attr("datetime_end", "TIMESTAMP")
    er.add_entity(lessons)

    # Связи
    er.add_relation("users", "teachers", "является", "1--1")
    er.add_relation("users", "students", "является", "1--1")
    er.add_relation("styles", "groups_", "содержит", "1--*")
    er.add_relation("styles", "programs", "имеет", "1--*")
    er.add_relation("groups_", "student_group", "включает", "1--*")
    er.add_relation("students", "student_group", "состоит", "1--*")
    er.add_relation("groups_", "lessons", "проводит", "1--*")
    er.add_relation("programs", "lessons", "изучается", "1--*")

    er.generate_puml("db/er_diagram.puml")
