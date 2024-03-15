#!/bin/zsh

# Directory to store collected data
DATA_DIR="./data/collected_data_dot2"

# how many data I want to collect in each level
HOW_MANY=20

# Ensure the data directory exists
mkdir -p "$DATA_DIR"

# Iterate from level 1 to 24
for level in {1..24}
do
  echo "Running level $level"

  # Create or clear a directory for the current level's data
  LEVEL_DIR="$DATA_DIR/level_$level"
  mkdir -p "$LEVEL_DIR"
  > "$LEVEL_DIR/round_info.txt"  # Assuming you want to store some round-specific information here

  # Run the game for 20 rounds
  for round in {1..$HOW_MANY}
  do
    echo "Round $round for Level $level"

    # Start the Python game with the --one-shot flag
    python -m mlgame --no-display -f 1000000 --one-shot -i ./ml/dot.py . --difficulty NORMAL --level $level

    # Since the game terminates after one round, there's no need to monitor and kill the process
    # Your game script should handle data collection and file writing per round
  done

  # After 20 rounds, process the collected data as needed
  echo "Completed 20 rounds for Level $level."
  # Here, you might process or summarize the data collected in LEVEL_DIR
done

echo "All levels completed."