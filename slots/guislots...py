import tkinter as tk
from tkinter import messagebox
import random

# Slot machine logic
def spin_slot_machine():
    symbols = ['9', '10', 'J', 'Q', 'K', 'A', '⭐', '☯️']
    weights = [30, 25, 20, 10, 5, 3, 2, 1]

    win_lines = [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
        [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
        [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
        [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],
        [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
        [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],
        [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],
    ]

    def spin():
        rows, cols = 3, 5
        slot_machine = [[random.choices(symbols, weights=weights)[0] for _ in range(cols)] for _ in range(rows)]
        return slot_machine

    def check_wins(slot_machine):
        total_win_multiplier = 0
        free_plays = 0
        
        for line in win_lines:
            matched_symbols = [slot_machine[row][col] for row, col in line]
            first_symbol = matched_symbols[0]
            
            match_count = 0
            for symbol in matched_symbols:
                if symbol == first_symbol:
                    match_count += 1
                else:
                    break
            
            if match_count >= 3:
                if match_count == 3:
                    total_win_multiplier += 1
                elif match_count == 4:
                    total_win_multiplier += 1.25
                elif match_count == 5:
                    total_win_multiplier += 1.9
        
        yin_yang_count = sum(row.count('☯️') for row in slot_machine)
        if yin_yang_count == 3:
            free_plays += 8
        elif yin_yang_count == 4:
            free_plays += 15
        elif yin_yang_count == 5:
            free_plays += 20

        return total_win_multiplier, free_plays

    return spin, check_wins

# GUI Setup
class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")
        
        self.spin_button = tk.Button(root, text="Spin", command=self.spin)
        self.spin_button.pack(pady=10)
        
        self.result_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.result_label.pack(pady=10)
        
        self.slot_machine = None
        self.check_wins = None
        self.total_win_multiplier = 0
        self.free_plays = 0
    
    def spin(self):
        spin_func, check_wins_func = spin_slot_machine()
        self.slot_machine = spin_func()
        self.total_win_multiplier, self.free_plays = check_wins_func(self.slot_machine)
        
        self.display_slot_machine()
        self.check_for_wins()
    
    def display_slot_machine(self):
        slot_machine_text = "\n".join(" | ".join(row) for row in self.slot_machine)
        self.result_label.config(text=f"Slot Machine:\n{slot_machine_text}")
    
    def check_for_wins(self):
        if self.total_win_multiplier > 0:
            message = f"Total win multiplier: {self.total_win_multiplier:.2f}"
        else:
            message = "Better luck next time!"
        self.result_label.config(text=self.result_label.cget("text") + f"\n{message}")

# Create the main window
root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
