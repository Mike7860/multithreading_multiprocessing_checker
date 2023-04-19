import time
from multiprocessing import Process
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor


def big_counter() -> None:
    for _ in range(99999999):
        pass


def multiprocessing_for_many_io_operations() -> None:
    filename: str = 'test.txt'
    process_lock = Lock()

    class MyProcess(Process):
        def __init__(self, func, lock):
            super().__init__()
            self.func = func
            self.lock = lock

        def run(self) -> None:
            with self.lock:
                self.func()

    def read_from_file() -> int:
        with open(filename, 'r+') as file:
            value = file.read()
            return int(value)

    def write_to_file(value: int) -> None:
        with open(filename, 'w') as file:
            file.write(str(value))

    def increment_value_in_file():
        value = read_from_file()
        write_to_file(value + 1)

    write_to_file(0)
    start = time.time()
    processes = []

    for i in range(10000):
        processes.append(MyProcess(increment_value_in_file, process_lock))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    stop = time.time()
    print("High IO operations amount case: exec time for processes:", stop - start, "[s]")


def multithreading_for_many_io_operations() -> None:
    filename: str = 'test.txt'
    lock = Lock()

    def read_from_file() -> int:
        with open(filename, 'r+') as file:
            value = file.read()
            return int(value)

    def write_to_file(value: int) -> None:
        with open(filename, 'w') as file:
            file.write(str(value))

    def increment_value_in_file():
        with lock:
            value = read_from_file()
            write_to_file(value + 1)

    write_to_file(0)
    start = time.time()

    with ThreadPoolExecutor(10000) as executor:
        for _ in range(10000):
            executor.submit(increment_value_in_file)
    stop = time.time()
    print("High IO operations amount case: exec time for threads:", stop-start, "[s]")


def multiprocessing_for_high_cpu_using() -> None:
    processes = []

    for _ in range(10):
        processes.append(Process(target=big_counter))

    start = time.time()

    for t in processes:
        t.start()

    for t in processes:
        t.join()

    stop = time.time()
    print("High CPU using case: exec time for processes:", stop-start, "[s]")


def multithreading_for_high_cpu_using() -> None:
    threads = []

    for _ in range(10):
        threads.append((Thread(target=big_counter)))

    start = time.time()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    stop = time.time()
    print("High CPU using case: exec time for threads:", stop-start, "[s]")


#multiprocessing_for_many_io_operations()
multithreading_for_many_io_operations()
multiprocessing_for_high_cpu_using()
multithreading_for_high_cpu_using()
