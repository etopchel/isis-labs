"""
Занятие 5. Генерация Use Case диаграммы в PlantUML.
"""
 
 
class UseCaseDiagram:
    """Генератор Use Case диаграмм."""
 
    def __init__(self, title, system_name):
        self.title = title
        self.system_name = system_name
        self.actors = []
        self.usecases = []
        self.relations = []
 
    def add_actor(self, id_, name, parent=None):
        self.actors.append((id_, name, parent))
 
    def add_usecase(self, id_, name):
        self.usecases.append((id_, name))
 
    def add_association(self, actor_id, uc_id):
        self.relations.append((actor_id, "-->", uc_id, None))
 
    def add_include(self, from_uc, to_uc):
        self.relations.append((from_uc, ".>", to_uc, "<<include>>"))
 
    def add_extend(self, from_uc, to_uc):
        self.relations.append((from_uc, ".>", to_uc, "<<extend>>"))
 
    def generate(self, filename):
        lines = ["@startuml", f"title {self.title}", ""]
 
        # Актеры
        for id_, name, parent in self.actors:
            lines.append(f'actor "{name}" as {id_}')
            if parent:
                lines.append(f'{parent} <|-- {id_}')
 
        lines.append(f'\nrectangle "{self.system_name}" {{')

        # Прецеденты
        for id_, name in self.usecases:
            lines.append(f'  usecase "{name}" as {id_}')
 
        lines.append("}")
        lines.append("")
 
        # Связи
        for src, arrow, dst, label in self.relations:
            if label:
                lines.append(f'{src} {arrow} {dst} : {label}')
            else:
                lines.append(f'{src} {arrow} {dst}')
 
        lines.append("@enduml")
 
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Use Case диаграмма: {filename}")
 
 
# Пример: Система учета студентов
if __name__ == "__main__":
    uc = UseCaseDiagram(
        "Use Case: Система учета студентов",
        "Система учета студентов"
    )
 
    # Актеры
    uc.add_actor("user", "Пользователь")
    uc.add_actor("student", "Студент", parent="user")
    uc.add_actor("teacher", "Преподаватель", parent="user")
    uc.add_actor("admin", "Администратор")
 
    # Прецеденты
    uc.add_usecase("UC1", "Авторизация")
    uc.add_usecase("UC2", "Просмотр расписания")
    uc.add_usecase("UC3", "Просмотр оценок")
    uc.add_usecase("UC4", "Выставление оценок")
    uc.add_usecase("UC5", "Управление пользователями")
    uc.add_usecase("UC6", "Формирование отчетов")
    uc.add_usecase("UC7", "Проверка прав доступа")
    uc.add_usecase("UC8", "Экспорт в Excel")
 
    # Ассоциации
    uc.add_association("student", "UC1")
    uc.add_association("student", "UC2")
    uc.add_association("student", "UC3")
    uc.add_association("teacher", "UC1")
    uc.add_association("teacher", "UC2")
    uc.add_association("teacher", "UC4")
    uc.add_association("admin", "UC5")
    uc.add_association("admin", "UC6")
 
    # Include и Extend
    uc.add_include("UC4", "UC7")
    uc.add_include("UC5", "UC7")
    uc.add_extend("UC6", "UC8")
 
    uc.generate("student_usecase.puml")
