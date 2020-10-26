#!/bin/bash
rm -r ../data/result/galaxycluster
mkdir ../data/result/galaxycluster

for i in {1..100}; do
    mkdir ../data/result/galaxycluster/$i
done