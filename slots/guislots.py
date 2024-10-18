import tkinter as tk
from tkinter import messagebox
import random

class SlotMachineGame:
    def __init__(self, root):
        self.root = root
        if self.root:
            self.root.title("Slot Machine Game")
            self.root.resizable(False, False)

        # Initialize game variables
        self.balance = 100.0  # Starting balance
        self.progressive_jackpot = 500.0  # Starting jackpot
        self.total_spins = 0  # Total spins played (for loyalty rewards)
        self.bet_amount = tk.DoubleVar(value=1.0)
        self.bet_lines = []
        self.free_spins = 0

        # Define the symbols and their weights
        self.symbols = ['9 ', '10', 'J ', 'Q ', 'K ', 'A ', '⭐', ' ☯️', '💎']
        self.weights = [30, 25, 20, 10, 5, 3, 2, 1, 0.5]  # Updated weights, '💎' is rare

        # Define win lines
        self.win_lines = [
            # Horizontal lines
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # Line 1
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],  # Line 2
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],  # Line 3

            # Diagonal lines
            [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # Line 4
            [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # Line 5

            # Zig-Zag lines 
            [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],  # Line 6
            [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],  # Line 7
        ]

        # Colors corresponding to ROYGBIV for highlighting winning lines
        self.line_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

        # Set up the GUI elements
        if self.root:
            self.setup_gui()

    def setup_gui(self):
        # Frame for balance and jackpot
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.balance_label = tk.Label(top_frame, text=f"Balance: ${self.balance:.2f}", font=("Arial", 12))
        self.balance_label.pack(side=tk.LEFT, padx=20)

        self.jackpot_label = tk.Label(top_frame, text=f"Jackpot: ${self.progressive_jackpot:.2f}", font=("Arial", 12))
        self.jackpot_label.pack(side=tk.LEFT, padx=20)

        # Frame for betting options
        bet_frame = tk.Frame(self.root)
        bet_frame.pack(pady=10)

        tk.Label(bet_frame, text="Bet Amount per Line: $", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Entry(bet_frame, textvariable=self.bet_amount, width=5).pack(side=tk.LEFT)

        tk.Label(bet_frame, text="Bet Lines (1-7, comma-separated or 'all'):", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        self.bet_lines_entry = tk.Entry(bet_frame, width=20)
        self.bet_lines_entry.pack(side=tk.LEFT)
        self.bet_lines_entry.insert(0, "all")

        # Spin button
        self.spin_button = tk.Button(self.root, text="Spin", command=self.start_spin, font=("Arial", 14))
        self.spin_button.pack(pady=10)

        # Frame for the slot machine grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.reel_labels = [[tk.Label(self.grid_frame, text='   ', font=("Arial", 24), width=3, borderwidth=2, relief="groove") for _ in range(5)] for _ in range(3)]
        for r in range(3):
            for c in range(5):
                self.reel_labels[r][c].grid(row=r, column=c, padx=5, pady=5)

        # Message area
        self.message_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def start_spin(self, free_spin=False):
        self.total_spins += 1
        # Reset any previous highlights
        for row in self.reel_labels:
            for label in row:
                label.config(bg='SystemButtonFace')

        if not free_spin:
            # Get bet amount and lines
            try:
                bet_amount = float(self.bet_amount.get())
                if bet_amount <= 0:
                    messagebox.showerror("Invalid Bet", "Bet amount must be greater than zero.")
                    return
            except ValueError:
                messagebox.showerror("Invalid Bet", "Please enter a valid bet amount.")
                return

            bet_lines_input = self.bet_lines_entry.get().strip()
            if bet_lines_input.lower() == 'all':
                self.bet_lines = list(range(1, len(self.win_lines) + 1))
            else:
                try:
                    self.bet_lines = [int(x.strip()) for x in bet_lines_input.split(',') if x.strip().isdigit()]
                    self.bet_lines = [line for line in self.bet_lines if 1 <= line <= len(self.win_lines)]
                    if not self.bet_lines:
                        messagebox.showerror("Invalid Lines", "Please select valid lines to bet on.")
                        return
                except ValueError:
                    messagebox.showerror("Invalid Lines", "Please enter valid line numbers.")
                    return

            total_bet = bet_amount * len(self.bet_lines)
            if total_bet > self.balance:
                messagebox.showerror("Insufficient Balance", "You do not have enough balance for this bet.")
                return

            # Deduct bet amount from balance
            self.balance -= total_bet
            self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
            # Increment the progressive jackpot
            self.progressive_jackpot += total_bet * 0.05  # 5% of the bet goes to the jackpot
            self.jackpot_label.config(text=f"Jackpot: ${self.progressive_jackpot:.2f}")

            self.current_bet_amount = bet_amount
            self.current_bet_lines = self.bet_lines.copy()
        else:
            # For free spins, use the last bet amount and lines
            bet_amount = self.current_bet_amount
            self.bet_lines = self.current_bet_lines

        # Start spinning
        self.spin_button.config(state=tk.DISABLED)
        self.message_label.config(text="Spinning...")
        self.final_grid = None
        self.current_grid = [['   ' for _ in range(5)] for _ in range(3)]
        self.stopping_times = [random.randint(10, 15) + i*2 for i in range(5)]
        self.max_stopping_time = max(self.stopping_times)
        self.frame = 0
        self.animate_spin()

    def animate_spin(self):
        if self.frame < self.max_stopping_time:
            for col in range(5):
                if self.frame >= self.stopping_times[col]:
                    # Reel has stopped; set the final symbols for this reel
                    if not self.final_grid:
                        self.final_grid = [[random.choices(self.symbols, weights=self.weights)[0] for _ in range(5)] for _ in range(3)]
                    for row in range(3):
                        symbol = self.final_grid[row][col]
                        self.reel_labels[row][col].config(text=symbol)
                else:
                    # Reel is still spinning; assign random symbols
                    for row in range(3):
                        symbol = random.choice(self.symbols)
                        self.reel_labels[row][col].config(text=symbol)
            self.frame += 1
            self.root.after(100, self.animate_spin)
        else:
            # Spinning complete
            self.spin_button.config(state=tk.NORMAL)
            self.check_special_features()

    def check_special_features(self):
        if random.random() < 0.10:  # 10% chance to trigger Snake Wilds
            self.message_label.config(text="🐍 Snake Wilds Activated!")
            self.root.after(1000, self.apply_snake_wilds)
        else:
            self.process_results()

    def apply_snake_wilds(self):
        # Define the snake path
        snake_path = [
            (0, 0), (1, 0), (2, 0),
            (2, 1), (1, 1), (0, 1),
            (0, 2), (1, 2), (2, 2),
            (2, 3), (1, 3), (0, 3),
            (0, 4), (1, 4), (2, 4)
        ]
        for row, col in snake_path:
            if random.random() < 0.3:  # 30% chance to place a wild star
                self.final_grid[row][col] = '⭐'
                self.reel_labels[row][col].config(text='⭐')
        self.root.after(500, self.process_results)

    def process_results(self):
        self.check_wins()
        if self.free_spins > 0:
            self.play_free_spins()
        else:
            self.check_loyalty_reward()

    def check_wins(self):
        total_win = 0
        free_plays = 0
        bonus_triggered = False
        jackpot_won = False
        winning_positions = {}  # To store positions of winning symbols with their line color

        for index, line in enumerate(self.win_lines):
            if index + 1 not in self.bet_lines:
                continue  # Skip lines the player didn't bet on
            matched_symbols = [self.final_grid[row][col] for row, col in line]

            # Find the first non-wild symbol
            for symbol in matched_symbols:
                if symbol != '⭐':
                    first_symbol = symbol
                    break
            else:
                first_symbol = '⭐'  # All symbols are wildcards

            # Check for matching symbols
            match_count = 0
            for symbol in matched_symbols:
                if symbol == first_symbol or symbol == '⭐':
                    match_count += 1
                else:
                    break  # Stop counting if the sequence breaks

            # Calculate win based on the number of matches
            if match_count >= 3:
                line_win = 0
                if match_count == 3:
                    line_win = self.current_bet_amount * 1
                elif match_count == 4:
                    line_win = self.current_bet_amount * 2
                elif match_count == 5:
                    line_win = self.current_bet_amount * 5
                total_win += line_win
                self.message_label.config(text=f"🎉 Line {index + 1} win! Matched {match_count} '{first_symbol.strip()}' symbols! You win ${line_win:.2f}")
                self.root.after(1000)

                # Store winning positions and their line color
                color = self.line_colors[index]
                for i in range(match_count):
                    pos = line[i]
                    winning_positions[pos] = color

                # Check for bonus game trigger
                if first_symbol == '⭐' and match_count >= 5:
                    bonus_triggered = True

        # Highlight winning symbols
        for pos, color in winning_positions.items():
            row, col = pos
            self.reel_labels[row][col].config(bg=color)

        # Check for Yin-Yangs and calculate free plays
        yin_yang_count = sum(row.count('☯️ ') for row in self.final_grid)
        if yin_yang_count >= 3:
            if yin_yang_count == 3:
                free_plays += 8
                self.message_label.config(text="🎰 You get 8 free spins for 3 Yin-Yangs!")
            elif yin_yang_count == 4:
                free_plays += 15
                self.message_label.config(text="🎰 You get 15 free spins for 4 Yin-Yangs!")
            elif yin_yang_count == 5:
                free_plays += 20
                self.message_label.config(text="🎰 You get 20 free spins for 5 Yin-Yangs!")
            self.free_spins += free_plays
            self.root.after(1000)

        # Check for jackpot
        diamond_count = sum(row.count('💎') for row in self.final_grid)
        if diamond_count > 4:
            jackpot_won = True
            total_win += self.progressive_jackpot
            self.progressive_jackpot = 500.0
            self.jackpot_label.config(text=f"Jackpot: ${self.progressive_jackpot:.2f}")
            self.message_label.config(text=f"💎💎💎 JACKPOT! You won the progressive jackpot of ${total_win:.2f}! 💎💎💎")
            self.root.after(1000)

        if total_win != 0:
            self.balance += total_win
            self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        # Near miss encouragement
        if total_win == 0 and not jackpot_won:
            self.message_label.config(text="So close! Try again to win big!")
            self.root.after(1000)

        # Check for bonus game
        if bonus_triggered:
            self.root.after(1000, self.bonus_game)


    def bonus_game(self):
        # Simple bonus game: pick a card
        bonus_window = tk.Toplevel(self.root)
        bonus_window.title("Bonus Game")
        tk.Label(bonus_window, text="🎁 Bonus Game! Pick a card:", font=("Arial", 14)).pack(pady=10)
        cards = ['💰', '🍀', '💎', '🔥', '💣']
        random.shuffle(cards)

        def select_card(index):
            selected_card = cards[index]
            bonus_win = 0
            extra_spins = 0
            if selected_card == '💰':
                bonus_win = random.randint(10, 50)
                messagebox.showinfo("Bonus Game", f"💰 You won ${bonus_win} in the bonus game!")
            elif selected_card == '🍀':
                bonus_win = random.randint(5, 20)
                messagebox.showinfo("Bonus Game", f"🍀 You won ${bonus_win} in the bonus game!")
            elif selected_card == '💎':
                bonus_win = random.randint(50, 100)
                messagebox.showinfo("Bonus Game", f"💎 You won ${bonus_win} in the bonus game!")
            elif selected_card == '🔥':
                messagebox.showinfo("Bonus Game", "🔥 You didn't win anything, but you get 5 free spins!")
                extra_spins = 5
            elif selected_card == '💣':
                bonus_win = -20
                messagebox.showinfo("Bonus Game", "💣 Oh no! You lost $20!")
            self.balance += bonus_win
            self.free_spins += extra_spins
            self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
            bonus_window.destroy()
            self.process_results()

        card_frame = tk.Frame(bonus_window)
        card_frame.pack(pady=10)
        for i in range(5):
            btn = tk.Button(card_frame, text=f"Card {i+1}", command=lambda idx=i: select_card(idx), font=("Arial", 12))
            btn.pack(side=tk.LEFT, padx=5)

    def play_free_spins(self):
        if self.free_spins > 0:
            self.message_label.config(text=f"Starting Free Spin ({self.free_spins} left)...")
            self.free_spins -= 1
            self.root.after(1000, lambda: self.start_spin(free_spin=True))
        else:
            self.check_loyalty_reward()

    def check_loyalty_reward(self):
        # Loyalty reward every 10 spins
        print(self.total_spins % 10)
        if self.total_spins % 10 == 0:
            self.message_label.config(text="🎁 Loyalty Reward! You get a free spin! 🎁")
            self.root.after(1000, lambda: self.start_spin(free_spin=True))
        else:
            # Encouraging message
            self.message_label.config(text="Good luck on your next spin!")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SlotMachineGame(root)
    root.mainloop()
