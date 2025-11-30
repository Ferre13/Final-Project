# Final Project: Mario Bros.

**Author:** [Your Name(s) Here]
**Course:** Programming 2025 - 2026

---

## Index

1.  [Brief Summary](#1-brief-summary)
2.  [Game Design and Implementation](#2-game-design-and-implementation)
    1.  [Game Description](#21-game-description)
    2.  [Core Objective](#22-core-objective)
    3.  [Implementation Strategy](#23-implementation-strategy)
3.  [Description of Designed Classes](#3-description-of-designed-classes)
4.  [Main Algorithms Used](#4-main-algorithms-used)
    1.  [The Main Game Loop: A State Machine](#41-the-main-game-loop-a-state-machine)
    2.  [Package Transfer and Failure Logic](#42-package-transfer-and-failure-logic)
5.  [Work Carried Out](#5-work-carried-out)
    1.  [Implemented Functionality](#51-implemented-functionality)
    2.  [Unimplemented Functionality](#52-unimplemented-functionality)
6.  [User Manual](#6-user-manual)
7.  [Conclusions](#7-conclusions)
    1.  [Final Summary](#71-final-summary)
    2.  [Main Problems Encountered](#72-main-problems-encountered)
    3.  [Future Improvements](#73-future-improvements)

---

## 1. Brief Summary

This document provides a comprehensive overview of the implementation of the "Mario Bros." final project. The game is a recreation of the classic Game & Watch title, developed in Python using the Pyxel game engine. This report details the object-oriented design, the main algorithms used, the functionalities implemented, a user manual, and a reflection on the development process, as required by the project specifications. The primary architectural goal was to create a well-organized, modular, and easily maintainable codebase that adheres to the principles of Object-Oriented Programming.

## 2. Game Design and Implementation

### 2.1. Game Description

The game is set in a bottling factory where brothers Mario and Luigi must work together to move packages from the top of the screen to a delivery truck at the bottom. The game is played on a single screen containing multiple levels of conveyor belts.

### 2.2. Core Objective

The player's goal is to achieve the highest possible score by successfully moving packages down the factory line. The game ends when the player accumulates 3 failures by dropping packages.

### 2.3. Implementation Strategy

The game is built using an object-oriented architecture. The core principle is that every "entity" in the game world is represented by its own class, responsible for its own state and behavior. This avoids monolithic "spaghetti code" and promotes modularity.

-   **Game Entry Point (`main.py`):** A minimal script responsible only for initializing the game.
-   **Object Creation (`factory.py`):** A dedicated `Factory` class is responsible for creating and configuring all game objects at the start.
-   **Game Orchestration (`board.py`):** The `Board` class acts as the central controller. It manages the main game loop and game state but delegates specific logic to other objects.
-   **Logic Management:** Specialist "manager" classes like `PackageManager` are used to handle complex systems (like package flow), keeping the `Board` class clean and focused on high-level state control.
-   **Configuration (`constants.py`):** All "magic numbers" (speeds, positions, scores, etc.) are defined in a single constants file, making the game easy to configure and tweak.

## 3. Description of Designed Classes

The project is broken down into the following classes, each with a single responsibility:

-   **`main.Game`**: The main class that initializes Pyxel and orchestrates the creation of the game world via the `Factory`.

-   **`board.Board`**: The most important class. It acts as the main controller for the game.
    -   **Attributes**: `state` (manages the current game state), `score`, `failures`, and references to all game objects.
    -   **Methods**: `update()` and `draw()` (the main game loop methods), `reset_game()`, and several private `__update...()` and `__draw...()` methods to handle logic for different game states (e.g., `__update_playing()`, `__update_game_over()`).

-   **`factory.Factory`**: Responsible for creating all game objects.
    -   **Methods**: `create_world()`, `create_characters()`, `create_background()`. It reads configuration from `constants.py` and returns a dictionary of fully constructed game objects.

-   **`package_manager.PackageManager`**: Manages the entire lifecycle of packages.
    -   **Attributes**: A reference to the `board` to modify game state like score and failures.
    -   **Methods**: `update()` (the main entry point called by the board), `__spawn_package()`, `__update_packages()`, `__handle_failure()`, `__handle_package_transfer()`.

-   **`game_info.GameInfo`**: Manages the Heads-Up Display (HUD).
    -   **Methods**: `draw_score(score)`, `draw_lives(failures)`.

-   **`characters.Character`**: Represents Mario or Luigi.
    -   **Attributes**: `name`, `x`, `y`, `floor`, `state`.
    -   **Methods**: `update()` (handles player input), `draw()`, `move_up()`, `move_down()`, `can_receive_package(floor)`.

-   **`package.Package`**: Represents a single package.
    -   **Attributes**: `x`, `y`, `state` ('moving' or 'falling'), `current_conveyor`.
    -   **Methods**: `update()` (moves the package and returns a status code), `draw()`, `fall()`, `advance_to_conveyor()`.

-   **`truck.Truck`**: A self-contained state machine for the delivery truck sequence.
    -   **Attributes**: `x`, `y`, `packages_count`, `is_delivering`.
    -   **Methods**: `update()` (manages its animation phases), `draw()`, `receive_package()`.

-   **`boss.Boss`**: A self-contained state machine for the boss animation sequence.
    -   **Attributes**: `state`, `target` (which player to yell at).
    -   **Methods**: `update()` (manages its animation phases), `draw()`, `appear(reason)`.

-   **Other Classes**: `Conveyor`, `Platform`, `Door`, and various classes in `background.py` are simple objects that primarily manage their own position and drawing logic.

## 4. Main Algorithms Used

### 4.1. The Main Game Loop: A State Machine

The most important algorithm is the state machine pattern implemented in the `Board` class. This was a key refactoring to eliminate "spaghetti code".

-   The `Board` has a `self.state` attribute which can hold values like `constants.PLAYING`, `constants.GAME_OVER`, etc.
-   The main `board.update()` method does not contain game logic itself. Instead, it acts as a dispatcher, checking the value of `self.state` and calling a specific private method for that state (e.g., `__update_playing()`).
-   State transitions are handled by other objects or logic. For example, when `PackageManager` detects 3 failures, it sets `self.board.state = constants.GAME_OVER`. When the truck becomes full, `PackageManager` sets `self.board.state = constants.TRUCK_SEQUENCE`. This keeps the flow of control clean and easy to follow.

### 4.2. Package Transfer and Failure Logic

This logic resides within the `PackageManager`.
1.  In its main `update` loop, it calls `package.update()` for every package.
2.  `package.update()` returns a status code (e.g., `PKG_STATUS_REACHED_END`).
3.  The `PackageManager` checks this code. If it's `PKG_STATUS_REACHED_END`, it calls its private `__handle_package_transfer()` method.
4.  This method checks the `floor` attribute of both `mario` and `luigi` and calls their `can_receive_package()` method to see if a transfer is possible.
5.  If the transfer is not possible, the `PackageManager` calls the package's `fall()` method, which changes the package's internal state to 'falling'.

## 5. Work Carried Out

### 5.1. Implemented Functionality

-   **Object-Oriented Design:** The entire project is built on OOP principles, with 15 classes separated into 11 files, each with a clear responsibility.
-   **Game States:** The game correctly transitions between all major states: Playing, Truck Delivery Sequence, Boss Appearance, and Game Over.
-   **Player Control:** Mario and Luigi can be controlled independently to move between floors.
-   **Package Flow:** Packages spawn correctly, move along conveyors, change appearance, and can be transferred between conveyors by the players.
-   **Scoring and Failures:** The score is incremented for successful transfers and truck deliveries. Failures are tracked, and the game ends at 3 failures.
-   **Truck & Boss Sequences:** The truck and boss have fully implemented, self-contained animation sequences that interrupt gameplay as required.
-   **Difficulty Settings:** The logic for different difficulty levels (affecting speed, spawning, etc.) is implemented, although the game is hard-coded to "EASY" in `main.py`.

### 5.2. Unimplemented Functionality

As per the optional Sprints in the project PDF, the following features have not been implemented:
-   A main menu to select difficulty before starting the game.
-   Sound effects and music.
-   A high-score table.

## 6. User Manual

-   **Objective:** Score as many points as possible by helping Mario and Luigi move packages from the top of the factory to the delivery truck at the bottom. The game ends after 3 dropped packages.
-   **Controls:**
    -   **Mario (Right Side):** Use `ARROW UP` and `ARROW DOWN` to move between floors.
    -   **Luigi (Left Side):** Use `W` and `S` to move between floors.
-   **Gameplay:**
    -   Position Mario or Luigi on the same floor as a package when it reaches the end of a conveyor belt to transfer it.
    -   Mario handles the even-numbered floors (starting at the ground floor, 0).
    -   Luigi handles the odd-numbered floors.
    -   Fill the truck with 8 packages to get bonus points.
-   **To Quit:** Press the `Q` key at any time.
-   **To Restart:** After a "Game Over," press `SPACE` or `ENTER`.

## 7. Conclusions

### 7.1. Final Summary

The project successfully implements the core requirements of the "Mario Bros." game using a robust, object-oriented design in Python with Pyxel. The final architecture is highly modular, separating concerns into distinct classes for game logic, object creation, and state management. This resulted in a clean, maintainable, and extensible codebase.

### 7.2. Main Problems Encountered

The primary challenge during development was managing the complexity of the main game logic. The initial design tended towards a single, large `Board` class that handled everything, resulting in "spaghetti code" that was difficult to debug and extend.

This problem was solved by a significant refactoring effort:
1.  **Introducing a State Machine:** Replacing multiple boolean flags with a single `state` variable in the `Board` made the game flow much clearer.
2.  **Delegating Responsibilities:** Creating `Factory` and `PackageManager` classes to handle object creation and package logic, respectively, drastically simplified the `Board` class and enforced the Single Responsibility Principle.

### 7.3. Future Improvements

The project provides a solid foundation for several future improvements:
-   Implement the optional features from the PDF, such as a main menu, sound effects, and a high-score system.
-   Add more visual feedback, such as particle effects when a package is successfully transferred or dropped.
-   Expand the difficulty levels with more unique rules or enemy patterns.
-   Create a more comprehensive test suite to verify the logic of each class independently.
