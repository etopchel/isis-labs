"""
Занятие 10. Работа с таймерами и отложенными задачами.
Демонстрация threading.Timer, периодических задач.
"""
import threading
import time
from datetime import datetime
 
 
def delayed_action(message):
    """Функция, вызываемая по таймеру."""
    now = datetime.now().strftime("%H:%M:%S")
    print(f"  [{now}] Таймер сработал: {message}")
 
 
def demo_single_timer():
    """Одноразовый таймер."""
    print("\n=== Одноразовый таймер ===")
    print("Таймер установлен на 3 секунды...")
 
    timer = threading.Timer(3.0, delayed_action,
                            args=["Привет через 3 секунды!"])
    timer.start()
    timer.join()  # ожидаем завершения
 
 
class PeriodicTimer:
    """Периодический таймер (аналог setInterval в JavaScript)."""
 
    def __init__(self, interval, func, *args):
        self.interval = interval
        self.func = func
        self.args = args
        self._running = False
        self._timer = None
 
    def _run(self):
        if self._running:
            self.func(*self.args)
            self._timer = threading.Timer(
                self.interval, self._run
            )
            self._timer.start()
 
    def start(self):
        self._running = True
        self._run()
 
    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()
 
 
def demo_periodic_timer():
    """Периодический таймер."""
    print("\n=== Периодический таймер (каждые 2 секунды) ===")
 
    counter = {"count": 0}
 
    def tick():
        counter["count"] += 1
        now = datetime.now().strftime("%H:%M:%S")
        print(f"  [{now}] Тик #{counter['count']}")
 
    pt = PeriodicTimer(2.0, tick)
    pt.start()
    time.sleep(10)  # работает 10 секунд
    pt.stop()
    print(f"Остановлен. Всего тиков: {counter['count']}")
 
 
def demo_reminder():
    """Напоминалка: пользователь задает текст и задержку."""
    print("\n=== Напоминалка ===")
    text = input("Текст напоминания: ") or "Время вышло!"
 
    try:
        delay = int(input("Через сколько секунд напомнить: ") or "5")
    except ValueError:
        delay = 5
 
    print(f"Напоминание через {delay} сек. Продолжаю работу...")
 
    timer = threading.Timer(delay, delayed_action, args=[text])
    timer.start()
 
    # Основная программа продолжает работу
    for i in range(delay + 2):
        time.sleep(1)
        print(f"  Основной поток: шаг {i+1}")
 
 
if __name__ == "__main__":
    demo_single_timer()
    demo_periodic_timer()
    demo_reminder()
