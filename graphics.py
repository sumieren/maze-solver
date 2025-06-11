from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Maze Solver"

        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__running = False

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

    def close(self):
        self.__running = False

class Point:
    # x,y 0,0 is top left of screen
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point_1 = point1
        self.point_2 = point2

    def draw(self, canvas, color):
        x1, y1 = self.point_1.x, self.point_1.y
        x2, y2 = self.point_2.x, self.point_2.y
        canvas.create_line(x1, y1, x2, y2, fill = color, width = 2)