#include "hash.hpp"
#include "mbedtls/md5.h"
#include <string.h>

// int mbedtls_md5_starts(mbedtls_md5_context *ctx){
//     ctx->private_total[0] = 0;
//     ctx->private_total[1] = 0;

//     ctx->private_state[0] = 0x67452301;
//     ctx->private_state[1] = 0xEFCDAB89;
//     ctx->private_state[2] = 0x98BADCFE;
//     ctx->private_state[3] = 0x10325476;

//     return 0;
// }

void calculate_md5(uint8_t *input, size_t input_len, uint8_t *output) {
    mbedtls_md5_context ctx;
    mbedtls_md5_init(&ctx);
    mbedtls_md5_starts(&ctx);
    mbedtls_md5_update(&ctx, input, input_len);
    mbedtls_md5_finish(&ctx, output);
}


std::array<uint32_t, 4> hash(const std::array<uint32_t, 4>& state, const std::array<uint32_t, 16>& message) {
    mbedtls_md5_context ctx;
    mbedtls_md5_init(&ctx);

    // Clone the provided state into the context
    ctx.private_state[0] = state[0];
    ctx.private_state[1] = state[1];
    ctx.private_state[2] = state[2];
    ctx.private_state[3] = state[3];

    // Start processing the message
    mbedtls_md5_update(&ctx, reinterpret_cast<const uint8_t*>(message.data()), message.size() * sizeof(uint32_t));

    // Extract the resulting state
    std::array<uint32_t, 4> output_state = {
        ctx.private_state[0],
        ctx.private_state[1],
        ctx.private_state[2],
        ctx.private_state[3]
    };

    return output_state;
}

std::array<uint32_t, 4> hash_init(const std::array<uint32_t, 16>& message) {
    mbedtls_md5_context ctx;
    mbedtls_md5_init(&ctx);

    // Initialize MD5 with the default state
    mbedtls_md5_starts(&ctx);

    // Process the message
    mbedtls_md5_update(&ctx, reinterpret_cast<const uint8_t*>(message.data()), message.size() * sizeof(uint32_t));

    // Extract the resulting state
    std::array<uint32_t, 4> output_state = {
        ctx.private_state[0],
        ctx.private_state[1],
        ctx.private_state[2],
        ctx.private_state[3]
    };

    return output_state;
}
