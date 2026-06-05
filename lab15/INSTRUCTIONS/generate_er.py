"""
Занятие 6. Генерация ER-диаграммы в PlantUML и SQL-скрипта CREATE TABLE.
"""
 
 
class Entity:
    """Описание сущности (таблицы) БД."""
 
    def __init__(self, name, table_name):
        self.name = name
        self.table_name = table_name
        self.attributes = []  # (имя, тип, pk, fk, not_null)
 
    def add_attr(self, name, dtype, pk=False, fk=None, not_null=True):
        self.attributes.append({
            "name": name, "type": dtype,
            "pk": pk, "fk": fk, "not_null": not_null
        })
        return self
 
 
class ERDiagram:
    """Генератор ER-диаграмм и SQL-скриптов."""
 
    def __init__(self, title):
        self.title = title
        self.entities = {}
        self.relations = []
 
    def add_entity(self, entity):
        self.entities[entity.table_name] = entity
 
    def add_relation(self, from_t, to_t, label, cardinality):
        """cardinality: '1--1', '1--*', '*--*'"""
        self.relations.append((from_t, to_t, label, cardinality))
 
    def generate_puml(self, filename):
        """Создает PlantUML ER-диаграмму."""
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
        print(f"ER-диаграмма: {filename}")
 
    def generate_sql(self, filename):
        """Создает SQL-скрипт CREATE TABLE."""
        lines = [f"-- {self.title}", f"-- Автогенерация из ER-диаграммы", ""]
 
        for ent in self.entities.values():
            lines.append(f"CREATE TABLE {ent.table_name} (")
            col_defs = []
            pks = []
            fks = []
            for a in ent.attributes:
                col = f"    {a['name']} {a['type']}"
                if a["not_null"]:
                    col += " NOT NULL"
                col_defs.append(col)
                if a["pk"]:
                    pks.append(a["name"])
                if a["fk"]:
                    ref_table, ref_col = a["fk"]
                    fks.append(
                        f"    FOREIGN KEY ({a['name']}) "
                        f"REFERENCES {ref_table}({ref_col})"
                    )
 
            if pks:
                col_defs.append(
                    f"    PRIMARY KEY ({', '.join(pks)})"
                )
            col_defs.extend(fks)
            lines.append(",\n".join(col_defs))
            lines.append(");")
            lines.append("")
 
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"SQL-скрипт: {filename}")
 
 
# Пример: БД "Система учета студентов"
if __name__ == "__main__":
    er = ERDiagram("ER-диаграмма: Система учета студентов")
 
    # Сущности
    students = Entity("Студенты", "students")
    students.add_attr("id", "SERIAL", pk=True)
    students.add_attr("last_name", "VARCHAR(100)")
    students.add_attr("first_name", "VARCHAR(100)")
    students.add_attr("group_id", "INTEGER", fk=("groups", "id"))
    students.add_attr("email", "VARCHAR(255)", not_null=False)
    er.add_entity(students)
 
    groups = Entity("Группы", "groups")
    groups.add_attr("id", "SERIAL", pk=True)
    groups.add_attr("name", "VARCHAR(20)")
    groups.add_attr("year", "INTEGER")
    er.add_entity(groups)
 
    subjects = Entity("Предметы", "subjects")
    subjects.add_attr("id", "SERIAL", pk=True)
    subjects.add_attr("name", "VARCHAR(200)")
    subjects.add_attr("hours", "INTEGER")
    er.add_entity(subjects)
 
    teachers = Entity("Преподаватели", "teachers")
    teachers.add_attr("id", "SERIAL", pk=True)
    teachers.add_attr("last_name", "VARCHAR(100)")
    teachers.add_attr("first_name", "VARCHAR(100)")
    teachers.add_attr("department", "VARCHAR(200)")
    er.add_entity(teachers)
 
    grades = Entity("Оценки", "grades")
    grades.add_attr("id", "SERIAL", pk=True)
    grades.add_attr("student_id", "INTEGER", fk=("students", "id"))
    grades.add_attr("subject_id", "INTEGER", fk=("subjects", "id"))
    grades.add_attr("teacher_id", "INTEGER", fk=("teachers", "id"))
    grades.add_attr("grade", "INTEGER")
    grades.add_attr("date", "DATE")
    er.add_entity(grades)
 
    # Связи
    er.add_relation("groups", "students", "содержит", "1--*")
    er.add_relation("students", "grades", "получает", "1--*")
    er.add_relation("subjects", "grades", "по предмету", "1--*")
    er.add_relation("teachers", "grades", "выставляет", "1--*")
 
    er.generate_puml("student_er.puml")
    er.generate_sql("create_tables.sql")
