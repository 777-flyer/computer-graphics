# CSE423 — Computer Graphics

## BRAC University | Spring 2026

This repository contains three programming assignments completed for CSE423 Computer Graphics. All implementations use Python with PyOpenGL (OpenGL + GLUT).

---

## Assignment 1 — OpenGL Primitives and Interactivity

**Directory:** `assignment_1/`

Two independent tasks demonstrating core OpenGL 2D rendering with keyboard and mouse interaction.

### Task 1 — Animated Rainy Scene (`TASK_1.py`)

A 2D scene rendered using `GL_TRIANGLES`, `GL_LINES`, and `GL_POINTS` primitives, depicting a house with flanking trees, a grass strip, and animated falling rain against a sky that transitions between night and day.

**Implemented Features:**

- Scene composition: sky, ground plane, grass band, triangular trees, and a structured house with roof, door, windows, and dividers — all built exclusively from triangle and line primitives
- Animated rain simulation using per-frame position updates with wrap-around boundary handling
- Continuous day/night brightness interpolation via a scalar `brightness` factor applied uniformly across all scene colours
- Rain direction controlled at runtime via horizontal drift adjustment

**Controls:**

| Input | Action |
| --- | --- |
| `Left Arrow` | Tilt rain leftward |
| `Right Arrow` | Tilt rain rightward |
| `d` | Gradually increase brightness (towards day) |
| `n` | Gradually decrease brightness (towards night) |

---

### Task 2 — Bouncing Points Simulator (`TASK_2.py`)

An interactive simulation of coloured points bouncing elastically inside a bounded rectangular region, with real-time speed, visibility, and freeze controls.

**Implemented Features:**

- Dynamic point spawning at the right-click cursor position, each assigned a random colour and random diagonal velocity
- Elastic boundary collision: velocity component sign is inverted upon contact with any wall
- Global speed scaling (multiplicative) via keyboard; minimum speed clamped to prevent stalling
- Frame-based blink toggling: visibility alternates every configurable number of idle frames
- Global freeze state suspending all physics and control input except unfreeze

**Controls:**

| Input | Action |
| --- | --- |
| `Right Click` | Spawn a coloured bouncing point at cursor |
| `Left Click` | Toggle blinking of all points |
| `Up Arrow` | Increase global speed (×1.5) |
| `Down Arrow` | Halve global speed |
| `Space` | Freeze / unfreeze all motion |

---

## Assignment 2 — Midpoint Line Algorithm and Game Development

**Directory:** `assignment_2/` | **File:** `a2.py`

A falling-object catch game titled *Catch the Diamonds*, in which all geometry is rendered using a custom software implementation of the **Midpoint Line Drawing Algorithm** — no OpenGL line primitives are used.

**Algorithm Implementation:**

The midpoint algorithm is generalised across all eight octants using zone detection and coordinate transformation. Endpoints are classified into one of eight zones based on the sign and relative magnitude of `dx` and `dy`. Coordinates are mapped to Zone 0 (gentle positive slope, left-to-right), the standard midpoint loop is executed, and each plotted pixel is inverse-transformed back to the original zone before rasterisation via `GL_POINTS`.

**Game Mechanics:**

- A diamond shape falls from a random horizontal position at the top of the viewport
- The player controls a trapezoidal catcher along the bottom of the screen using the arrow keys
- Successful catches increment the score and increase the fall speed by 8 px/s
- A missed diamond (falling below the screen) triggers game over; the catcher turns red
- On-screen UI buttons (drawn with the midpoint algorithm) provide restart, pause/play, and exit functionality

**Controls:**

| Input | Action |
| --- | --- |
| `Left / Right Arrow` | Move catcher |
| `Left Click` on buttons | Restart / Pause-Play / Exit |
| `c` | Toggle cheat mode (catcher auto-tracks diamond) |

---

## Assignment 3 — 3D Scene, Camera Systems, and Shooter Game

**Directory:** `assignment_3/` | **File:** `a3.py`

A real-time 3D top-down shooter titled *Bullet Frenzy*, implementing a fully three-dimensional scene with perspective projection, multiple camera modes, a humanoid player model, enemy AI, and projectile physics.

**Rendering and Scene:**

- Perspective projection via `gluPerspective`; scene rendered with depth testing enabled
- 1200×800 arena with a checkerboard floor (12×12 grid) and four distinctly coloured boundary walls
- Player model composed of GLU quadrics (cylinders, sphere) and a solid cube, rotated to face the current heading
- Five enemies rendered as pulsing sphere composites with a sinusoidal scale animation tied to elapsed time

**Camera System:**

- **Third-person overhead** (default): fixed `gluLookAt` from an elevated position centred on the arena origin
- **First-person**: eye positioned at the gun barrel with a look-at target projected along the player's heading vector
- **Cheat overhead follow**: bird's-eye camera that follows the player position when cheat mode is active
- Arrow keys orbit/elevate the overhead camera in third-person mode

**Gameplay:**

- Player navigates using WASD (forward/backward/turn or cardinal strafe in cheat mode)
- Left mouse button fires a bullet along the player's current heading; bullets are rendered as solid cubes
- Enemies spawn at least 180 units from the player and pursue using normalised vector steering
- Bullet–enemy collision is distance-based (radius 32 units); a hit respawns the enemy and increments the score
- **Lives:** an enemy reaching the player costs one life (5 total)
- **Missed shots:** 10 bullets leaving the arena boundary trigger game over
- Death animation: the player model tilts progressively to 90° on game over
- HUD displays lives remaining, score, and missed shot count via bitmap text overlay

**Controls:**

| Input | Action |
| --- | --- |
| `W / S` | Move forward / backward |
| `A / D` | Turn left / right |
| `Left Click` | Fire bullet |
| `Right Click` | Toggle first-person / third-person camera |
| `Arrow Keys` | Orbit / elevate overhead camera (third-person only) |
| `c` | Toggle cheat mode (auto-aim and fire; remaps WASD to cardinal movement) |
| `v` | Toggle gun-follow camera (first-person only) |
| `r` | Restart game |

---

## Dependencies

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

Python 3.x with a GLUT-compatible runtime (e.g., `freeglut`) is required.

## Running

```bash
# Assignment 1
python assignment_1/TASK_1.py
python assignment_1/TASK_2.py

# Assignment 2
python assignment_2/a2.py

# Assignment 3
python assignment_3/a3.py
```

---

## Academic Integrity

> ⚠️ This repository is shared publicly for learning and reference purposes. While you are welcome to study the implementations and understand the concepts, please do not copy code directly for your coursework or assignments.
>
> Academic integrity matters. Use this as a learning resource to build your own understanding, not as a shortcut. Your future self (and your professor) will thank you.

This repository represents coursework completed in **Spring 2026**. Problem statements are proprietary to BRAC University and are not included to respect copyright.

Happy Coding!
