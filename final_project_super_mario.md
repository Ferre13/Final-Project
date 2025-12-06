# Final Project: Mario Bros (Game & Watch)
**Course:** Programming 2025 - 2026 (uc3m) 

## 1. Introduction
This document describes the final project for the Programming course, focused on the development of a Mario Bros game. Students will apply the programming concepts and techniques learned throughout the course to create a fully functional and engaging game.

## 2. Project Objectives
The main objectives of this project are:
* Design and implement a classic Mario Bros game using Python with `pyxel`.
* Demonstrate mastery of fundamental programming concepts such as loops, conditional statements, data structures, and object-oriented programming.
* Gain experience in game development concepts such as character movement or collision detection.
* Develop problem-solving and critical thinking skills in a creative and engaging context.

## 3. Game Description
A digital version of the famous game 'Game & Watch: Mario Bros. (1983)' must be developed. In this version, Mario and Luigi work in a bottling factory, and their mission is to ensure that packages arrive correctly at the delivery truck without falling to the ground.

*Reference:* You can play this game online at [https://itizso.itch.io/nintendo-mario-bros](https://itizso.itch.io/nintendo-mario-bros).

### Setting and Characters
The game must be played on a single screen where the following elements and characters will be available:

*   **Mario:** Located on the right side of the screen. Responsible for picking up empty boxes (Conveyor) and placing them on the first conveyor belt (Conveyor1). He also manages movements between **EVEN → ODD** conveyor belts.
*   **Luigi:** Located on the left side of the screen. Responsible for placing finished packages in the truck. He also manages movements between **ODD → EVEN** conveyor belts.
*   **The Boss:** Mario and Luigi's boss. Appears to punish them when a package falls (adding a 'failure') and appears after breaks to make them return to work.

**Conveyor System:**
*   **Conveyor:** The first belt. Carries empty boxes to Mario.
*   **Even Conveyor Belts:** Mario receives packages here and moves them to an Odd Conveyor Belt (higher level).
*   **Odd Conveyor Belts:** Luigi receives packages here and moves them to an Even Conveyor Belt (higher level).
*   **Truck:** Waits for Luigi to deliver 8 packages. Once full, it leaves for delivery. During delivery, characters rest, belts stop, and packages freeze. (Packages at the very end of a belt disappear when the truck leaves).
*   **Floors and Stairs:** Characters start at Floor0. They move up/down using painted stairs.

### Game Mechanics
*   **Controls:**
    *   **Mario:** Arrow UP / Arrow DOWN.
    *   **Luigi:** W (Up) / S (Down).
*   **Automatic Movement:** If a character is on the correct floor, they automatically move the package:
    *   *Floor0:* Mario moves package from Conveyor to Conveyor1.
    *   *Intermediate Floors:* Mario moves Even → Even+1; Luigi moves Odd → Odd+1.
    *   *Floor N:* Luigi moves ConveyorX (Odd) → Truck.
*   **Scoring & Failures:**
    *   **Game Over:** After 3 errors (lost packages). A package is lost if the character is not on the correct floor to receive it.
    *   **Points:** +1 point for every correct movement between belts. +10 points for every completed truck (8 packages).
    *   **Packages:** There must always be at least one package in play.

### Difficulty Levels
The game has varied difficulty levels affecting controls, speed, and rules.

| Feature | Easy | Medium | Extreme | Crazy |
| :--- | :--- | :--- | :--- | :--- |
| **Mario Controls** | Up: Up<br>Down: Down | Up: Up<br>Down: Down | Up: Up<br>Down: Down | **Up: Down<br>Down: Up** |
| **Luigi Controls** | W: Up<br>S: Down | W: Up<br>S: Down | W: Up<br>S: Down | **W: Down<br>S: Up** |
| **Belts** | 5 | 7 | 9 | 5 |
| **Conveyor Speed** | Always 1x | Conv0/Even: 1x<br>Odd: 1.5x | Conv0: 1x<br>Even: 1.5x<br>Odd: 2x | **Random (1-2) per conveyor** |
| **Packages / Truck** | Starts at 1. Increases every 50 pts.<br>Eliminates 1 failure every 3 deliveries. | Starts at 1. Increases every 30 pts.<br>Eliminates 1 failure every 5 deliveries. | Starts at 1. Increases every 30 pts.<br>Eliminates 1 failure every 5 deliveries. | Starts at 1. Increases every 20 pts.<br>**Does NOT eliminate failures.** |

## 4. Project Requirements
*   **Functionality:** Fully functional game (controls, package movement, truck logic).
*   **Code Quality:** Well-written, organized, commented, using **Object-Oriented Programming (OOP)**.
*   **User Interface:** Clear interface showing the factory and characters.
*   **Game Design:** Attractive and challenging. *Note:* Graphics can be created by the class (shared repository) or custom. Grading focuses on OOP implementation, not art. (Bonus 0.1 pts for the first 3 groups to upload graphics) .
*   **Audio:** Sound effects allowed (moving box, stairs, truck, punishment, etc.).

## 5. Project Deliverables
1.  **Source Code:** Complete and well-commented.
2.  **Executable Game:** Playable version.
3.  **Documentation (PDF, max 10 pages):** 
    *   Cover, index, summary.
    *   Class design description (attributes/methods).
    *   Algorithm description.
    *   Work log (functionalities included/excluded).
    *   User manual.
    *   Conclusions (problems, improvements).

### Recommended Sprints
*   **Sprint 1:** Objects & GUI. Class creation (Characters, Conveyor, Truck). Visual representation (no movement yet).
*   **Sprint 2:** Mario & Luigi Movement. Vertical control, stairs logic, graphical position updates.
*   **Sprint 3:** Package Movement. Flow logic, spawn rates, automatic pickup if character is present, falling logic if absent.
*   **Sprint 4:** Scoring, Failures, Game End. +1/+10 points, 3 failure limit, Truck delivery/rest logic, Boss effects.
*   **Sprint 5 (Optional):** Difficulty Levels & Polish. Implement the difficulty table, sound effects, high scores.

## 6. Resources
Students have access to course materials, online tutorials, language documentation, and instructor support.

## 7. Evaluation
**Total Score: 0 - 2.5 points** 
*   Sprint 1-4: 0.5 points each (2.0 total).
*   Report: 0.5 points.
*   Optional/Extra: +0.1 per functionality (max score cap is 2.5).

**Penalties:**
*   -0.25 pts: Insufficient comments.
*   -0.50 pts: Bad practices (no methods, repetitive code, no OOP, global variables).
*   -0.25 pts: Bad encapsulation (unnecessary public attributes, code outside classes).
*   -0.25 pts: Long methods (should fit on one screen).
*   **Plagiarism:** Automatic exclusion from continuous evaluation.

## 8. Submission Rules
*   **Group Size:** 2 students.
*   **Format:** Zip file named `initials1-initials2.zip` (e.g., `lpg-jgj.zip`).
*   **Deadline:** Upload to Aula Global.