#!/bin/zsh

for i in {1..23}
do
  ls ./data/collected_data2/level_$i/ | wc -lw
done
