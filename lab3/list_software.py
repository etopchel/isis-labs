"""
Занятие 3. Получение списка установленных программ (Windows).
Использует реестр Windows через модуль winreg.
"""
import sys
import winreg

def get_installed_software_windows():
    """Получает список ПО из реестра Windows."""


    software_list = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    for path in registry_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    try:
                        version = winreg.QueryValueEx(
                            subkey, "DisplayVersion")[0]
                    except FileNotFoundError:
                        version = "N/A"
                    software_list.append((name, version))
                except (FileNotFoundError, OSError):
                    continue
        except FileNotFoundError:
            continue

    return sorted(set(software_list), key=lambda x: x[0].lower())


def classify_software(name):
    """Классифицирует ПО по категориям на основе ключевых слов."""
    name_lower = name.lower()

    system_keywords = [
        "driver", "runtime", "redistribut", "framework",
        "update", "service pack", "directx"
    ]
    tool_keywords = [
        "python", "java", "visual studio", "git", "node",
        "cmake", "compiler", "sdk", "docker"
    ]

    if any(kw in name_lower for kw in system_keywords):
        return "Системное"
    elif any(kw in name_lower for kw in tool_keywords):
        return "Инструментальное"
    else:
        return "Прикладное"


def main():
    if sys.platform != "win32":
        print("Этот скрипт предназначен для Windows.")
        print("В Linux используйте: dpkg --list или rpm -qa")
        return

    software = get_installed_software_windows()
    print(f"Найденопрограмм: {len(software)}")
    print()
    print(f"{'Название':<45} {'Версия':<15} {'Категория'}")
    print("-" * 75)

    stats = {"Системное": 0, "Прикладное": 0, "Инструментальное": 0}
    for name, version in software:
            category = classify_software(name)
            stats[category] += 1
            print(f"{name[:44]:<45} {version[:14]:<15} {category}")

    print()
    print("Статистика:")
    for cat, count in stats.items():
        print(f"  {cat}: {count}")

    return software


if __name__ == "__main__":
    main()
