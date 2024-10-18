# FishBot

FishBot is a Tetris bot created over the summer holiday as a project. It uses a beam search algorithm to determine the optimal piece placements base on the heuristics defined. 

As of the moment, the heuristic considers:
- Number of line clears
- Number of cavities/holes in the stack
- Bumpiness of the stack
- Height of the stack

<!-- GETTING STARTED -->
## Getting Started
To run the bot locally, clone the repository.
Ensure you have python3 installed.

To run the bot:
  ```sh
  export PYTHONPATH=/Path-To-FishBot/:$PYTHONPATH
  python bot/bot.py
  ```
