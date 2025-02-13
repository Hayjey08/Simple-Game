# Simple Collecting Game

A challenging game where you control a blue square to collect yellow stars while avoiding moving red obstacles. Complete all 5 levels to win!

## How to Play

1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Run the game:
```
python game.py
```

## Controls

- Use arrow keys (↑, ↓, ←, →) to move the blue square
- Collect yellow stars to increase your score
- Avoid red obstacles
- If you hit an obstacle or run out of time, the game ends
- Press 'R' to restart when game is over
- Press 'SPACE' to proceed to the next level when you complete a level
- Close the window to quit the game

## Game Features

- 5 increasingly difficult levels
- Level-specific requirements:
  - Level 1: Collect 10 stars in 20 seconds
  - Level 2: Collect 10 stars in 25 seconds
  - Level 3: Collect 15 stars in 25 seconds
  - Level 4: Collect 20 stars in 25 seconds
  - Level 5: Collect 25 stars in 25 seconds
- Moving obstacles with different patterns:
  - Level 1: Horizontal moving obstacles
  - Level 2: Adds vertical moving obstacles
  - Level 3: Adds circular moving obstacles
  - Level 4 & 5: Adds chasing obstacles that follow the player
- Increased player speed in higher levels
- More obstacles in higher levels
- Score resets to 0 at the start of each new level

## Level Progression

Each level becomes progressively harder with:
- More stars required to complete each level (+5 stars per level)
- More obstacles with different movement patterns
- Faster moving obstacles
- More stars available to collect
- Increased player movement speed to help with the challenge
- Score resets at the start of each new level
