import os

from PIL import Image, ImageTk

from tkinter import Tk, Button, Label
from tkinter.messagebox import showinfo

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.resizable(False, False)
        self.window.config(bg = '#F2F4FF')
        
        self.board = [''] * 9
        self.current_player = 'X'

        self.winner = None
        self.load_wins_from_file()
        
        self.create_ui()

        self.window.update_idletasks()
        
        win_width = self.window.winfo_reqwidth()
        win_height = self.window.winfo_reqheight()

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        
        self.window.geometry(f'{win_width}x{win_height}+{x}+{y}')
    
    def create_ui(self):
        self.buttons = [Button(self.window, text = '', font = ('Calisto MT', 24), width = 6, height = 3, relief = 'groove', bg = '#A9D3FF', activebackground = '#CEE4FF', command = lambda i = i: self.on_click(i)) for i in range(9)]

        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row = row, column = col, padx = 2, pady = 2)
        
        self.reset_button = Button(self.window, text = 'Reset', command = self.reset_game, font = ('Candara', 16), bg = '#A0CCFB', activebackground = '#A9D3FF', fg = '#454A45', activeforeground = '#454A45')
        self.reset_button.grid(row = 3, column = 0, columnspan = 3, sticky = 'EW', padx = (5, 5), pady = (5, 5))

        self.player_stats_label = Label(self.window, text = 'Player Stats: X - 0, O - 0', font = ('Candara', 14), pady = 5, fg = '#1E201E')
        self.player_stats_label.grid(row = 4, column = 0, columnspan = 3)

        self.update_player_stats()
    
    def on_click(self, index):
        if self.board[index] == '' and not self.winner:
            self.board[index] = self.current_player
            self.update_button_text(index)

            self.check_winner()
            self.switch_player()
    
    def update_button_text(self, index):
        self.buttons[index].config(text = self.current_player, state = 'disabled')
    
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def check_winner(self):
        win_conditions = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]

        for condn in win_conditions:
            if self.board[condn[0]] == self.board[condn[1]] == self.board[condn[2]] != '':
                self.winner = self.current_player

                self.update_player_wins(self.current_player)
                self.update_player_stats()
                self.show_winner_message()
                break
        
        else:
            if '' not in self.board:
                self.show_draw_message()
    
    def update_player_wins(self, player):
        self.wins[player] += 1
    
    def show_winner_message(self):
        showinfo('Winner!', f'Player {self.current_player} wins!')
        self.reset_game()
    
    def show_draw_message(self):
        showinfo('Draw!', "It's a draw!")
        self.reset_game()
    
    def reset_game(self):
        for i in range(9):
            self.buttons[i].config(text = '', state = 'normal')
            self.board[i] = ''
        
        self.current_player = 'X'
        self.winner = None
    
    def update_player_stats(self):
        self.player_stats_label.config(text = f"Player Stats: X - {self.get_wins('X')}, O - {self.get_wins('O')}")
        self.save_wins_to_file()
    
    def load_wins_from_file(self):
        if os.path.exists('wins.txt'):
            with open('wins.txt', 'r') as file:
                data = file.read().split(', ')
                self.wins = {
                    'X': int(data[0]),
                    'O': int(data[1])
                }
        
        else:
            self.wins = {
                'X': 0,
                'O': 0
            }
    
    def save_wins_to_file(self):
        with open('wins.txt', 'w') as file:
            file.write(f"{self.wins['X']}, {self.wins['O']}")
    
    def get_wins(self, player):
        return self.wins[player]
    
    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    game = TicTacToe()
    game.run()