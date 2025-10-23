# Line-following robot simulator

A small PyQt6-based simulator that draws a warehouse and runs a line-following robot program. The robot reads three line sensors (left, front, right), executes a sequence of commands, and reports its direction and coordinates to a secondary status window.

## Features
- Render a warehouse from a text file.
- Configurable robot size, start position, direction, time step and program via text file.
- Pixel-based sensors sample the rendered warehouse to detect lines.
- Secondary window displays robot direction, coordinates and program; allows pause/resume.

## Requirements
- Python 3.10+ (or 3.8+)
- PyQt6

Install dependency:
```bash
pip install PyQt6
```

## Quick start
From the project root run:
```bash
python src/main.py
```
(Ensure you run this command in the project root where the `resources/` and `src/` folders are located.)

## Project layout
- resources/
  - Magatzem.txt        — warehouse line definitions (see format below)
  - Robot.txt           — robot configuration and program (see format below)
  - secondary_win.ui    — Qt Designer file for the secondary window
- src/
  - main.py             — entry point: reads resources and starts the app
  - main_win.py         — FinPpal: main window that draws the warehouse and runs the timer
  - robot.py            — Robot: widget that implements robot state, movement and logic
  - secondary_win.py    — SecondaryWin: UI showing robot status and controls
  - line_sensor.py      — Sensor: samples a single pixel from the main window

## File formats

### resources/Magatzem.txt
- Line 1: `<width> <height>` — canvas/window size in pixels (e.g. `500 500`).
- Following lines: one `x1 y1 x2 y2` per line describing segments to draw (integers).

Example:
```
500 500
100 280 400 280
...
```

### resources/Robot.txt
- Line 1: robot size (integer)
- Line 2: initial position `x y` (center coordinates)
- Line 3: initial direction (`N`, `E`, `S`, `O` or lowercase)
- Line 4: time step in milliseconds (timer interval)
- Line 5: program — sequence of single-character commands separated by spaces (e.g. `e d t r p`)

Common commands:
- `E`/`e` = left turn (−90°)
- `D`/`d` = right turn (+90°)
- `T`/`t` = 180° turn
- `R`/`r` = (application-specific rule/straight logic)
- `P`/`p` = stop/finish when sensors detect no line

## How it works (brief)
- main.py reads both text files and creates the main window.
- main_win draws the lines and instantiates a Robot and a SecondaryWin.
- Robot places three pixel sensors around its center and samples the rendered main window to know if each sensor is over a black line (`1`) or background (`0`).
- A QTimer periodically calls Robot.robot_move to evaluate the sensors and execute the next command in the program when a junction is detected.
- Robot emits status strings (`"<DIR> <X> <Y>"` or `Kill`) to update the secondary window and to stop on completion.

## Troubleshooting
- Robot not visible:
  - Check that `resources/Magatzem.txt` window size matches what the main window expects.
  - Ensure robot start coordinates are inside the canvas bounds.
  - Run `python src/main.py` from the project root (so relative paths to `resources` work).
- UI not loading:
  - Confirm `secondary_win.ui` is in `resources` and `secondary_win.py` uses the resources path.
