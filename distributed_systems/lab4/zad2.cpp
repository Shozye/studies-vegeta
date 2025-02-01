#include <cstdlib>      // exit(1)
#include <chrono>       // std::chrono
#include <cstdint>      // uint64_t
#include <pthread.h>    // pthread_mutex_t, pthread_exit(NULL)
#include <memory>       // std::make_unique
#include <cstddef>      // NULL
#include <cstdio>       // printf
#include <sys/types.h>  // waitpid
#include <sys/wait.h>   // waitpid
#include <iostream>     
#include<vector>
#include <fstream>
#include <sstream>


static uint64_t millis(){
    return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
}

typedef struct {
    uint64_t worker_id;
    uint64_t thread_id;
    uint64_t uids_per_thread;
    uint64_t millis_since_start;
} ThreadArgs;

typedef struct {
    uint64_t timestamp;
    uint64_t worker_id;
    uint64_t thread_id;
    uint64_t seq_num;
} UIDGeneratorData;


static pthread_mutex_t g_file_mutex = PTHREAD_MUTEX_INITIALIZER;
static FILE* shared_file = nullptr; 


static std::string make_uid_string(const UIDGeneratorData& gen) {
    // format: "timestamp-worker-thread-seq"
    std::ostringstream oss;
    oss << gen.timestamp << "-"
        << gen.worker_id << "-"
        << gen.thread_id << "-"
        << gen.seq_num;
    return oss.str();
}

static void *thread_task(void *arg) {
    std::vector<std::string> uids_buffer;

    std::unique_ptr<ThreadArgs> args(static_cast<ThreadArgs*>(arg)); 
    UIDGeneratorData generator = {
        .timestamp = millis()-args->millis_since_start, 
        .worker_id = args->worker_id, 
        .thread_id = args->thread_id, 
        .seq_num = 0}
    ;
    for (uint64_t i = 0; i < args->uids_per_thread; i++) {
        uint64_t new_timestamp = millis()-args->millis_since_start;
        if(new_timestamp != generator.timestamp){
            generator.timestamp = new_timestamp;
            generator.seq_num = 0;
        }
        std::string uid = make_uid_string(generator);
        generator.seq_num++;
        uids_buffer.push_back(uid);

        if (uids_buffer.size() >= 1000) {
            pthread_mutex_lock(&g_file_mutex);
            for (const auto &str : uids_buffer) {
                fprintf(shared_file, "%s\n", str.c_str());
            }
            fflush(shared_file);
            pthread_mutex_unlock(&g_file_mutex);

            uids_buffer.clear();
        }
    }
    pthread_exit(NULL);
}

static void worker_task(
    uint64_t worker_id, 
    uint64_t num_threads, 
    uint64_t uids_per_thread, 
    uint64_t milliseconds_since_epoch
) {
    std::string filename = "uids/" + std::to_string(worker_id) + ".txt";
    shared_file = fopen(filename.c_str(), "a");
    if (!shared_file) {
        std::cerr << "Failed to open output file.\n";
        exit(1);
    }


    pthread_t threads[num_threads];

    for (size_t i = 0; i < num_threads; i++) {
        auto args = std::make_unique<ThreadArgs>();
        args->worker_id = worker_id;
        args->thread_id = i;
        args->uids_per_thread = uids_per_thread;
        args->millis_since_start = milliseconds_since_epoch;
        
        pthread_create(&threads[i], NULL, thread_task, args.release());
    }

    for (size_t i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
}

int main() {
    uint64_t total_uids = 10000000;
    uint64_t num_workers = (1 << 6) - 1;
    uint64_t num_threads = (1 << 6) - 1;
    uint64_t uids_per_thread = (total_uids / (num_workers * num_threads)) + 1; 

    printf("Workers: %zu\n", num_workers);
    printf("Threads per Worker: %zu\n", num_threads);
    printf("UIDs per Thread: %zu\n", uids_per_thread);

    pid_t pids[num_workers];

    uint64_t milliseconds_since_epoch = millis();

    for (size_t i = 0; i < num_workers; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            worker_task(i, num_threads, uids_per_thread, milliseconds_since_epoch);
            exit(0);
        } else {
            pids[i] = pid;
        }
    }

    for (size_t i = 0; i < num_workers; i++) {
        waitpid(pids[i], NULL, 0);
    }

    uint64_t end = millis();
    double elapsed_time = end - milliseconds_since_epoch;
    printf("Total time: %.2f ms\n", elapsed_time);
    printf("Generation speed: %.2f Millions of UID/s\n", ((double)total_uids/((double)elapsed_time/1000))/1000000);
}
