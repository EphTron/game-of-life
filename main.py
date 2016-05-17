import time
import math, random
import pygame, sys
from pygame.locals import *

def main():

    # set up pygame
    pygame.init()

    game = App("test",
                0.125,
                90,
                90, 
                10,10)

    game.run()

class App:
    def __init__(self, name, tick_time, cols, rows, rect_w, rect_h):
        self.name = name
        self.play = False
        self.timer = time.time()
        self.tick_time = tick_time

        self.mouse_lock = False
        self.mouse_mode = 1
        self.running_time = 0.0
        self.elapsed_time = 0.0
        self.last_rect = None

        self.proxy_alive = Rect(-1,0,0,0,0,(0,0), 1)
        self.proxy_dead = Rect(-2,0,0,0,0,(0,0), 0)

        self.rects = []
        self.rect_count = 0

        self.cols = cols
        self.rows = rows
        self.rect_w = rect_w
        self.rect_h = rect_h
        self.init_grid()
        #for rect in self.rects:
            #rect.get_neighbor_count()


        self.app_size = (cols * rect_w, rows * rect_h)
        self.screen = pygame.display.set_mode(self.app_size, 0, 32)

        # set up the colors
        self.colors = {
            "BLACK" :(0, 0, 0),
            "WHITE" :(255, 255, 255),
            "RED" :(255, 0, 0),
            "GREEN" :(0, 255, 0),
            "BLUE" :(0, 0, 255),
        }

        # set up the window
        pygame.display.set_caption(self.name)

        # draw the white background onto the surface
        self.screen.fill(self.colors["GREEN"])

    def init_grid(self):
        self.rect_count = self.cols *self.rows
        for idx in range(0,self.rect_count):
                _new_rect = Rect(idx, 
                                 (idx % self.cols) * self.rect_w,
                                 (idx / self.cols) * self.rect_h,
                                 (idx % self.cols),
                                 (idx / self.cols),
                                 (self.rect_w,self.rect_h),
                                 #1)
                                 random.getrandbits(1))
                self.rects.append(_new_rect)

        print "count",self.rect_count
        print "ROWS: ",self.rows
        print "COLS: ",self.cols
        print "width", self.rect_w
        print "height", self.rect_h
        print self.cols * self.rect_w

        for rect in self.rects:            
            #print "create neighbors for rect:",rect.id
            col = rect.col
            row = rect.row
            #print col, row
            rect.add_neighbor(self.get_rect_by_col_row(col-1,row-1))
            rect.add_neighbor(self.get_rect_by_col_row(col  ,row-1))
            rect.add_neighbor(self.get_rect_by_col_row(col+1,row-1))
            rect.add_neighbor(self.get_rect_by_col_row(col-1,row))
            rect.add_neighbor(self.get_rect_by_col_row(col+1,row))
            rect.add_neighbor(self.get_rect_by_col_row(col-1,row+1))
            rect.add_neighbor(self.get_rect_by_col_row(col  ,row+1))
            rect.add_neighbor(self.get_rect_by_col_row(col+1,row+1))

            
    def get_rect_by_col_row(self, col, row):
        #set proxy to be either dead or alive
        _proxy = self.proxy_dead
        #_proxy = self.proxy_alive
        if col >= 0 and row >= 0: #if bigger than 0
            if col >= self.cols:  #if too big
                return _proxy
            elif row >= self.rows:#if too big
                return _proxy
            else:                 # good candidate   
                _idx = row * self.cols + (col % self.cols)
                try:
                    return self.rects[_idx]
                except IndexError:
                    return _proxy
        else:
            return _proxy

    def get_rect_by_pos(self,x,y):
        _col = x / self.rect_w 
        _residual_col = x % self.rect_w
        #_col = _col - _residual_col
        _row = y / self.rect_h
        _residual_row = y % self.rect_h
        #_row = _row - _residual_row
        _idx = _row * self.cols + (_col % self.cols)
        try:
            return self.rects[_idx]
        except IndexError:
            return self.rects[0]

    def get_rect_size(self):
        if self.app_size[0] == self.app_size[1]:
            _w = self.app_size[0]
            _h = self.app_size[1]
            _rect_size = _w / self.cols

            return (_rect_size,_rect_size)
        else:
            return (10,10)

    def add_color(self, color):
        self.colors.append(color)

    def get_color(self, color):
        return self.colors[color]

    def update_timer(self):
        _time = time.time()
        self.elapsed_time += self.delta_time(_time, self.timer)
        self.running_time += self.elapsed_time
        self.timer = _time 

    def delta_time(self, now, old_time):
        return now - old_time

    def clear_rects(self):
        for rect in self.rects:
            rect.set_active(0)
            

    def draw_rects(self):
        for rect in self.rects:
            rect.draw(self.screen)

    def run(self):

        # run the game loop
        while True:
            self.update_timer()
            if self.elapsed_time >= self.tick_time:
                self.screen.fill(self.colors["WHITE"])
                self.elapsed_time = self.elapsed_time % self.tick_time
                self.draw_rects()
                if self.play:
                    for rect in self.rects:
                        rect.evaluate_environment()
                    for rect in self.rects:
                        rect.next_gen()
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif (event.type == KEYDOWN):
                    if event.key == K_w:
                        self.clear_rects()

                    if event.key == K_r:
                        self.play = not self.play
                        print "play is", self.play

                    if event.key == K_x:
                        pygame.quit()
                        sys.exit()
                elif event.type == KEYUP:
                    pass
                    #if event.key == K_w:
                    #    ...
                if event.type == MOUSEBUTTONDOWN:
                    self.mouse_lock = True
                    _pos = pygame.mouse.get_pos()
                    _rect = self.get_rect_by_pos(_pos[0],_pos[1])
                    _mode = pygame.mouse.get_pressed()
                    if _mode[0] == 1:
                        _rect.set_active(1) 
                    elif _mode[2] == 1:
                        _rect.set_active(0) 
                            
                    self.last_rect = _rect
                    

                if self.mouse_lock and event.type == MOUSEMOTION:
                    _pos = pygame.mouse.get_pos()
                    _rect = self.get_rect_by_pos(_pos[0],_pos[1])
                    if _rect != self.last_rect:
                        _mode = pygame.mouse.get_pressed()
                        if _mode[0] == 1:
                            _rect.set_active(1) 
                            
                        elif _mode[2] == 1:
                            _rect.set_active(0) 
                            

                if event.type == MOUSEBUTTONUP:
                    
                    self.mouse_lock = False
                 
                    



