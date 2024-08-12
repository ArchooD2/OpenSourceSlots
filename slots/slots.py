import random

def spin_slot_machine():
    # Define the symbols that can appear on the slot machine and their respective weights
    symbols = ['9 ', '10', 'J ', 'Q ', 'K ', 'A ', '⭐', '☯️ ']
    weights = [30, 25, 20, 10, 5, 3, 2, 1]  # Example weights, higher means more common

    # Define win lines
    win_lines = [
        # Horizontal lines
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # Line 1
        [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],  # Line 2
        [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],  # Line 3
        
        # Diagonal lines
        [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # Line 4
        [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # Line 5
        
        # Zig-Zag lines 
        [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],  # Line 8
        [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],  # Line 9
    ]

    def spin():
        # Create a 5x3 grid of randomly selected symbols using the weights
        rows, cols = 3, 5
        slot_machine = [[random.choices(symbols, weights=weights)[0] for _ in range(cols)] for _ in range(rows)]
        
        # Display the slot machine to the user
        for row in slot_machine:
            print("| " + " | ".join(row) + " |")
        
        return slot_machine

    def check_wins(slot_machine):
        total_win_multiplier = 0
        free_plays = 0
        
        for line in win_lines:
            matched_symbols = [slot_machine[row][col] for row, col in line]
            first_symbol = matched_symbols[0]
            
            # Check if there are at least 3 matching symbols in the line
            match_count = 0
            for symbol in matched_symbols:
                if symbol == first_symbol:
                    match_count += 1
                else:
                    break  # Stop counting if the sequence breaks
            
            # Calculate win multiplier based on the number of matches
            if match_count >= 3:
                if match_count == 3:
                    print(f"🎉 Win with 3 symbols on line {win_lines.index(line) + 1}! 🎉")
                    total_win_multiplier += 1
                elif match_count == 4:
                    print(f"🎉 Win with 4 symbols on line {win_lines.index(line) + 1}! 🎉")
                    total_win_multiplier += 1.25
                elif match_count == 5:
                    print(f"🎉 Win with 5 symbols on line {win_lines.index(line) + 1}! 🎉")
                    total_win_multiplier += 1.9
        
        # Check for Yin-Yangs and calculate free plays
        yin_yang_count = sum(row.count('☯️ ') for row in slot_machine)
        if yin_yang_count == 3:
            free_plays += 8
            print("You get 8 free plays for 3 Yin-Yangs! 🎉")
        elif yin_yang_count == 4:
            free_plays += 15
            print("You get 15 free plays for 4 Yin-Yangs! 🎉")
        elif yin_yang_count == 5:
            free_plays += 20
            print("You get 20 free plays for 5 Yin-Yangs! 🎉")

        if total_win_multiplier > 0:
            print(f"Total win multiplier: {total_win_multiplier:.2f}")
        else:
            print("Better luck next time!")

        return total_win_multiplier, free_plays

    def play_free_plays(free_plays):
        total_win_multiplier = 0
        x = 0
        while free_plays > 0:
            print(f"\nFree Play {x+1}:")
            slot_machine = spin()
            win_multiplier, additional_free_plays = check_wins(slot_machine)
            total_win_multiplier += win_multiplier
            free_plays -= 1  # Decrement the free plays count
            x += 1
            free_plays += additional_free_plays  # Add any new free plays
            
        return total_win_multiplier

    # Initial spin
    slot_machine = spin()
    total_win_multiplier, free_plays = check_wins(slot_machine)

    while free_plays > 0:
        free_play_multiplier = play_free_plays(free_plays)
        total_win_multiplier += free_play_multiplier
        #break  # Exit the loop after the first set of free plays

    print(f"\nFinal Total win multiplier: {total_win_multiplier:.2f}")

# Run the slot machine
spin_slot_machine()
