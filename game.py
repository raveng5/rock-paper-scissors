"""A small Tkinter game. Run with: python3 game.py"""

import random

CHOICES = ("Rock", "Paper", "Scissors")
BEATS = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}


def get_result(player, computer):
    """Return win, lose, or draw for two valid choices."""
    if player not in CHOICES or computer not in CHOICES:
        raise ValueError("Choices must be Rock, Paper, or Scissors")
    if player == computer:
        return "draw"
    return "win" if BEATS[player] == computer else "lose"


def main():
    try:
        import tkinter as tk
    except ImportError:
        raise SystemExit(
            "Tkinter is missing. On Fedora: sudo dnf install python3-tkinter\n"
            "On Ubuntu/Debian: sudo apt install python3-tk"
        ) from None

    bg, panel, muted = "#111827", "#1f2937", "#9ca3af"
    root = tk.Tk()
    root.title("Rock Paper Scissors")
    root.geometry("680x680")
    root.minsize(560, 660)
    root.configure(bg=bg)
    scores = {"win": 0, "draw": 0, "lose": 0}

    def label(parent, text, size=12, color="#f9fafb", background=bg):
        return tk.Label(parent, text=text, font=("Helvetica", size),
                        fg=color, bg=background)

    label(root, "THE CLASSIC HAND GAME", 10, "#a78bfa").pack(pady=(26, 8))
    label(root, "Rock. Paper. Scissors.", 28).pack()
    label(root, "Make your move. Can you beat the computer?", 12, muted).pack(pady=10)

    scoreboard = tk.Frame(root, bg=panel, padx=20, pady=14)
    scoreboard.pack(fill="x", padx=30, pady=14)
    counters = {}
    for column, (key, title) in enumerate(
            (("win", "YOU"), ("draw", "DRAWS"), ("lose", "COMPUTER"))):
        scoreboard.columnconfigure(column, weight=1)
        label(scoreboard, title, 10, muted, panel).grid(row=0, column=column)
        counters[key] = label(scoreboard, "0", 26, background=panel)
        counters[key].grid(row=1, column=column, pady=(6, 0))

    arena = tk.Frame(root, bg=bg)
    arena.pack(fill="x", padx=30, pady=18)
    arena.columnconfigure(0, weight=1)
    arena.columnconfigure(2, weight=1)
    player_label = label(arena, "Your move\n?", 22, "#c4b5fd")
    player_label.grid(row=0, column=0, sticky="ew")
    label(arena, "VS", 12, muted).grid(row=0, column=1, padx=15)
    computer_label = label(arena, "Computer\n?", 22, "#93c5fd")
    computer_label.grid(row=0, column=2, sticky="ew")

    result_label = label(root, "Ready when you are", 20)
    result_label.pack(pady=(4, 5))
    detail_label = label(root, "Choose one of the three buttons below.", 11, muted)
    detail_label.pack()

    def play(choice):
        computer = random.choice(CHOICES)
        result = get_result(choice, computer)
        scores[result] += 1
        player_label.config(text=f"Your move\n{choice}")
        computer_label.config(text=f"Computer\n{computer}")
        messages = {"win": ("You win!", "#34d399"),
                    "lose": ("Computer wins!", "#fca5a5"),
                    "draw": ("It's a draw!", "#fcd34d")}
        message, color = messages[result]
        result_label.config(text=message, fg=color)
        winner, loser = (choice, computer) if result == "win" else (computer, choice)
        detail_label.config(text="Same move. Try again!" if result == "draw"
                            else f"{winner} beats {loser.lower()}.")
        for key, counter in counters.items():
            counter.config(text=str(scores[key]))

    controls = tk.Frame(root, bg=bg)
    controls.pack(fill="x", padx=30, pady=24)
    for column, choice in enumerate(CHOICES):
        controls.columnconfigure(column, weight=1, uniform="choice")
        tk.Button(controls, text=choice, command=lambda c=choice: play(c),
                  font=("Helvetica", 15, "bold"), bg="#7c3aed", fg="white",
                  activebackground="#6d28d9", activeforeground="white",
                  relief="flat", cursor="hand2", pady=16,
                  highlightthickness=2, highlightbackground=bg,
                  highlightcolor="#ddd6fe").grid(row=0, column=column, sticky="ew", padx=5)

    def reset():
        for key in scores:
            scores[key] = 0
            counters[key].config(text="0")
        player_label.config(text="Your move\n?")
        computer_label.config(text="Computer\n?")
        result_label.config(text="Ready when you are", fg="#f9fafb")
        detail_label.config(text="Choose one of the three buttons below.")

    tk.Button(root, text="Reset score", command=reset, font=("Helvetica", 11),
              bg=panel, fg="#e5e7eb", activebackground="#374151",
              activeforeground="white", relief="flat", padx=18, pady=8).pack()
    label(root, "Keyboard: R = Rock · P = Paper · S = Scissors", 10, muted).pack(pady=14)
    for key, choice in zip("rps", CHOICES):
        root.bind(key, lambda event, c=choice: play(c))
        root.bind(key.upper(), lambda event, c=choice: play(c))
    root.mainloop()


if __name__ == "__main__":
    main()
