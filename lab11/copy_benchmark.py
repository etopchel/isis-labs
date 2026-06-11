"""
Занятие 11. Сравнение методов копирования файлов.
"""
import os
import time
import shutil
 
 
def create_test_file(path, size_mb):
    """Создает тестовый файл заданного размера."""
    with open(path, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))
 
 
def copy_manual(src, dst, block_size=65536):
    """Копирование вручную блоками."""
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(block_size)
            if not chunk:
                break
            fout.write(chunk)
 
 
def benchmark_copy(src, label):
    """Сравнивает методы копирования."""
    methods = [
        ("Ручное (64 КБ блоки)", lambda: copy_manual(src, "copy1.tmp")),
        ("shutil.copy()", lambda: shutil.copy(src, "copy2.tmp")),
        ("shutil.copy2()", lambda: shutil.copy2(src, "copy3.tmp")),
    ]
 
    print(f"\n  {label}:")
    for name, func in methods:
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        print(f"    {name:<25} {elapsed:.4f} сек")
 
    # Очистка
    for f in ["copy1.tmp", "copy2.tmp", "copy3.tmp"]:
        if os.path.exists(f):
            os.remove(f)
 
 
if __name__ == "__main__":
    print("=" * 50)
    print("  БЕНЧМАРК КОПИРОВАНИЯ ФАЙЛОВ")
    print("=" * 50)
 
    sizes = [1, 10, 50]  # МБ
    for size in sizes:
        src = f"test_{size}mb.tmp"
        create_test_file(src, size)
        benchmark_copy(src, f"Файл {size} МБ")
        os.remove(src)
 
    print("\nГотово! Тестовые файлы удалены.")
