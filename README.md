# Rock Paper Scissors

A lightweight Python desktop game with an English interface, a computer opponent,
score tracking, a reset button, and keyboard shortcuts. No pip dependencies.

## Run

From this directory:

```sh
python3 game.py
```

Python needs Tkinter and a graphical desktop. If Tkinter is missing:

- Fedora: `sudo dnf install python3-tkinter`
- Ubuntu/Debian: `sudo apt install python3-tk`
- Windows: enable Tcl/Tk in the Python installer.

Click a choice or press R, P, or S. Every move plays a new round.
Reset score clears all three counters.

## Practice ideas

- Add a first-to-five game mode.
- Save scores to a JSON file.
- Change the colors and layout in `main()`.
- Add a round history.

`get_result()` contains the game rules and can be tested without opening a window.
