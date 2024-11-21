#!/bin/bash

# Compile CUDA file with nvcc
nvcc -c src/kernel.cu -o src/kernel.o

# Compile C++ files and link them
g++ src/main.cpp src/hash.cpp src/kernel.o -o md5_break -lmbedtls -lmbedcrypto -lcudart

echo "Compilation complete. Run './md5_break' to execute."