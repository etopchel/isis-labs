"""
Занятие 9. Мониторинг процессов и ресурсов ОС.
Установите psutil: pip install psutil
"""
import psutil
import time
import os
 
 
def show_top_processes(n=10):
    """Показывает топ-N процессов по использованию CPU."""
    print(f"\n{'PID':<8} {'Имя':<25} {'CPU%':<8} {'Память (МБ)':<12} {'Статус'}")
    print("-" * 65)
 
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent',
                                      'memory_info', 'status']):
        try:
            info = proc.info
            mem_mb = info['memory_info'].rss / (1024 * 1024)
            processes.append({
                'pid': info['pid'],
                'name': info['name'][:24],
                'cpu': info['cpu_percent'],
                'mem': mem_mb,
                'status': info['status'],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
 
    # Сортировка по CPU
    processes.sort(key=lambda x: x['cpu'], reverse=True)
 
    for p in processes[:n]:
        print(f"{p['pid']:<8} {p['name']:<25} {p['cpu']:<8.1f} "
              f"{p['mem']:<12.1f} {p['status']}")
def monitor_resources(duration=30, interval=3):
    """Мониторинг ресурсов в реальном времени."""
    print(f"\nМониторинг ресурсов ({duration} сек, интервал {interval} сек)")
    print(f"{'Время':<10} {'CPU%':<8} {'RAM%':<8} {'Диск (чт/зап МБ/с)'}")
    print("-" * 50)
 
    disk_prev = psutil.disk_io_counters()
    start = time.time()
 
    while time.time() - start < duration:
        cpu = psutil.cpu_percent(interval=interval)
        ram = psutil.virtual_memory().percent
 
        disk_curr = psutil.disk_io_counters()
        read_speed = (disk_curr.read_bytes - disk_prev.read_bytes)
        read_speed = read_speed / (1024 * 1024 * interval)
        write_speed = (disk_curr.write_bytes - disk_prev.write_bytes)
        write_speed = write_speed / (1024 * 1024 * interval)
        disk_prev = disk_curr
 
        elapsed = int(time.time() - start)
        print(f"{elapsed:>4} сек   {cpu:<8.1f} {ram:<8.1f} "
              f"{read_speed:.1f} / {write_speed:.1f}")
 
 
if __name__ == "__main__":
    print("=" * 50)
    print("  МОНИТОР ПРОЦЕССОВ И РЕСУРСОВ")
    print("=" * 50)
 
    print(f"\nВсего процессов: {len(list(psutil.process_iter()))}")
    print(f"Загрузка CPU: {psutil.cpu_percent()}%")
    print(f"Загрузка RAM: {psutil.virtual_memory().percent}%")
 
    show_top_processes()
    monitor_resources(duration=15, interval=3)
