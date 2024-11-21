#pragma once
#include<array>
#include<cstdint>

std::array<uint32_t, 4> hash(const std::array<uint32_t, 4>& state, const std::array<uint32_t, 16>& message);
std::array<uint32_t, 4> hash_init(const std::array<uint32_t, 16>& message);

