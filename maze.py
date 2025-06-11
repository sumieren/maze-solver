from graphics import Line, Point
from time import sleep

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
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

    def __create_cells(self):
        for j in range(0, self.num_cols):
            result = []
            for i in range(0, self.num_rows):
                result.append(Cell(self.win))
            self.__cells.append(result)

        for col in range(0, self.num_cols):
            for row in range(0, self.num_rows):
                if self.win:
                    self.__draw_cell(col, row)


    def __draw_cell(self, x ,y):
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
        sleep(0.05)

    def __break_entrance_and_exit(self):
        entrance = self.__cells[0][0]
        exit = self.__cells[self.num_cols - 1][self.num_rows - 1]

        entrance.has_top_wall = False
        exit.has_bottom_wall = False

        if self.win:
            self.__draw_cell(0, 0)
            self.__draw_cell(self.num_cols - 1, self.num_rows - 1)

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