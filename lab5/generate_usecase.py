"""
Занятие 5. Генерация Use Case диаграммы в PlantUML.
Адаптировано для ИС "Танцевальная студия"
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

        for id_, name, parent in self.actors:
            lines.append(f'actor "{name}" as {id_}')
            if parent:
                lines.append(f'{parent} <|-- {id_}')

        lines.append(f'\nrectangle "{self.system_name}" {{')

        for id_, name in self.usecases:
            lines.append(f'  usecase "{name}" as {id_}')

        lines.append("}")
        lines.append("")

        for src, arrow, dst, label in self.relations:
            if label:
                lines.append(f'{src} {arrow} {dst} : {label}')
            else:
                lines.append(f'{src} {arrow} {dst}')

        lines.append("@enduml")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Use Case diagram: {filename}")


if __name__ == "__main__":
    uc = UseCaseDiagram(
        "Use Case: Танцевальная студия",
        "Танцевальная студия"
    )

    # Актеры
    uc.add_actor("user", "Пользователь")
    uc.add_actor("student", "Студент", parent="user")
    uc.add_actor("teacher", "Преподаватель", parent="user")

    # Прецеденты
    uc.add_usecase("UC1", "Регистрация")
    uc.add_usecase("UC2", "Вход и редактирование профиля (учитель)")
    uc.add_usecase("UC3", "Вход и редактирование профиля (студент)")
    uc.add_usecase("UC4", "Управление стилями танца")
    uc.add_usecase("UC5", "Управление группами")
    uc.add_usecase("UC6", "Добавление/удаление студентов из групп")
    uc.add_usecase("UC7", "Просмотр своих групп (студент)")
    uc.add_usecase("UC8", "Управление программами")
    uc.add_usecase("UC9", "Управление уроками")
    uc.add_usecase("UC10", "Просмотр расписания уроков (студент)")

    # Ассоциации
    uc.add_association("student", "UC1")
    uc.add_association("student", "UC3")
    uc.add_association("student", "UC7")
    uc.add_association("student", "UC10")
    uc.add_association("teacher", "UC1")
    uc.add_association("teacher", "UC2")
    uc.add_association("teacher", "UC4")
    uc.add_association("teacher", "UC5")
    uc.add_association("teacher", "UC6")
    uc.add_association("teacher", "UC8")
    uc.add_association("teacher", "UC9")

    # Include — авторизация нужна для всех действий
    uc.add_include("UC2", "UC1")
    uc.add_include("UC3", "UC1")
    uc.add_include("UC4", "UC1")
    uc.add_include("UC5", "UC1")
    uc.add_include("UC6", "UC1")
    uc.add_include("UC7", "UC1")
    uc.add_include("UC8", "UC1")
    uc.add_include("UC9", "UC1")
    uc.add_include("UC10", "UC1")

    uc.generate("usecase.puml")
