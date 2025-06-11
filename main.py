from graphics import Window
from maze import Maze, Cell

def main():
    win = Window(800, 600)

    maze = Maze(50, 50, 12, 17, 40, 40, win)
    maze.solve()

    win.wait_for_close()

main()
