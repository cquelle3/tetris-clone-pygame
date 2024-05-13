import pygame
import sys
import random
import copy

class Game:
    def __init__(self, cols, rows, cell_size, fps):
        pygame.init()
        self.game_start = False
        self.STARTBLINK = pygame.USEREVENT
        self.start_blink = True
        pygame.time.set_timer(self.STARTBLINK, 400)
        self.screen_padding_x = 1000
        self.screen_padding_y = 300
        self.grid_pos_x = self.screen_padding_x/2
        self.grid_pos_y = self.screen_padding_y/2
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode((cols*cell_size + self.screen_padding_x, rows*cell_size + self.screen_padding_y))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font('fonts/Fipps-Regular.otf', 40)
        self.ui_font = pygame.font.Font('fonts/pixelmix.ttf', 20)
        self.fps = fps
        self.score = 0
        self.high_score = 0
        self.x_movement = [False, False]
        self.user_move_down = False
        self.rotation_index = 0
        self.level_time = 0
        self.fall_time = 0
        self.fall_speed = 0.35
        self.final_fall_speed = self.fall_speed    
        self.move_time = 0
        self.move_speed = 0.01
        self.grid = self.create_grid(cols, rows)
        self.next_shape_grid = self.create_grid(5, 5)
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.curr_shape = None
        self.next_shape = None
        self.shapes = {
            "i": {'color': (0, 255, 255), 'positions': [[0, 0], [1, 0], [2, 0], [3, 0]], 
                    'rotations': 
                        [
                            [[0, 0], [1, 0], [2, 0], [3, 0]], 
                            [[0, 0], [0, 1], [0, 2], [0, 3]]
                        ]
                },
                        # [
                        #     0000
                        #     ....
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     0...
                        #     0...
                        #     0...
                        #     0...
                        # ]
            "j": {'color': (0, 0, 255), 'positions': [[0, 0], [0, 1], [1, 1], [2, 1]],
                    'rotations':
                    [
                        [[0, 0], [0, 1], [1, 1], [2, 1]],
                        [[1, 0], [0, 0], [0, 1], [0, 2]],
                        [[2, 1], [2, 0], [1, 0], [0, 0]],
                        [[0, 2], [1, 2], [1, 1], [1, 0]]
                    ]  
                },
                        # [
                        #     0...
                        #     000.
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     00..
                        #     0...
                        #     0...
                        #     ....
                        # ],
                        # [
                        #     000.
                        #     ..0.
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     .0..
                        #     .0..
                        #     00..
                        #     ....
                        # ]
            "l": {'color': (255, 165, 0), 'positions': [[3, 0], [3, 1], [2, 1], [1, 1]],
                    'rotations':
                    [
                        [[3, 0], [3, 1], [2, 1], [1, 1]],
                        [[3, 2], [2, 2], [2, 1], [2, 0]],
                        [[1, 1], [1, 0], [2, 0], [3, 0]],
                        [[2, 0], [3, 0], [3, 1], [3, 2]]
                    ]  
                },
                        # [
                        #     ...0
                        #     .000
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     ..0.
                        #     ..0.
                        #     ..00
                        #     ....
                        # ],
                        # [
                        #     .000
                        #     .0...
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     ..00
                        #     ...0
                        #     ...0
                        #     ....
                        # ]
            "o": {'color': (255, 255, 0), 'positions': [[0, 0], [1, 0], [0, 1], [1, 1]],
                    'rotations':
                    [
                        [[0, 0], [1, 0], [0, 1], [1, 1]]
                    ]  
                },
                        # [
                        #     00..
                        #     00..
                        #     ....
                        #     ....
                        # ]
            "s": {'color': (0, 255, 0), 'positions': [[2, 0], [3, 0], [1, 1], [2, 1]],
                    'rotations':
                    [
                        [[2, 0], [3, 0], [1, 1], [2, 1]],
                        [[3, 1], [3, 2], [2, 0], [2, 1]]
                    ]
                },
                        # [
                        #     ..00
                        #     .00.
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     ..0.
                        #     ..00
                        #     ...0
                        #     ....
                        # ]
            "t": {'color': (119, 0, 200), 'positions': [[1, 0], [0, 1], [1, 1], [2, 1]],
                    'rotations':
                    [
                        [[1, 0], [0, 1], [1, 1], [2, 1]],
                        [[1, 1], [0, 0], [0, 1], [0, 2]],
                        [[1, 1], [2, 0], [1, 0], [0, 0]],
                        [[0, 1], [1, 2], [1, 1], [1, 0]]
                    ]  
                },
                        
                        # [
                        #     .0..
                        #     000.
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     0...
                        #     00..
                        #     0...
                        #     ....
                        # ],
                        # [
                        #     000.
                        #     .0..
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     .0..
                        #     00..
                        #     .0..
                        #     ....
                        # ]
                        
            "z": {'color': (255, 0, 0), 'positions': [[0, 0], [1, 0], [1, 1], [2, 1]],
                    'rotations':
                    [
                        [[0, 0], [1, 0], [1, 1], [2, 1]],
                        [[1, 0], [1, 1], [0, 1], [0, 2]]
                    ]
                }
                        # [
                        #     00..
                        #     .00.
                        #     ....
                        #     ....
                        # ],
                        # [
                        #     .0..
                        #     00..
                        #     0...
                        #     ....
                        # ]
        }

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_movement[0] = True
                        self.move_time = self.move_speed + 1
                    if event.key == pygame.K_RIGHT:
                        self.move_time = self.move_speed + 1
                        self.x_movement[1] = True
                    if event.key == pygame.K_DOWN:
                        self.final_fall_speed = 0.01
                        self.user_move_down = True
                    if event.key == pygame.K_UP:
                        self.rotate_curr_shape()
                    if event.key == pygame.K_SPACE and not self.game_start:
                        self.game_start = True
                        self.reset_game()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.x_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.x_movement[1] = False
                    if event.key == pygame.K_DOWN:
                        self.final_fall_speed = self.fall_speed
                        self.user_move_down = False
                if not self.game_start:
                    if event.type == self.STARTBLINK:
                        self.start_blink = not self.start_blink


            #draw the game
            self.draw_grid()
            #draw the ui
            self.draw_ui()
            #draw grid for next shape
            self.draw_next_grid()

            if self.game_start:
                #spawning shapes
                #checking for gameover
                if self.curr_shape == None: 
                    self.curr_shape = self.spawn_shape()
                    self.game_start = not self.gameover_check()
                    self.insert_shape(self.curr_shape)
                    self.insert_shape_next(self.next_shape)
                
                #set high score after gameover
                if not self.game_start:
                    if self.score > self.high_score:
                        self.high_score = self.score

                #make the difficulty harder every 10 seconds
                self.level_time += self.clock.get_rawtime()
                if self.level_time/1000 > 5:
                    self.level_time = 0
                    #increase speed of fall speed
                    if self.fall_speed > 0.15:
                        self.fall_speed -= 0.01
                        #if the user isn't manually moving shape down, set final fall speed
                        if self.user_move_down == False:
                            self.final_fall_speed = self.fall_speed

                #moving shapes down
                self.fall_time += self.clock.get_rawtime()
                if self.fall_time / 1000 > self.final_fall_speed:
                    self.fall_time = 0
                    if not self.hit_bottom():
                        self.move_curr_shape(0, 1)
                    else:
                        self.cement_curr_shape()
                        self.check_and_remove_rows()
                        self.curr_shape = None
                        self.rotation_index = 0

                #moving shapes left and right
                self.move_time += self.clock.get_rawtime()
                if self.move_time / 1000 > self.move_speed:
                    self.move_time = 0
                    if self.curr_shape != None:
                        if not self.hit_wall(self.x_movement[1] - self.x_movement[0]):
                            self.move_curr_shape(self.x_movement[1] - self.x_movement[0], 0)

            pygame.display.update()
            self.clock.tick(self.fps)

    def create_grid(self, cols, rows):
        #create grid with black cells
        #0 = empty, 1 = placed block, 2 = moving block
        grid = [[{'type': 0, 'color': (0, 0, 0)} for i in range(cols)] for j in range(rows)]
        return grid
    
    def draw_grid(self):
        #draw cells
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(self.screen, self.grid[row][col]['color'], pygame.Rect(col * self.cell_size + self.grid_pos_x, row * self.cell_size + self.grid_pos_y, self.cell_size, self.cell_size))
        #draw grid lines
        for col in range(self.cols+1):
            pygame.draw.line(self.screen, (100, 100, 100), (col * self.cell_size + self.grid_pos_x, self.grid_pos_y), (col * self.cell_size + self.grid_pos_x, self.cell_size * self.rows + self.grid_pos_y), 1)
        for row in range(self.rows+1):
            pygame.draw.line(self.screen, (100, 100, 100), (self.grid_pos_x, row * self.cell_size + self.grid_pos_y), (self.cell_size * self.cols + self.grid_pos_x, row * self.cell_size + self.grid_pos_y), 1)

    def draw_next_grid(self):        
        #draw cells
        for row in range(len(self.next_shape_grid)):
            for col in range(len(self.next_shape_grid[0])):
                pygame.draw.rect(self.screen, self.next_shape_grid[row][col]['color'], pygame.Rect((self.cols * self.cell_size) + ((col+1) * self.cell_size) + self.grid_pos_x + self.screen_padding_x/10, (row+1) * self.cell_size + self.grid_pos_y, self.cell_size, self.cell_size))
        #draw grid lines
        for col in range(len(self.next_shape_grid[0])+1):
            pygame.draw.line(self.screen, (100, 100, 100), ((self.cols * self.cell_size) + (col * self.cell_size) + self.grid_pos_x + self.screen_padding_x/10, self.grid_pos_y), ((self.cols * self.cell_size) + (col * self.cell_size) + self.grid_pos_x + self.screen_padding_x/10, self.cell_size * len(self.next_shape_grid) + self.grid_pos_y), 1)
        for row in range(len(self.next_shape_grid)+1):
            pygame.draw.line(self.screen, (100, 100, 100), ((self.cols * self.cell_size) + self.grid_pos_x + self.screen_padding_x/10, row * self.cell_size + self.grid_pos_y), ((self.cols * self.cell_size) + (self.cell_size * len(self.next_shape_grid[0])) + self.grid_pos_x + self.screen_padding_x/10, row * self.cell_size + self.grid_pos_y), 1)

    def draw_ui(self):
        #render title
        title_surface = self.title_font.render('Tetris', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width()/2, self.screen_padding_y/4))
        self.screen.blit(title_surface, title_rect)
        
        #score
        score_surface = self.ui_font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.screen.get_width()-self.screen_padding_x/4, self.screen.get_height()-self.screen_padding_y/2))
        self.screen.blit(score_surface, score_rect)
        #high score
        high_score_surface = self.ui_font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(self.screen_padding_x/4, self.screen.get_height()-self.screen_padding_y/2))
        self.screen.blit(high_score_surface, high_score_rect)
        #if game not started, draw start UI
        if not self.game_start:
            if self.start_blink:
                start_surface = self.ui_font.render('Hit SPACE to start', True, (255, 255, 255))
                start_rect = start_surface.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()-self.screen_padding_y/4))
                self.screen.blit(start_surface, start_rect)

    def spawn_shape(self):
        if self.next_shape == None:
            self.next_shape = copy.deepcopy(self.shapes[random.choice(list(self.shapes.keys()))])
        new_shape = copy.deepcopy(self.next_shape)
        self.next_shape = copy.deepcopy(self.shapes[random.choice(list(self.shapes.keys()))])
        #set shape spawn point
        for cell in new_shape['positions']:
            cell[0] += int(self.cols/2) - 2
        return new_shape
    
    def insert_shape(self, shape):
        for cell in shape['positions']:
            self.grid[cell[1]][cell[0]] = {'type': 2, 'color': shape['color']}

    def insert_shape_next(self, shape):
        #clear next shape grid
        self.next_shape_grid = [[{'type': 0, 'color': (0, 0, 0)} for i in range(len(self.next_shape_grid[0]))] for j in range(len(self.next_shape_grid))]
        #insert next shape
        for cell in shape['positions']:
            self.next_shape_grid[cell[1]][cell[0]] = {'type': 2, 'color': shape['color']}

    def move_curr_shape(self, x, y):
        #delete previous shape location
        for cell in self.curr_shape['positions']:
            self.grid[cell[1]][cell[0]] = {'type': 0, 'color': (0, 0, 0)}
        #insert new shape location
        for cell in self.curr_shape['positions']:
            #move x direction
            cell[0] += x
            #move y direction
            cell[1] += y
            self.grid[cell[1]][cell[0]] = {'type': 2, 'color': self.curr_shape['color']}

    def rotate_curr_shape(self):
        #get old rotation
        old_rotation = copy.deepcopy(self.curr_shape['rotations'][self.rotation_index])
        #increment rotation index
        prev_rotation_index = self.rotation_index
        self.rotation_index += 1
        if self.rotation_index >= len(self.curr_shape['rotations']):
            self.rotation_index = 0
        #get new rotation
        new_rotation = copy.deepcopy(self.curr_shape['rotations'][self.rotation_index])
        #delete previous shape location
        for cell in self.curr_shape['positions']:
            self.grid[cell[1]][cell[0]] = {'type': 0, 'color': (0, 0, 0)}
        #rotate shape
        final_rotation = copy.deepcopy(self.curr_shape['positions'])
        for i in range(len(self.curr_shape['positions'])):
            final_rotation[i][0] += (new_rotation[i][0] - old_rotation[i][0])
            final_rotation[i][1] += (new_rotation[i][1] - old_rotation[i][1])
        #check if rotation is valid
        if self.rotation_valid(final_rotation):
            self.curr_shape['positions'] = final_rotation
        else:
            self.rotation_index = prev_rotation_index
        #insert new shape location
        for cell in self.curr_shape['positions']:
            self.grid[cell[1]][cell[0]] = {'type': 2, 'color': self.curr_shape['color']}

    def rotation_valid(self, locations):
        for cell in locations:
            #if out of bounds
            if cell[0] < 0 or cell[0] >= self.cols or cell[1] < 0 or cell[1] >= self.rows:
                return False
            #if in another shape
            elif self.grid[cell[1]][cell[0]]['type'] == 1:
                return False
        return True

    def cement_curr_shape(self):
        for cell in self.curr_shape['positions']:
            self.grid[cell[1]][cell[0]] = {'type': 1, 'color': self.curr_shape['color']}

    def hit_bottom(self):
        #check if any cell is hitting bottom of grid or another shape
        for cell in self.curr_shape['positions']:
            if cell[1] == self.rows-1:
                return True
            if self.grid[cell[1] + 1][cell[0]]['type'] == 1:
                return True
        return False
    
    def hit_wall(self, x):
        if self.curr_shape != None:
            for cell in self.curr_shape['positions']:
                x_loc = cell[0] + x
                if x_loc < 0 or x_loc > self.cols-1:
                    return True
                if self.grid[cell[1]][x_loc]['type'] == 1:
                    return True
        return False

    def check_and_remove_rows(self):
        #check for full rows
        full_rows = []
        for row in range(len(self.grid)):
            check = True
            for cell in self.grid[row]:
                if cell['type'] != 1:
                    check = False
            if check:
                full_rows.append(row)
        #for each full row, remove it and shift all previous rows down
        for i in full_rows:
            self.grid[i] = [{'type': 0, 'color': (0, 0, 0)} for i in range(self.cols)]
            for row in range(i, 0, -1):
                prev_row = copy.deepcopy(self.grid[row-1])
                self.grid[row] = prev_row
        #add score
        if len(full_rows) == 1:
            self.score += 40
        elif len(full_rows) == 2:
            self.score += 100
        elif len(full_rows) == 3:
            self.score += 300
        elif len(full_rows) == 4:
            self.score += 1200  

    def gameover_check(self):
        for cell in self.curr_shape['positions']:
            if self.grid[cell[1]][cell[0]]['type'] == 1:
                return True
        return False

    def reset_game(self):
        self.grid = self.create_grid(self.cols, self.rows)
        self.next_shape_grid = self.create_grid(5, 5)
        self.curr_shape = None
        self.next_shape = None
        self.score = 0
        self.fall_speed = 0.35

if __name__=='__main__':
    game = Game(10, 20, 30, 60)
    game.run()