
from collections import defaultdict
import mapreduce

def word_count_map(child_connection):
    while True:
        task = child_connection.recv()
        if task == "DONE":
            break
        line = task
        for word in line.strip().split():
            child_connection.send((word, 1))
    child_connection.send("DONE")

def word_count_reduce(child_connection):
    word_counts = defaultdict(int)
    while True:
        task = child_connection.recv()
        if task == "DONE":
            break
        key, count = task
        word_counts[key] += count

    print("From reduce: ", word_counts)
    for key, value in word_counts.items():
        child_connection.send((key, value)) 
    child_connection.send("DONE")


# map i reduce musza byc skonsturowane tak zeby sie konczyly po otrzymaniu wiadomosci DONE.
if __name__ == "__main__":
    input_file = "example.txt"
    num_workers = 4
    mapreduce.mapreduce(
        file_path=input_file, 
        num_workers=num_workers, 
        map_function=word_count_map, 
        reduce_function=word_count_reduce
    )
   