class Rect:
    def __init__(self, idx, x, y, col, row, size, flag):
        self.id = idx
        self.x = x
        self.y = y
        self.col = col 
        self.row = row
        self.size = size
        self.active = flag
        
        self.next_gen_active = flag
        self.color = (0, 0, 0)
        self.neighbors = []
        self.neighbors_count = 0
        self.active_neighbors = 0

        if self.active:
            self.color = (255, 255, 255)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def get_neighbor_count(self):
        self.neighbors_count = 0
        for rect in self.neighbors:
            if rect.id >= 0:
                self.neighbors_count += 1
        print "rect", self.id, "has ", self.neighbors_count, "neighbors"

    def print_neighbors(self):
        for rect in self.neighbors:
            print self.id, " has neighbor :", rect.id

    def get_active_neighbors(self):
        self.active_neighbors = 0
        for rect in self.neighbors:
            if rect.active:
                self.active_neighbors += 1
        return self.active_neighbors

    def evaluate_environment(self):
        self.get_active_neighbors()
        if self.active:
            if self.active_neighbors < 2:
                self.next_gen_active = 0
            elif self.active_neighbors > 3:
                self.next_gen_active = 0
            else:
                self.next_gen_active = 1
        if self.active == False:
            if self.active_neighbors == 3:
                self.next_gen_active = 1
            else:
                self.next_gen_active = 0

    def next_gen(self):
        self.set_active(self.next_gen_active)
        

    def toggle_active(self):
        self.active = not self.active
        if self.active:
            self.color = (255, 255, 255)
        else: 
            self.color = (0, 0, 0)


    def set_active(self, flag):
        self.active = flag
        if self.active:
            self.color = (255, 255, 255)
        #if not self.active and _old_state == 1:
        #    self.color = (50, 50, 50)
        else: 
            self.color = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, #surface
                         self.color, #color
                         (self.x, self.y, #x and y
                          self.size[0], self.size[1]) #width and height
                        )

            
if __name__ == '__main__':
    main()
