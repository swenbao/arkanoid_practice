# #!/bin/zsh

# # Directory for storing win rate files
# WIN_RATE_DIR="./model_win_rate"

# # Ensure the win rate directory exists
# mkdir -p "$WIN_RATE_DIR"

# # Run models from K=1 to K=10
# for k in {1..10}
# do
#   echo "Running model for K=$k"
  
#   # Iterate through levels 1 to 24
#   for level in {1..24}
#   do
#     echo "Processing Level $level for K=$k"

#     # Set the K and LEVEL environment variables for the Python script
#     export K=$k
#     export LEVEL=$level

#     # Start the Python game in the background and get its PID
#     python -m mlgame --no-display -f 1000000 -i ./ml/ml_play_model.py . --difficulty NORMAL --level $level &
#     PYTHON_PID=$!

#     # Monitor for the existence of '10.win' or '10.lost' in the win rate file
#     while true
#     do
#       if grep -E '10\.(won|lost)' "$WIN_RATE_DIR/new_big${K}nn_model_win_rate.txt" > /dev/null; then
#         echo "10 rounds completed for Level $level and K=$k. Terminating the game."
#         kill $PYTHON_PID
#         break
#       else
#         sleep 1  # Check every 1 second
#       fi
#     done

#     # Calculate and append win rate information for the current level
#     wins=$(grep -c 'won' "$WIN_RATE_DIR/new_big${K}nn_model_win_rate.txt")
#     losses=$(grep -c 'lost' "$WIN_RATE_DIR/new_big${K}nn_model_win_rate.txt")
#     total=$((wins + losses))
#     win_rate=$(echo "scale=2; $wins / $total * 100" | bc)

#     # Append summary for the current level to the win rate file
#     echo -e "Level: $level\nTotal: $total rounds\nWin: $wins rounds\nWin Rate: $win_rate%" >> "$WIN_RATE_DIR/new_big${K}nn_model_win_rate.txt"

#   done  # End of level loop

# done  # End of K loop

# echo "All models evaluation completed."

############################################

#!/bin/zsh

WIN_RATE_DIR="./model_win_rate/"
mkdir -p "$WIN_RATE_DIR"

# Run models from K=1 to K=19
for k in {1..19}
do
  echo "Running model for K=$k"

  # Run through levels 1 to 24
  for level in {1..24}
  do
    echo "Processing Level $level for K=$k"

    temp_win_rate_file="$WIN_RATE_DIR/temp_dot2_${k}nn_level${level}_win_rate.txt"
    > "$temp_win_rate_file"  # Clear the temporary win rate file for the current level

    export K=$k

    # Run the game 10 times for the current level
    for round in {1..10}
    do
      echo "Round $round for Level $level and K=$k"
      
      # Start the Python game with the --one-shot flag
      python -m mlgame --no-display -f 1000000 --one-shot -i ./ml/ml_play_model.py . --difficulty NORMAL --level $level

      # Since the game terminates after one round, there's no need to monitor and kill the process
      # The game's result (won/lost) for each round will be automatically appended to the designated file by the game script
    done

    # Summarize the win rate after 10 rounds
    wins=$(grep -c 'won' "$WIN_RATE_DIR/dot2_${k}nn_level${level}_win_rate.txt")
    losses=$(grep -c 'lost' "$WIN_RATE_DIR/dot2_${k}nn_level${level}_win_rate.txt")
    total=$((wins + losses))
    win_rate=$(echo "scale=2; $wins / $total * 100" | bc -l)

    # Append summary for the current level to the main win rate file
    echo "Level: $level\nTotal: $total rounds\nWin: $wins rounds\nWin Rate: $win_rate%%\n----------------------\n" >> "$WIN_RATE_DIR/dot2_${k}nn_model_win_rate.txt"
  done
done

echo "All models evaluation completed."