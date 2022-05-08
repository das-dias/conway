from loguru import logger as log
from tkinter import Tk
from board import Grid
from read import read_grid
import argparse
def main():
    log.info("Conway's Game of Life by Diogo André")
    parser = argparse.ArgumentParser(description="Conway's Game of Life by Diogo André")
    parser.add_argument("-g", "--grid-size", dest="gridsize", type=int, default=20, help="Size of the grid")
    parser.add_argument("-c", "--cell-size-", dest="cellsize", type=int, default=15, help="Size of each cell in the GUI")
    parser.add_argument("-s", "--speed", dest="speed", type=int, default=2, help="Number of computed generations per second")
    parser.add_argument("--random", dest="random", action="store_true", help="Randomize the initialization of the cell grid")
    parser.add_argument("-w", "--write", dest="write", type=str, help="Write the grid to a file")
    parser.add_argument("-r", "--read", dest="read", type=str, help="Read the grid from a file")
    args = parser.parse_args()
    app = Tk()
    app.title("Conway's Game of Life - Diogo André")
    grid = Grid(app, grid_size=args.gridsize, cell_size=args.cellsize, speed=args.speed)
    if args.random:
        grid.random_grid()
    if bool(args.read):
        grid.init_grid(read_grid(args.read))
    if bool(args.write):
        grid.save_grid(args.write)
    grid.draw_grid()
    grid.pack()
    
    app.mainloop()
    log.info(f"Maximum generation: {grid.current_gen}")

if __name__=="__main__":
    main()