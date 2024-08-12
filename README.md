# Slot Machine Game

This is a simple slot machine game implemented in Python. It simulates a slot machine with various symbols and win lines, allowing for free plays based on special symbols.

## Features

- **Symbols and Weights**: Uses symbols with associated weights to control their appearance frequency.
- **Win Lines**: Includes horizontal, diagonal, and zig-zag win lines.
- **Win Calculation**: Awards multipliers for matching symbols and provides free plays for special symbols (Yin-Yangs).
- **Free Plays**: Allows for additional spins with the free plays earned.

## How It Works

1. **Spin**: Generates a 5x3 grid of symbols based on predefined weights.
2. **Display**: Prints the slot machine grid.
3. **Win Checking**: Checks each win line for matching symbols and calculates win multipliers.
4. **Yin-Yang Special**: Awards free plays based on the number of Yin-Yangs.
5. **Play Free Plays**: Executes additional spins using the free plays awarded.

## Installation

No installation is required. You can run the script directly with Python.

## Usage

To run the slot machine game, simply execute the Python script:

```bash
python slots.py
