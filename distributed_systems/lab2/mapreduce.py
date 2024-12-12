import multiprocessing
from collections import defaultdict
import os
import time


def worker_map(child_connection, worker_id):
    """Proces WORKER: faza MAP."""
    word_counts = defaultdict(int)
    
    while True:
        task = child_connection.recv()
        if task == "DONE":
            break
        line_index, line = task
        for word in line.strip().split():
            word_counts[word] += 1
    child_connection.send(dict(word_counts))
    print(f"WORKER {worker_id} zakończył pracę.")

def worker_reduce(child_connection, worker_id):
    """Proces WORKER: faza REDUCE."""
    
    word_counts = defaultdict(int)
    while True:
        task = child_connection.recv()
        if task == "DONE":
            break

        for partial_result in task:
            for word, count in partial_result.items():
                word_counts[word] += count
    child_connection.send(dict(word_counts)) 
    print(f"WORKER {worker_id} zakończył pracę.")


def master(file_path, num_workers):
    """Proces MASTER."""
    map_pipes = [multiprocessing.Pipe() for _ in range(num_workers)]
    reduce_pipes = [multiprocessing.Pipe() for _ in range(num_workers)]

    map_workers = [
        multiprocessing.Process(target=worker_map, args=(pipe[1], i))
        for i, pipe in enumerate(map_pipes)
    ]

    reduce_workers = [
        multiprocessing.Process(target=worker_reduce, args=(pipe[1], i))
        for i, pipe in enumerate(reduce_pipes)
    ]

    for w in map_workers + reduce_workers:
        w.start()

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            map_pipes[i % num_workers][0].send((i, line))

    for pipe in map_pipes:
        pipe[0].send("DONE")

    map_results = []
    for pipe in map_pipes:
        while True:
            result = pipe[0].recv()
            map_results.append(result)
            break

    grouped_results = [list() for _ in range(num_workers)]
    for i, result in enumerate(map_results):
        grouped_results[i % num_workers].append(result)

    for i, pipe in enumerate(reduce_pipes):
        pipe[0].send(grouped_results[i])
        pipe[0].send("DONE")

    final_counts = defaultdict(int)
    for pipe in reduce_pipes:
        reduce_result = pipe[0].recv()
        for word, count in reduce_result.items():
            final_counts[word] += count

    for w in map_workers + reduce_workers:
        w.join()

    print("Wyniki WordCount:")
    for word, count in sorted(final_counts.items()):
        print(f"{word}: {count}")


if __name__ == "__main__":
    input_file = "example.txt"
    if not os.path.exists(input_file):
        with open(input_file, "w") as f:
            f.write(
                """Sure, here are 6 random sentences in English with some repetition:

1. The cat loves to run around the garden.
2. It's always important to take care of your health.
3. In the garden, there are beautiful flowers blooming.
4. The cat loves to run around the garden because there is plenty of space.
5. Taking care of your health is essential for feeling good every day.
6. In the garden, there are flowers that attract bees and butterflies.

These sentences contain some repetition and can serve as input for your task. Let me know if you'd like further adjustments!"""
            )
    num_workers = 4
    master(input_file, num_workers)
