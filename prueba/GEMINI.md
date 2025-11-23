# Gemini Project Analysis: Mario Bros. Factory Game

## Project Overview

This project is a clone of the "Game & Watch: Mario Bros." handheld game, developed as the final project for a programming course. The game is built using Python and the `pyxel` retro game engine.

The objective of the game is to control Mario and Luigi to move packages through a bottling factory. Packages move along a series of conveyor belts. The players must move the characters to the correct floors to catch the packages and transfer them to the next belt or to the delivery truck. The game ends after three packages are dropped.

The project is structured following Object-Oriented Programming (OOP) principles, with each game entity (Character, Package, Conveyor, Truck, Boss) encapsulated in its own class and file. The main game logic is orchestrated by a `Board` class, keeping the main application file clean.

**Key Technologies:**
*   **Language:** Python
*   **Framework:** `pyxel`

**Architecture:**
*   **Object-Oriented:** Each game element is a class (`character.py`, `package.py`, etc.).
*   **Model-View-Controller (MVC) like pattern:**
    *   The classes in `character.py`, `package.py`, etc., act as the **Model**.
    *   The `draw()` methods in each class act as the **View**.
    *   The `Board` class and the `update()` methods act as the **Controller**.
*   **Configuration:** Game constants, including layout and sprite definitions, are stored in `constants.py`.
*   **Main Entry Point:** `main.py` initializes the game and runs the main loop.

## Building and Running

### Dependencies
The project requires the `pyxel` library. You can install it using pip:
```bash
pip install pyxel
```

### Running the Game
To run the game, execute the `main.py` file from within the `prueba` directory:
```bash
cd prueba
python3 main.py
```
Alternatively, from the project root:
```bash
python3 prueba/main.py
```

### Testing
There are no automated tests in this project. Testing is done manually by running the game.

## Development Conventions

*   **Object-Oriented Design:** All game logic is encapsulated within classes. The main program file (`main.py`) should not contain any game logic.
*   **One Class Per File:** Each class is stored in its own Python file (e.g., `Character` class is in `character.py`).
*   **Naming:**
    *   Class names use `UpperCamelCase`.
    *   File names, methods, and variables use `snake_case`.
*   **Attribute Protection:** Class attributes are intended to be "private" and should be accessed via `@property` decorators. Setters (`@attribute.setter`) are used to validate new values.
*   **Constants:** All magic numbers and configuration values are stored in `constants.py`.
*   **Sprites:** The game uses a `pyxel` resource file (`.pyxres`) for sprites. The definitions in `constants.py` map to the coordinates within this resource file. The project is set up to load `my_resource.pyxres`.
