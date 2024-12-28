import multiprocessing
from collections import defaultdict
import os
import time

def worker_map(child_connection, working_function, worker_id):
    working_function(child_connection)
    print(f"WORKER Map {worker_id} zakończył pracę.")

def worker_reduce(child_connection, working_function, worker_id):
    working_function(child_connection)
    print(f"WORKER Reduce {worker_id} zakończył pracę.")

def mapreduce(file_path, num_workers, map_function, reduce_function):
    map_pipes = [multiprocessing.Pipe() for _ in range(num_workers)]
    reduce_pipes = [multiprocessing.Pipe() for _ in range(num_workers)]

    map_workers = [
        multiprocessing.Process(target=worker_map, args=(pipe[1], map_function, i))
        for i, pipe in enumerate(map_pipes)
    ]

    reduce_workers = [
        multiprocessing.Process(target=worker_reduce, args=(pipe[1], reduce_function, i))
        for i, pipe in enumerate(reduce_pipes)
    ]

    for w in map_workers + reduce_workers:
        w.start()

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            map_pipes[i % num_workers][0].send((line))

    for pipe in map_pipes:
        pipe[0].send("DONE")

    map_results = []
    for i in range(num_workers):
        pipe = map_pipes[i]
        proc = map_workers[i]
        while True:
            result = pipe[0].recv()
            if result == "DONE":
                break
            map_results.append(result)
    
    map_results.sort(key=lambda x: x[0])

    grouped_results = [list() for _ in range(num_workers)]
    
    worker_i = 0
    for i in range(len(map_results)):
        current_result_key = map_results[i][0]
        next_result_key = map_results[i+1][0] if i+1 < len(map_results) else None

        grouped_results[worker_i].append(map_results[i])

        if current_result_key != next_result_key:
            worker_i = (worker_i + 1)%num_workers

    for i, pipe in enumerate(reduce_pipes):
        for tupl in grouped_results[i]:
            pipe[0].send(tupl)
        pipe[0].send("DONE")

    final_counts = dict()
    for pipe in reduce_pipes:
        while True:
            reduce_result = pipe[0].recv()
            if reduce_result == "DONE":
                break
            key, value = reduce_result
            
            final_counts[key] = value

    for w in map_workers + reduce_workers:
        w.join()

    for word, count in sorted(final_counts.items()):
        print(f"{word}: {count}")

