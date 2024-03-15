#!/bin/bash

# Directory containing the level directories
src_dir="./data/collected_data_dot/"

# Destination base directory
dest_dir="./data/training_data3/"

# Iterate over each level directory in the source directory
for level_dir in $(ls $src_dir); 
do
  echo "Processing $level_dir..."

  # Make sure the corresponding destination directory exists
  mkdir -p "$dest_dir/$level_dir"

  # List files in the current level directory, sorted by the number of frames (ascending),
  # then select the first 30 files
  # Assumes file names are in the format {number_of_frames}frames_round{round_number}.json
  ls "$src_dir/$level_dir" | sort -n -t_ -k1 | head -n 30 | while read file; 
  do
    # Move the selected files to the corresponding directory in ../training_data3
    cp "$src_dir/$level_dir/$file" "$dest_dir/$level_dir/"
  done
done

echo "Files moved successfully."

# cd ./data/training_data3

# # Iterate over each level directory in the source directory
# for level in {2..23}; 
# do
#   echo "Processing $level..."
#   mv level_$level/* ../
#   rm -rf level_$level
# done

# echo "Files moved successfully."