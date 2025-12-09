
# Final Project: Mario Bros

**Group Members:** [Your Name(s)]
**Subject:** [Your Subject/Course Name]
**Date:** December 9, 2025

---

## Index & Abstract

This document is the report for our final project, a clone of the "Game & Watch: Mario Bros." game we built with Python and Pyxel. It goes over how we designed the classes using OOP ideas from class, the main logic that makes the game work, what we got done, a quick user manual, and our thoughts on the whole process. Our game has the main features of the original, where you control Mario and Luigi to move packages from conveyors to a truck, trying not to mess up as it gets harder.

---

## 1. Our Project Design: The Classes

When we started, we really tried to follow what we learned in class about Object-Oriented Programming. So, we broke the whole project down into different classes. It just made sense to have a class for Mario, one for the packages, one for the conveyors, and so on. It kept things from getting messy.

The big principle we focused on was **encapsulation**. The professor mentioned how important it is to protect the data inside a class, so we took that seriously. We didn't want code from outside a class to be able to just change an object's attributes directly. So, we used `@property` and `@attribute.setter` for pretty much everything. This was great because it let us run checks. For example, the `Character` class setter makes sure the `floor` is always a number, which prevented some weird bugs.

We also used **inheritance** a lot, just like we saw in the lectures.
*   We made a basic `GameObject` class that just had an `x` and `y` position. Almost every other class inherits from this. It was nice not having to write that code over and over.
*   The `Character` class inherits from `GameObject`, and then `Mario` and `Luigi` inherit from `Character`. This worked really well. `Character` has all the shared stuff like moving and handling states, and then the `Mario` and `Luigi` classes just have the details specific to them, like their controls and sprites.

**Composition** was the other big idea we used. The main `Game` class is basically the best example—it holds all the other objects and makes them work together. The `PackageManager` is another good one; it holds a list of all the `Package` objects and tells them what to do.

---

## 2. The Main Logic

Getting the game to actually *work* involved a few key parts.

### Character Movement
Getting Mario and Luigi to move right was interesting. We didn't want them to move pixel by pixel. That would be messy. Instead, they just jump between the different floors. When you press a key (Arrows for Mario, W/S for Luigi), it just changes a `floor` variable inside the character object. Then, a different method (`update_y_pos`) figures out the exact Y-coordinate for that floor, and that’s where the character gets drawn.

### Package Handling on Conveyors
The packages kind of move themselves, which is cool. The `PackageManager` creates a new package and puts it on the first conveyor. From there, the package's own `update` method just scoots it along based on the speed of whatever conveyor it's on. When it gets to the end, it basically sends up a flag to the `PackageManager` to say, "I'm done, what's next?"

### Collision Detection
For "collisions"—which for us just meant catching a package—we didn't do any complicated math to see if sprites were touching. That seemed like overkill. We just checked if the character was on the right floor and in the right state when the package got to the end of the conveyor. It was way simpler and worked perfectly for this kind of game. We made a method called `can_receive_package` for this. If the check is good, the package moves to the next level and you get points. If not, the package falls, and you get a failure.

---

## 3. Work Carried Out

We managed to get a complete and playable game done. We're pretty happy with it. It has all the main things you'd expect:

*   **A Main Menu:** You can pick the difficulty (`EASY`, `MEDIUM`, `EXTREME`, `CRAZY`).
*   **The Main Game:** You can move the characters, catch packages, and load up the truck.
*   **Scoring:** You get points for doing things right.
*   **Failures:** You can only mess up a few times before the game is over.
*   **Difficulty Changes:** The game gets harder not just based on the menu, but also as your score goes up.
*   **Animations:** We put in little "cutscenes" for when the truck is full or when the boss comes out. The game pauses so you can watch.
*   **Game Over Screen:** It shows your final score and lets you go back to the menu.

**Extra Features:**
We got a little creative and added a "CRAZY" difficulty. It flips the controls and makes the conveyor speeds random just to make things harder.

**Unimplemented Parts:**
The game loop is solid, so we didn't leave anything half-finished. But if we had more time, it would be cool to add different factory layouts or maybe make the boss do more than just yell at you. A high-score table would have been a nice touch too.

---

## 4. User Manual

The goal is to move packages from the factory's conveyor belts to the delivery truck.

### Controls:

*   **Luigi (Left Side):**
    *   **W Key:** Move Up
    *   **S Key:** Move Down
*   **Mario (Right Side):**
    *   **Up Arrow Key:** Move Up
    *   **Down Arrow Key:** Move Down
*   **Menu Navigation:** Use arrow keys to select difficulty and `ENTER` to confirm.
*   **Game Over:** Press `SPACE` to return to the main menu.

---

## 5. Our Conclusions

### Summary
Overall, we think the project was a success. We made a fun game that actually works, and we got to use all the OOP stuff we talked about in class. Breaking the problem down into classes made a huge difference and kept the project from becoming a total mess.

### Main Problems We Ran Into
We definitely ran into some problems.

1.  **The `platform.py` Mistake:** One of the first ones was pretty classic, actually. We named a file `platform.py` because it had our platform code in it. But when we ran the game, it crashed with a weird import error. It turned out Python has its *own* standard library with that exact name, and it was getting confused. Total rookie mistake. We renamed our file to **`game_platform.py`** and it fixed it right away. A good lesson to learn.

2.  **Stopping the Players During Animations:** Another thing that was tricky was the game states. When the truck was driving off, you could still move Mario and Luigi around, and it just looked weird and buggy. We fixed this by building a state machine for the whole game in the `Game` class. We set up states like `PLAYING` and `TRUCK_SEQUENCE`. Then the main update loop would only run the logic for whatever state the game was in. So if the state was `TRUCK_SEQUENCE`, it just wouldn't check for player input. It was a simple idea but it made the whole game feel much more solid.

### Personal Comments
This project was a great way to actually use the OOP ideas from the lectures. It's one thing to hear about encapsulation, but it's another to see how it helps keep your code clean when things get complicated. Making the `PackageManager` to handle all the package logic was probably one of our best decisions. It took a lot of messy code out of the other classes and put it all in one place.

If we were to do more, we'd probably pull all the sprite and level info out of the `constants.py` file and put it into something like a JSON file. Then you could change the game or add levels without even touching the Python code.
