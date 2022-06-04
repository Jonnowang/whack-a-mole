import os

import numpy as np
import PySimpleGUI as sg

sg.theme('BluePurple')

class Game:
    def __init__(self, size):
        # UI Settings slider
        self.grid_size = size
        self.reset_btn = sg.Button('Reset', key='-RESET-', size=(9, 1), font=('TkFixedFont', -14))
        # self.hint_btn = sg.Button('Hint', key='-HINT-', size=(9, 1), font=('TkFixedFont', -14))
        # self.solve_btn = sg.Button('Auto Solve', key='-SOLVE-', size=(9, 1), font=('TkFixedFont', -14))
        settings_layout = [self.reset_btn]
        self.settings = sg.Column([settings_layout])

        # Create game grid
        self.grid_state = None
        self.grid_layout = []
        self.grid = None
        self.setup_grid()
        layout = [[self.settings], [self.grid]]
        self.window = sg.Window('DreamsAI Task', layout)

    # Represent field as binary matrix or n^2 vector
    def setup_grid(self, reset=False):
        self.grid_state = np.random.randint(0, 2, size=(self.grid_size, self.grid_size), dtype='bool')
        if reset == False:
            for r in range(self.grid_size):
                row = []
                for c in range(self.grid_size):
                    if self.grid_state[r][c]:
                        image = "sprites/mole_out_sprite.png"
                    else:
                        image = "sprites/mole_in_sprite.png"
                    m = sg.Button(image_filename=image, pad=(0, 0), enable_events=True, key=f'tile{r}-{c}')
                    # add to layout row
                    row.append(m)
                self.grid_layout.append(row)
            self.grid = sg.Column(self.grid_layout, key="-GRID-")
        else:
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    if self.grid_state[r][c]:
                        image = "sprites/mole_out_sprite.png"
                    else:
                        image = "sprites/mole_in_sprite.png"
                    self.window.find_element(f'tile{r}-{c}').Update(image_filename=image)

    def update_grid(self, position):
        i = position[0]
        j = position[1]
        if self.grid_state[i][j] == False:
            return False
        self.make_hit(position)
        adj_index = [[i,j], [i+1,j], [i,j-1], [i-1,j], [i,j+1]]
        for square in adj_index:
            if all(k >= 0 for k in square) and all(k < self.grid_size for k in square):
                if self.grid_state[square[0]][square[1]]:
                    image = "sprites/mole_out_sprite.png"
                else:
                    image = "sprites/mole_in_sprite.png"
                self.window.find_element(f'tile{square[0]}-{square[1]}').Update(image_filename=image)
            else:
                pass
        return True

    def cast_to_vec(self, binary_matrix):
        return np.reshape(binary_matrix, self.grid_size**2)

    def make_hit(self, position):
        i = position[0]
        j = position[1]
        adj_index = [[i,j], [i+1,j], [i,j-1], [i-1,j], [i,j+1]]
        for square in adj_index:
            if all(k >= 0 for k in square) and all(k < self.grid_size for k in square):
                self.grid_state[square[0]][square[1]] = not self.grid_state[square[0]][square[1]]
            else:
                pass

    # def auto_solve(self):
    #     adj_field_list = list()
    #     # Generate list of all squares and adjacent squares
    #     for i in range(self.grid_size):
    #         for j in range(self.grid_size):
    #             cur_field = np.zeros((self.grid_size, self.grid_size), dtype = 'bool')
    #             adj_index = [[i,j], [i+1,j], [i,j-1], [i-1,j], [i,j+1]]
    #             for square in adj_index:
    #                 if all(k >= 0 for k in square) and all(k < self.grid_size for k in square):
    #                     cur_field[square[0]][square[1]] = True
    #                 else:
    #                     pass
    #             adj_field_list.append(cur_field)
    #     adj_field_list = list(map(self.cast_to_vec, adj_field_list))

def play():
    print("Starting game")
    valid = False
    while valid == False:
        try:
            size = int(input("(Please input a grid size between 2 and 9) \nEnter Grid Size:"))
            if size > 9 or size < 2:
                valid = False
            else:
                valid = True
        except ValueError:
            valid = False
    game = Game(size)

    while True:  # Event Loop
        event, values = game.window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            game.window.close()
            break
        if event[:4] == 'tile':
            position = [int(event[4]), int(event[6])]
            game.update_grid(position)
        if event == "-RESET-":
            game.setup_grid(True)
            
        
        
if __name__ == "__main__":
    play()