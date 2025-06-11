from graphics import Window
from maze import Maze, Cell

def main():
    win = Window(800, 600)

    Maze(50, 50, 12, 17, 40, 40, win)

    win.wait_for_close()

main()
