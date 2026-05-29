def generate_component_diagram(title, packages, connections, filename):
    """
    Генерирует PlantUML-диаграмму компонентов.
 
    Args:
        title: название диаграммы
        packages: dict {имя_пакета: [список_компонентов]}
        connections: list [(источник, цель, подпись)]
        filename: имя выходного .puml файла
    """
    lines = ["@startuml", f'title {title}', ""]
 
    for pkg_name, components in packages.items():
        lines.append(f'package "{pkg_name}" {{')
        for comp in components:
            lines.append(f'  [{comp}]')
        lines.append("}")
        lines.append("")
 
    for src, dst, label in connections:
        lines.append(f'[{src}] --> [{dst}] : {label}')
 
    lines.append("@enduml")
 
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
 
    print(f"Диаграмма сохранена: {filename}")
 
 
# Пример использования
if __name__ == "__main__":
    packages = {
        "Клиентская часть": ["Веб-интерфейс", "Мобильное приложение"],
        "Серверная часть": ["API-сервер", "Бизнес-логика", "Авторизация"],
        "Хранилище данных": ["PostgreSQL", "Redis (кэш)"],
    }
 
    connections = [
        ("Веб-интерфейс", "API-сервер", "HTTP/REST"),
        ("Мобильное приложение", "API-сервер", "HTTP/REST"),
        ("API-сервер", "Авторизация", "JWT"),
        ("API-сервер", "Бизнес-логика", "вызов"),
        ("Бизнес-логика", "PostgreSQL", "SQL"),
        ("Бизнес-логика", "Redis (кэш)", "GET/SET"),
    ]
 
    generate_component_diagram(
        title='Архитектура ИС "Интернет-магазин"',
        packages=packages,
        connections=connections,
        filename="shop_architecture.puml"
    )
