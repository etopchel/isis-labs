"""
Занятие 8. Сбор информации об аппаратном обеспечении ПК.
Использует модули platform, psutil, os.
Установите psutil: pip install psutil
"""
import platform
import os
 
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("Установите psutil: pip install psutil")
 
 
def get_system_info():
    """Общая информация о системе."""
    print("=" * 55)
    print("  ПАСПОРТ РАБОЧЕЙ СТАНЦИИ")
    print("=" * 55)
 
    info = {
        "ОС": f"{platform.system()} {platform.release()}",
        "Версия ОС": platform.version(),
        "Архитектура": platform.machine(),
        "Имя компьютера": platform.node(),
        "Процессор": platform.processor(),
    }
 
    print("\n--- Общая информация ---")
    for key, value in info.items():
        print(f"  {key}: {value}")
 
 
def get_cpu_info():
    """Информация о процессоре."""
    if not HAS_PSUTIL:
        return
 
    print("\n--- Процессор ---")
    print(f"  Физические ядра: {psutil.cpu_count(logical=False)}")
    print(f"  Логические ядра: {psutil.cpu_count(logical=True)}")
 
    freq = psutil.cpu_freq()
    if freq:
        print(f"  Частота: {freq.current:.0f} МГц")
        print(f"  Макс. частота: {freq.max:.0f} МГц")
 
    print(f"  Загрузка CPU: {psutil.cpu_percent(interval=1)}%")

def get_memory_info():
    """Информация об оперативной памяти."""
    if not HAS_PSUTIL:
        return
 
    print("\n--- Оперативная память ---")
    mem = psutil.virtual_memory()
    print(f"  Всего: {mem.total / (1024**3):.2f} ГБ")
    print(f"  Используется: {mem.used / (1024**3):.2f} ГБ")
    print(f"  Свободно: {mem.available / (1024**3):.2f} ГБ")
    print(f"  Загрузка: {mem.percent}%")
 
 
def get_disk_info():
    """Информация о дисках."""
    if not HAS_PSUTIL:
        return
 
    print("\n--- Дисковые накопители ---")
    for partition in psutil.disk_partitions():
        print(f"  Диск: {partition.device}")
        print(f"    Файловая система: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"    Всего: {usage.total / (1024**3):.2f} ГБ")
            print(f"    Занято: {usage.used / (1024**3):.2f} ГБ")
            print(f"    Свободно: {usage.free / (1024**3):.2f} ГБ")
        except PermissionError:
            print("    (нет доступа)")
 
 
def get_network_info():
    """Информация о сетевых интерфейсах."""
    if not HAS_PSUTIL:
        return
 
    print("\n--- Сетевые интерфейсы ---")
    addrs = psutil.net_if_addrs()
    for iface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family.name == "AF_INET":
                print(f"  {iface}: {addr.address}")
 
 
def save_report(filename="workstation_passport.md"):
    """Сохраняет отчет в Markdown-файл."""
    import io
    import sys
 
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
 
    get_system_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
 
    sys.stdout = old_stdout
    report = buffer.getvalue()
 
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Паспорт рабочей станции\n\n```\n{report}\n```")
    print(report)
    print(f"\nОтчет сохранен: {filename}")
 
 
if __name__ == "__main__":
    save_report()
