#!/bin/bash

mkdir out
rm out/out.out
touch out/out.out


for i in {1..12} {a..d}
do
    julia zad1.jl data/gap${i}.txt > out/gap${i}.out
    
    echo "file gap$i.txt" >> out/out.out
    julia zad1.jl data/gap${i}.txt >> out/out.out
done