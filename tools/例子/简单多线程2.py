from multiprocessing import Process
def spawn_n_processes(n, target):

    threads = []

    for _ in range(n):
        thread = Process(target=target)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
if __name__ == '__main__':
    test(fib, spawner=spawn_n_processes)
