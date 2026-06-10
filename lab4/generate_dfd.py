"""
Занятие 4. Генерация DFD-диаграммы в формате PlantUML.
Скрипт принимает описание системы и создает .puml файл.
"""


class DFDDiagram:
    """Генератор DFD-диаграмм в формате PlantUML."""

    def __init__(self, title):
        self.title = title
        self.entities = []      # внешниесущности
        self.processes = []     # процессы
        self.datastores = []    # хранилища данных
        self.flows = []         # потоки данных

    def add_entity(self, id_, name):
        """Добавляет внешнюю сущность."""
        self.entities.append((id_, name))

    def add_process(self, id_, name):
        """Добавляетпроцесс."""
        self.processes.append((id_, name))

    def add_datastore(self, id_, name):
        """Добавляетхранилищеданных."""
        self.datastores.append((id_, name))

    def add_flow(self, from_id, to_id, label):
        """Добавляетпотокданных."""
        self.flows.append((from_id, to_id, label))

    def generate(self, filename):
        """ГенерируетPlantUML-файл."""
        lines = [
            "@startuml",
            f"title {self.title}",
            "skinparam rectangle {",
            "  BackgroundColor<<entity>>LightBlue",
            "  BackgroundColor<<process>>LightGreen",
            "  BackgroundColor<<datastore>>LightYellow",
            "}",
            "",
        ]

        for id_, name in self.entities:
            lines.append(f'rectangle "{name}" <<entity>> as {id_}')

        lines.append("")
        for id_, name in self.processes:
            lines.append(f'rectangle "({id_})\\n{name}" <<process>> as {id_}')
            
        lines.append("")
        for id_, name in self.datastores:
            lines.append(f'database "{name}" <<datastore>> as {id_}')

        lines.append("")
        for src, dst, label in self.flows:
            lines.append(f'{src} --> {dst} : {label}')

        lines.append("@enduml")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"DFD-диаграмма сохранена: {filename}")


# Пример: DFD для интернет-магазина
if __name__ == "__main__":
    dfd = DFDDiagram("DFD: Обработка заказа в интернет-магазине")

        # Внешние сущности
    dfd.add_entity("client", "Клиент")
    dfd.add_entity("courier", "Курьерскаяслужба")
    dfd.add_entity("payment", "Платежнаясистема")

    # Процессы
    dfd.add_process("P1", "Обработка заказа")
    dfd.add_process("P2", "Управление складом")
    dfd.add_process("P3", "Обработка платежа")

        # Хранилища
    dfd.add_datastore("D1", "D1: База заказов")
    dfd.add_datastore("D2", "D2: Каталог товаров")

        # Потоки данных
    dfd.add_flow("client", "P1", "заявка")
    dfd.add_flow("P1", "client", "подтверждение")
    dfd.add_flow("P1", "D1", "сохранение заказа")
    dfd.add_flow("P1", "P2", "проверка наличия")
    dfd.add_flow("P2", "D2", "запрос остатков")
    dfd.add_flow("P1", "P3", "данные оплаты")
    dfd.add_flow("P3", "payment", "запросплатежа")
    dfd.add_flow("P1", "courier", "заявка на доставку")
    dfd.generate("shop_dfd.puml")