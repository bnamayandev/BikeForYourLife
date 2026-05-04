# Bike for Your Life

Bike for Your Life is a terminal typing game about surviving a monster chase on a bicycle. Each level gives you a passage to type while a monster slowly closes in on your bike. Correct characters move you toward the finish line, mistakes cost time, and the game tracks your words per minute as you escape through the story.

The project started as a high-school Python game and has been reorganized into a small package so the game loop, terminal helpers, passages, state, and stats are easier to read and maintain.

## Project structure

```text
.
├── main.py
├── requirements.txt
├── README.md
└── bike_for_your_life/
    ├── __init__.py
    ├── cli.py
    ├── game.py
    ├── passages.py
    ├── state.py
    ├── stats.py
    └── terminal.py
```

`main.py` is now only the entry point. The rest of the code lives in `bike_for_your_life/`:

- `cli.py` handles the title screen, story flow, and replay prompts.
- `game.py` runs each typing level and moves the monster.
- `terminal.py` contains terminal clearing, color, and single-key input helpers.
- `state.py` stores shared game state.
- `stats.py` calculates typing stats.
- `passages.py` stores the level passages.

## Running locally

Use a normal terminal window. The game reads one keypress at a time, so run it in an interactive terminal rather than inside an editor output pane.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

On Windows, activate the virtual environment with:

```bash
.venv\Scripts\activate
```
