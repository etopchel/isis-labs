"""
Занятие 11. Бенчмарк файлового ввода-вывода.
Сравнение различных методов чтения и записи файлов.
"""
import time
import os
import tempfile
 
 
def benchmark(func, label):
    """Измеряет время выполнения функции."""
    start = time.perf_counter()
    result = func()
    elapsed = time.perf_counter() - start
    print(f"  {label:<40} {elapsed:.4f} сек")
    return result
 
 
def test_write_methods():
    """Сравнение методов записи."""
    print("\n=== ТЕСТ ЗАПИСИ (100 000 строк) ===")
    lines_count = 100_000
    line = "Тестовая строка для записи в файл номер "
 
    # Метод 1: построчная запись
    def write_line_by_line():
        with open("test_write1.txt", "w", encoding="utf-8") as f:
            for i in range(lines_count):
                f.write(f"{line}{i}\n")
 
    # Метод 2: запись списком (writelines)
    def write_all_lines():
        data = [f"{line}{i}\n" for i in range(lines_count)]
        with open("test_write2.txt", "w", encoding="utf-8") as f:
            f.writelines(data)
 
    # Метод 3: формирование строки и одна запись
    def write_single_block():
        data = "\n".join(f"{line}{i}" for i in range(lines_count))
        with open("test_write3.txt", "w", encoding="utf-8") as f:
            f.write(data)
 
    benchmark(write_line_by_line, "Построчная запись")
    benchmark(write_all_lines, "writelines (список)")
    benchmark(write_single_block, "Единый блок")
 
 
def test_read_methods():
    """Сравнение методов чтения."""
    print("\n=== ТЕСТ ЧТЕНИЯ ===")
 
    filename = "test_write1.txt"
    file_size = os.path.getsize(filename)
    print(f"  Размер файла: {file_size / 1024:.1f} КБ")
 
    # Метод 1: построчное чтение
    def read_line_by_line():
        count = 0
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                count += 1
        return count
 
    # Метод 2: readlines()
    def read_all_lines():
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return len(lines)
 
    # Метод 3: read() (весь файл целиком)
    def read_whole_file():
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return len(content)
 
    benchmark(read_line_by_line, "Построчное чтение (for line)")
    benchmark(read_all_lines, "readlines()")
    benchmark(read_whole_file, "read() (целиком)")
 
 
def test_block_sizes():
    """Чтение блоками разного размера."""
    print("\n=== ЧТЕНИЕ БЛОКАМИ РАЗНОГО РАЗМЕРА ===")
 
    # Создаем файл 10 МБ
    filename = "test_large.bin"
    size_mb = 10
    print(f"  Создание файла {size_mb} МБ...")
    with open(filename, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))
 
    block_sizes = [1, 256, 1024, 4096, 65536, 1024*1024]
 
    for bs in block_sizes:
        def read_blocks(block_size=bs):
            total = 0
            with open(filename, "rb") as f:
                while True:
                    chunk = f.read(block_size)
                    if not chunk:
                        break
                    total += len(chunk)
            return total
 
        if bs < 1024:
            label = f"Блок {bs} байт"
        elif bs < 1024 * 1024:
            label = f"Блок {bs // 1024} КБ"
        else:
            label = f"Блок {bs // (1024*1024)} МБ"
 
        benchmark(read_blocks, label)
 
 
def cleanup():
    """Удаление тестовых файлов."""
    for f in ["test_write1.txt", "test_write2.txt",
              "test_write3.txt", "test_large.bin"]:
        if os.path.exists(f):
            os.remove(f)
 
 
if __name__ == "__main__":
    print("=" * 55)
    print("  БЕНЧМАРК ФАЙЛОВОГО ВВОДА-ВЫВОДА")
    print("=" * 55)
 
    test_write_methods()
    test_read_methods()
    test_block_sizes()
    cleanup()
 
    print("\nТестовые файлы удалены.")

