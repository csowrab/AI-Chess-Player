# AI-Chess-Player:
## About:
A chess game made through Pygame and Scikit-learn. Main focus of the coursework is on the "AI" of the game, allowing you to face it in 3 difficulties.

"AiChessGame" is the actual python file, running this (along with its import dependencies) should run the game.
"MLP_NET" JSON files are the actual AIs, each of different difficulties to load to the game.

## Requirements:
1. Python version 3.0 or above.
2. [Pygame](https://pypi.org/project/pygame/)
3. [Scikit-learn](https://pypi.org/project/scikit-learn/) (please use version 0.23.1 or below)
4. [pickleshare](https://pypi.org/project/pickleshare/)
5. [python-chess](https://pypi.org/project/chess/)

## Demo:
### Mid-game Explanation:

![In-Game screenshot](/Screenshots/HelperDemo.jpeg)

Capital letters are white pieces, rest are black pieces 

**(P = pawn, Q = queen, R = rook, K = king, N = knight, B = bishop)**

Green squares notifies the player where the piece can move,the blue square is the place "suggested"  by the algorithm.

### Menu:
Program starts by asking the player which difficulty to play at:
![Difficult](/Screenshots/InitialMenu.jpeg)

Then asks which colour to play as:
![Difficult](/Screenshots/TurnChoice.jpeg)

## Executable version coming soon! :)
