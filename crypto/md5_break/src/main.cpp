#include <iostream>
#include <array>
#include <cassert>
#include <cstdint>
#include <vector>
#include <chrono>
#include "hash.hpp"

extern void generate_candidates_cuda(
    const uint32_t* state,
    uint32_t* candidates,
    uint8_t* found,
    size_t iterations,
    size_t threads_per_block,
    size_t block_dim,
    size_t seed
);

struct Collision {
    std::array<uint32_t, 16> m0;
    std::array<uint32_t, 16> m1;
    std::array<uint32_t, 16> m0_prim;
    std::array<uint32_t, 16> m1_prim;
    std::array<uint32_t, 4> hash;

    friend std::ostream& operator<<(std::ostream& os, const Collision& collision) {
        auto print_array = [&os](const auto& arr, const std::string& label) {
            os << label << ": [";
            for (size_t i = 0; i < arr.size(); ++i) {
                os << "0x" << std::hex << arr[i];
                if (i != arr.size() - 1) os << ", ";
            }
            os << "]\n";
        };

        print_array(collision.m0, "m0");
        print_array(collision.m1, "m1");
        print_array(collision.m0_prim, "m0_prim");
        print_array(collision.m1_prim, "m1_prim");

        os << "hash: [";
        for (size_t i = 0; i < collision.hash.size(); ++i) {
            os << "0x" << std::hex << collision.hash[i];
            if (i != collision.hash.size() - 1) os << ", ";
        }
        os << "]";
        return os;
    }
};

Collision second_step(const std::array<uint32_t, 16>& m0, const std::array<uint32_t, 16>& m0_prim) {
    std::array<uint32_t, 16> delta_m0;
    for (size_t i = 0; i < 16; ++i) {
        delta_m0[i] = m0_prim[i] ^ m0[i];
    }

    const std::array<uint32_t, 16> M0_DELTA = {
        0,
        0,
        0,
        0,
        1U << 31,  // 2^31
        0,
        0,
        0,
        0,
        0,
        0,
        1U << 15,  // 2^15
        0,
        0,
        1U << 31,  // 2^31
        0,
    };
    assert(delta_m0 == M0_DELTA);

    const std::array<uint32_t, 4> INITIAL_STATE = {0, 0, 0, 0}; // Replace with actual state
    auto state_m0 = hash_init(m0);
    auto state_m0_prim = hash_init(m0_prim);

    const size_t ITERATIONS = 5000000;
    const size_t THREADS_PER_BLOCK = 256;
    const size_t BLOCK_DIM = 352;
    const size_t BATCH_SIZE = THREADS_PER_BLOCK * BLOCK_DIM;

    std::vector<uint32_t> candidates(16 * BATCH_SIZE);
    size_t candidate_counter = 0;
    size_t loop_counter = 0;
    // Start measuring time for the current loop
    auto start_time = std::chrono::high_resolution_clock::now();

    while (true) {
        std::vector<uint8_t> found(BATCH_SIZE, 0);
    
        generate_candidates_cuda(
            state_m0.data(),
            candidates.data(),
            found.data(),
            ITERATIONS,
            THREADS_PER_BLOCK,
            BLOCK_DIM,
            rand()
        );

        for (size_t i = 0; i < BATCH_SIZE; ++i) {
            if (found[i]) {
                ++candidate_counter;
                std::array<uint32_t, 16> candidate;
                std::array<uint32_t, 16> candidate_prim;

                std::copy(candidates.begin() + i * 16, candidates.begin() + (i + 1) * 16, candidate.begin());
                for (size_t j = 0; j < 16; ++j) {
                    candidate_prim[j] = candidate[j] ^ delta_m0[j];
                }

                if (hash(state_m0, candidate) == hash(state_m0_prim, candidate_prim)) {
                    auto end_time = std::chrono::high_resolution_clock::now();
                    std::chrono::duration<double> elapsed = end_time - start_time;

                    return Collision{m0, candidate, m0_prim, candidate_prim, state_m0};
                }
            }
        }

        // Measure time for the loop
        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end_time - start_time;
        ++loop_counter;
        std::cout << "Loop: " << loop_counter << ", Candidates: " << candidate_counter 
                  << ", Time since start: " << elapsed.count() << " seconds\n";
    }
}

int main() {
    // Initial state
    const std::array<uint32_t, 16> m0 = {
        0x2dd31d1, 0xc4eee6c5, 0x69a3d69, 0x5cf9af98, 0x87b5ca2f, 0xab7e4612, 0x3e580440,
        0x897ffbb8, 0x634ad55, 0x2b3f409, 0x8388e483, 0x5a417125, 0xe8255108, 0x9fc9cdf7,
        0xf2bd1dd9, 0x5b3c3780
    };

    // After step 1
    const std::array<uint32_t, 16> m0_prim = {
        0x2dd31d1, 0xc4eee6c5, 0x69a3d69, 0x5cf9af98, 0x7b5ca2f, 0xab7e4612, 0x3e580440,
        0x897ffbb8, 0x634ad55, 0x2b3f409, 0x8388e483, 0x5a41f125, 0xe8255108, 0x9fc9cdf7,
        0x72bd1dd9, 0x5b3c3780
    };

    // Compute the collision
    Collision collision = second_step(m0, m0_prim);

    // Print collision found
    std::cout << "Collision found:\n";
    std::cout << collision;

    assert(
        hash(hash_init(collision.m0), collision.m1) ==
        hash(hash_init(collision.m0_prim), collision.m1_prim)
    );

    std::cout << "Collision verified!" << std::endl;

    return 0;
}
