#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mbedtls/md5.h"

uint8_t M0[64] = {
    0xd1, 0x31, 0xdd, 0x02, // 0x02dd31d1,
    0xc5, 0xe6, 0xee, 0xc4, // 0xc4eee6c5,
    0x69, 0x3d, 0x9a, 0x06, // 0x069a3d69,
    0x98, 0xaf, 0xf9, 0x5c, // 0x5cf9af98,
    0x2f, 0xca, 0xb5, 0x87, // 0x87b5ca2f,
    0x12, 0x46, 0x7e, 0xab, // 0xab7e4612,
    0x40, 0x04, 0x58, 0x3e, // 0x3e580440,
    0xb8, 0xfb, 0x7f, 0x89, // 0x897ffbb8,
    0x55, 0xad, 0x34, 0x06, // 0x0634ad55,
    0x09, 0xf4, 0xb3, 0x02, // 0x02b3f409,
    0x83, 0xe4, 0x88, 0x83, // 0x8388e483,
    0x25, 0x71, 0x41, 0x5a, // 0x5a417125,
    0x08, 0x51, 0x25, 0xe8, // 0xe8255108,
    0xf7, 0xcd, 0xc9, 0x9f, // 0x9fc9cdf7,
    0xd9, 0x1d, 0xbd, 0xf2, // 0xf2bd1dd9,
    0x80, 0x37, 0x3c, 0x5b, // 0x5b3c3780,
};

uint8_t M1[64] = {
    0x96, 0x0b, 0x1d, 0xd1, // 0xd11d0b96
    0xdc, 0x41, 0x7b, 0x9c, // 0x9c7b41dc
    0xe4, 0xd8, 0x97, 0xf4, // 0xf497d8e4
    0x5a, 0x65, 0x55, 0xd5, // 0xd555655a
    0x35, 0x73, 0x9a, 0xc7, // 0xc79a7335
    0xf0, 0xeb, 0xfd, 0x0c, // 0x0cfdebf0
    0x30, 0x29, 0xf1, 0x66, // 0x66f12930
    0xd1, 0x09, 0xb1, 0x8f, // 0x8fb109d1
    0x75, 0x27, 0x7f, 0x79, // 0x797f2775
    0x30, 0xd5, 0x5c, 0xeb, // 0xeb5cd530
    0x22, 0xe8, 0xad, 0xba, // 0xbaade822
    0x79, 0xcc, 0x15, 0x5c, // 0x5c15cc79
    0xed, 0x74, 0xcb, 0xdd, // 0xddcb74ed
    0x5f, 0xc5, 0xd3, 0x6d, // 0x6dd3c55f
    0xb1, 0x9b, 0x0a, 0xd8, // 0xd80a9bb1
    0x35, 0xcc, 0xa7, 0xe3, // 0xe3a7cc35
};

uint8_t M0_prime[64] = {
    0xd1, 0x31, 0xdd, 0x02, // 0x02dd31d1,
    0xc5, 0xe6, 0xee, 0xc4, // 0xc4eee6c5,
    0x69, 0x3d, 0x9a, 0x06, // 0x069a3d69,
    0x98, 0xaf, 0xf9, 0x5c, // 0x5cf9af98,
    0x2f, 0xca, 0xb5, 0x07, // 0x07b5ca2f,
    0x12, 0x46, 0x7e, 0xab, // 0xab7e4612,
    0x40, 0x04, 0x58, 0x3e, // 0x3e580440,
    0xb8, 0xfb, 0x7f, 0x89, // 0x897ffbb8,
    0x55, 0xad, 0x34, 0x06, // 0x0634ad55,
    0x09, 0xf4, 0xb3, 0x02, // 0x02b3f409,
    0x83, 0xe4, 0x88, 0x83, // 0x8388e483,
    0x25, 0xf1, 0x41, 0x5a, // 0x5a41f125,
    0x08, 0x51, 0x25, 0xe8, // 0xe8255108,
    0xf7, 0xcd, 0xc9, 0x9f, // 0x9fc9cdf7,
    0xd9, 0x1d, 0xbd, 0x72, // 0x72bd1dd9,
    0x80, 0x37, 0x3c, 0x5b, // 0x5b3c3780,
};

uint8_t M1_prime[64] = {
    0x96, 0x0b, 0x1d, 0xd1, // 0xd11d0b96
    0xdc, 0x41, 0x7b, 0x9c, // 0x9c7b41dc
    0xe4, 0xd8, 0x97, 0xf4, // 0xf497d8e4
    0x5a, 0x65, 0x55, 0xd5, // 0xd555655a
    0x35, 0x73, 0x9a, 0x47, // 0x479a7335
    0xf0, 0xeb, 0xfd, 0x0c, // 0x0cfdebf0
    0x30, 0x29, 0xf1, 0x66, // 0x66f12930
    0xd1, 0x09, 0xb1, 0x8f, // 0x8fb109d1
    0x75, 0x27, 0x7f, 0x79, // 0x797f2775
    0x30, 0xd5, 0x5c, 0xeb, // 0xeb5cd530
    0x22, 0xe8, 0xad, 0xba, // 0xbaade822
    0x79, 0x4c, 0x15, 0x5c, // 0x5c154c79
    0xed, 0x74, 0xcb, 0xdd, // 0xddcb74ed
    0x5f, 0xc5, 0xd3, 0x6d, // 0x6dd3c55f
    0xb1, 0x9b, 0x0a, 0x58, // 0x580a9bb1
    0x35, 0xcc, 0xa7, 0xe3, // 0xe3a7cc35
};

void calculate_md5(uint8_t *input, size_t input_len, uint8_t *output) {
    mbedtls_md5_context ctx;
    mbedtls_md5_init(&ctx);
    mbedtls_md5_starts(&ctx);
    mbedtls_md5_update(&ctx, input, input_len);
    mbedtls_md5_finish(&ctx, output);
}

void compute_concat_md5(uint8_t *M0, size_t M0_len, uint8_t *M1, size_t M1_len, uint8_t *output) {
    uint8_t *combined_M0 = malloc(M0_len + M0_len); 
    memcpy(combined_M0, M0, M0_len);
    memcpy(combined_M0 + M0_len, M1, M1_len);

    calculate_md5(combined_M0, M0_len + M1_len, output);
    free(combined_M0);
}

void print_hash(uint8_t* hash, size_t len) {
    for (int i = 0; i < len; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

int is_collision(uint8_t* m0, uint8_t* m00, uint8_t* m1, uint8_t* m11, int print) {
    uint8_t hash1[16], hash2[16];
    compute_concat_md5(m0, sizeof(m0), m1, sizeof(m1), hash1);
    compute_concat_md5(m00, sizeof(m00), m11, sizeof(m11), hash2);
    int has_collided = (memcmp(hash1, hash2, 16) == 0);

    if (print == 1){
        printf("MD5(MD5(IV, M0 ), M1 ): ");
        print_hash(hash1, sizeof(hash1));

        printf("MD5(MD5(IV, M'0), M'1): ");
        print_hash(hash2, sizeof(hash2));

        if (memcmp(hash1, hash2, sizeof(hash1)) == 0) {
            printf("Collision detected. Hashes are the same.\n");
        } else {
            printf("No collision.\n");
        }
    }

    return has_collided;
}

int is_collision(uint8_t* m0, uint8_t* m00, uint8_t* m1, uint8_t* m11){
    is_collision(m0, m00, m1, m11, 0);
}

int main() {
    is_collision(M0, M0_prime, M1, M1_prime, 1);

    
    return 0;
}

