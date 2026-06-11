"""
Занятие 10. Обработка сигналов (аналог прерываний).
Ctrl+C не завершает программу, а вызывает обработчик.
"""
import signal
import time
import sys
from datetime import datetime
 
 
class InterruptibleWorker:
    """Рабочий процесс с обработкой прерываний."""
    def __init__(self):
        self.iterations = 0
        self.start_time = None
        self.running = True
        self.interrupt_count = 0
 
    def handle_interrupt(self, signum, frame):
        """Обработчик сигнала SIGINT (Ctrl+C)."""
        self.interrupt_count += 1
        elapsed = time.time() - self.start_time
 
        print(f"\n\n{'='*40}")
        print(f"  ПРЕРЫВАНИЕ #{self.interrupt_count}")
        print(f"  Время работы: {elapsed:.1f} сек")
        print(f"  Итераций выполнено: {self.iterations}")
        print(f"  Скорость: {self.iterations/elapsed:.0f} ит/сек")
        print(f"{'='*40}")
 
        if self.interrupt_count >= 3:
            print("  Три прерывания --- завершаю работу.")
            self.running = False
        else:
            remaining = 3 - self.interrupt_count
            print(f"  Нажмите Ctrl+C еще {remaining} раз для выхода.")
            print("  Продолжаю работу...\n")
 
    def run(self):
        """Основной рабочий цикл."""
        # Регистрация обработчика сигнала
        signal.signal(signal.SIGINT, self.handle_interrupt)
 
        print("Рабочий процесс запущен.")
        print("Нажмите Ctrl+C для вызова обработчика прерывания.")
        print("3 прерывания --- завершение программы.\n")
 
        self.start_time = time.time()
 
        while self.running:
            # Имитация полезной работы
            self.iterations += 1
            result = sum(i * i for i in range(1000))
 
            if self.iterations % 500 == 0:
                elapsed = time.time() - self.start_time
                print(f"  Итерация {self.iterations:>6} | "
                      f"Время: {elapsed:.1f} сек")
 
            time.sleep(0.01)  # небольшая пауза
 
        print(f"\nПрограмма завершена после {self.iterations} итераций.")
 
 
if __name__ == "__main__":
    worker = InterruptibleWorker()
    worker.run()
