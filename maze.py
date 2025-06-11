from graphics import Line, Point
from time import sleep
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

        if seed:
            random.seed(seed)

    def __create_cells(self):
        for j in range(0, self.num_cols):
            result = []
            for i in range(0, self.num_rows):
                result.append(Cell(self.win))
            self.__cells.append(result)

        for col in range(0, self.num_cols):
            for row in range(0, self.num_rows):
                self.__draw_cell(col, row)


    def __draw_cell(self, x ,y):
        if self.win:
            cell = self.__cells[x][y]
            x1 = x * self.cell_size_x + self.x1
            y1 = y * self.cell_size_y + self.y1
            x2 = x1 + self.cell_size_x
            y2 = y1 + self.cell_size_y

            cell.draw(x1, y1, x2, y2)
            self.__animate()

    def __animate(self):
        if self.win:
            self.win.redraw()
        sleep(0.01)

    def __break_entrance_and_exit(self):
        entrance = self.__cells[0][0]
        exit = self.__cells[self.num_cols - 1][self.num_rows - 1]

        entrance.has_top_wall = False
        exit.has_bottom_wall = False

        self.__draw_cell(0, 0)
        self.__draw_cell(self.num_cols - 1, self.num_rows - 1)

    def __break_walls_r(self, x, y):
        current_cell = self.__cells[x][y]
        current_cell.visited = True

        while True:
            to_visit = []

            # check if can move left, right, up, down
            if x > 0:
                left_cell = self.__cells[x - 1][y]
                if not left_cell.visited:
                    to_visit.append((x - 1, y, "left"))
            if x < self.num_cols - 1:
                right_cell = self.__cells[x + 1][y]
                if not right_cell.visited:
                    to_visit.append((x + 1, y, "right"))
            if y > 0:
                top_cell = self.__cells[x][y - 1]
                if not top_cell.visited:
                    to_visit.append((x, y - 1, "up"))
            if y < self.num_rows - 1:
                bottom_cell = self.__cells[x][y + 1]
                if not bottom_cell.visited:
                    to_visit.append((x, y + 1, "down"))

            if len(to_visit) == 0:
                self.__draw_cell(x, y)
                return
            
            rand_direction = random.choice(to_visit)
            next_cell = self.__cells[rand_direction[0]][rand_direction[1]]

            match rand_direction[2]:
                case "left":
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
                case "right":
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                case "up":
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
                case "down":
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False

            self.__break_walls_r(rand_direction[0], rand_direction[1])

        
    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, x, y):
        current_cell = self.__cells[x][y]
        self.__animate()

        current_cell.visited = True

        if (x == self.num_cols - 1) and (y == self.num_rows - 1):
            return True
        
        directions = []
        if x > 0:
            directions.append((x - 1, y, "left"))
        if x < self.num_cols - 1:
            directions.append((x + 1, y, "right"))
        if y > 0:
            directions.append((x, y - 1, "up"))
        if y < self.num_rows - 1:
            directions.append((x, y + 1, "down"))
        random.shuffle(directions)

        for direction in directions:
            cell = self.__cells[direction[0]][direction[1]]
            cell_exists = cell != None
            cell_visited = cell.visited
            wall_in_direction = True
            match direction[2]:
                case "left":
                    wall_in_direction = current_cell.has_left_wall
                case "right":
                    wall_in_direction = current_cell.has_right_wall
                case "up":
                    wall_in_direction = current_cell.has_top_wall
                case "down":
                    wall_in_direction = current_cell.has_bottom_wall

            if cell_exists and not cell_visited and not wall_in_direction:
                current_cell.draw_move(cell)
                if self._solve_r(direction[0], direction[1]):
                    return True
                else:
                    current_cell.draw_move(cell, undo=True)
        
        return False

class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1

        self.__win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win:
            self.draw_wall(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), self.has_left_wall)
            self.draw_wall(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), self.has_right_wall)
            self.draw_wall(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), self.has_top_wall)
            self.draw_wall(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), self.has_bottom_wall)

    def draw_wall(self, line, has_wall=True):
        color = "white"
        if has_wall:
            color = "black"
        self.__win.draw_line(line, color)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"

        own_middle = ((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
        to_middle = ((to_cell.__x1 + to_cell.__x2) / 2, (to_cell.__y1 + to_cell.__y2) / 2)
        point1 = Point(own_middle[0], own_middle[1])
        point2 = Point(to_middle[0], to_middle[1])

        if self.__win:
            self.__win.draw_line(Line(point1, point2), color)