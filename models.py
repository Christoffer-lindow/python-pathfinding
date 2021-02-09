from constants import COLORS
from queue import PriorityQueue
class Cell:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLORS["WHITE"]
        self.neighbors = []
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == COLORS["RED"]
    
    def is_open(self):
        return self.color == COLORS["GREEN"]
    
    def is_barrier(self):
        return self.color == COLORS["BLACK"]
    
    def is_start(self):
        return self.color == COLORS["ORANGE"]
    
    def is_end(self):
        return self.color == COLORS["TURQUIOSE"]
    
    def reset(self):
        self.color = COLORS["WHITE"]
    
    def close(self):
        self.color = COLORS["RED"]
    
    def open_self(self):
        self.color = COLORS["GREEN"]
    
    def turn_barrier(self):
        self.color = COLORS["BLACK"]
    
    def start(self):
        self.color = COLORS["ORANGE"]
    
    def end(self):
        self.color = COLORS["TURQUOISE"]
    
    def path(self):
        self.color = COLORS["PURPLE"]
    
    def draw(self,win,pygame, width, height):
        pygame.draw.rect(win, self.color, (self.x, self.y,width, height ))
    
    def update_neighbors(self,grid):
        self.neighboors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        

    def __lt__(self,other):
        return False

class Game:
    def __init__(self,pygame,width,height,rows):
        self.pygame = pygame
        self.width = width
        self.height = height
        self.rows = rows
        self.gap = self.width // self.rows
        self.win = self.pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Path finding")
        self.grid = self.create_grid()
        
    def h(self,p1,p2):
        x1,y1 = p1
        x2,y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def create_grid(self):
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                grid[i].append(Cell(i,j,self.gap,self.rows))
    
        return grid

    def draw_grid(self):
        for i in range(self.rows):
            self.pygame.draw.line(self.win,COLORS["GREY"], (0,i * self.gap), (self.width, i*self.gap))
            for j in range(self.rows):
                self.pygame.draw.line(self.win,COLORS["GREY"], (j * self.gap,0), (j * self.gap, self.width))

    def draw(self):
        self.win.fill(COLORS["WHITE"])

        for row in self.grid:
            for cell in row:
                cell.draw(self.win,self.pygame,self.width, self.height)
    
        self.draw_grid()
        self.pygame.display.update()

    def get_clicked_pos(self,pos):
        y,x = pos

        row = y // self.gap
        col = x // self.gap

        return row,col

    def get_cell_from_grid(self):
        pos = self.pygame.mouse.get_pos()
        row, col = self.get_clicked_pos(pos)
        return self.grid[row][col]

    def reconstruct_path(self,came_from,current):
        while current in came_from:
            current = came_from[current]
            current.path()
            self.draw()

    def algorithm(self,start,end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {cell: float("inf") for row in self.grid for cell in row}
        g_score[start] = 0
        f_score = {cell: float("inf") for row in self.grid for cell in row}
        f_score[start] = self.h(start.get_position(), end.get_position())

        open_set_hash = {start}

        while not open_set.empty():
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
        
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end)
                end.end()
                return True
            
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_position(), end.get_position())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.open_self()
            self.draw()

            if current != start:
                current.close()
    
        return False

    def run(self):
        start = None
        end = None
        run = True
        started = False

        while run:
            self.draw()
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    run = False

                if started:
                    continue

                if self.pygame.mouse.get_pressed()[0]:
                    cell = self.get_cell_from_grid()
                    if not start and cell != end:
                        start = cell
                        start.start()
                    elif not end and cell != start:
                        end = cell
                        end.end()
                
                    elif cell != end and cell != start:
                        cell.turn_barrier()

                elif self.pygame.mouse.get_pressed()[2]:
                    cell = self.get_cell_from_grid()
                    cell.reset()
                
                    if cell == start:
                        start = None
                    elif cell == end:
                        end = None
            
                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_SPACE and start and end:
                        for row in self.grid:
                            for cell in row:
                                cell.update_neighbors(self.grid)
                
                        self.algorithm(start, end)
                    if event.key == self.pygame.K_c:
                        start = None
                        end = None
                        self.grid = self.create_grid()

        self.pygame.quit()

