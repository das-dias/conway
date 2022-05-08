""" ***********************************
* *[author] Diogo André (git-hub : das-dias)
* *[date] 2022-05-07
* *[summary] Implementation of the grid cell, cell and board classes for the game of life, with GUI
* ***********************************
"""
import tkinter as tk
from loguru import logger as log
import numpy as np
import time
import threading as th
import pickle
from write import write_grid
from copy import copy
class Cell(object):
    FILLED_COLOUR_CELL = "black"
    EMPTY_COLOUR_CELL = "white"
    FILLED_COLOUR_BORDER = "white"
    EMPTY_COLOUR_BORDER = "black"
    
    def __init__(self, master, x, y, size):
        """
        Constructor for the cell object
        """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.state = False # False == empty / dead | True == filled / alive
    
    def kill(self):
        """
        Switch the state of the cell
        """
        self.state = False
    
    def birth(self):
        """
        Switch the state of the cell
        """
        self.state = True    
    
    def draw(self):
        """_summary_
        Draws the cell on the grid
        Args:
            grid (_type_): _description_
        """
        if bool(self.master):
            fill = Cell.FILLED_COLOUR_CELL if self.state else Cell.EMPTY_COLOUR_CELL
            outline = Cell.FILLED_COLOUR_BORDER if self.state else Cell.EMPTY_COLOUR_BORDER
            
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)

class Grid(tk.Canvas):
    """_summary_
    Class for the grid object
    Args:
        tk (_type_): _description_
    """
    def __init__(self, master, grid_size, cell_size, max_gen=None, speed=2, *args, **kwargs):
        """_summary_
        Constructor for the grid object
        Args:
            master (_type_): _description_
            grid_size (_type_): _description_
            cell_size (_type_): _description_
            max_gen (_type_, optional): _description_. Defaults to None.
            speed (int, optional): _description_. Defaults to 2.
        """
        # init canvas main app
        tk.Canvas.__init__(self, master, width=cell_size*grid_size, height=cell_size*grid_size, *args, **kwargs)
        
        self.size = grid_size
        self.cell_size = cell_size
        self.grid=np.zeros((grid_size,grid_size)) # to memorize the switched cells
        self.gui_grid = [[Cell(self, x, y, cell_size) for x in range(grid_size)] for y in range(grid_size)]
        self.running = False
        self.max_gen = max_gen
        self.current_gen = 0
        self.speed = speed
        self.save_path = ""
        # bind clicking action on the grid
        self.bind("<Button-1>", self.handleLeftClick)
        # handle a single step in the generations
        self.bind("<Button-2>", self.handleRightClick)
        # handle automatic run
        self.master.bind("<Button-3>", self.handleEnter)
    
    def save_grid(self, path):
        self.save_path = path
    
    def draw_grid(self):
        [[cell.draw() for cell in self.gui_grid[row]] for row in range(len(self.gui_grid))]

    def init_grid(self, grid: np.ndarray):
        if grid is None:
            return
        if not grid.shape == self.grid.shape:
            raise ValueError("The initialization grid shape does not match the grid shape of the grid")
        self.grid = copy(grid)
        [[cell.birth() for col,cell in enumerate(self.gui_grid[row]) if self.grid[row,col] == 1] for row in range(len(self.gui_grid))]
    
    def random_grid(self):
        self.grid = np.random.randint(2, size=(self.size, self.size))
        [[cell.birth() for col,cell in enumerate(self.gui_grid[row]) if self.grid[row,col] == 1] for row in range(len(self.gui_grid))]
    
    def _update_grid(self):
        """
        Updates the grid array with the current state of the cells
        """
        for row in range(len(self.gui_grid)):
            for col,cell in enumerate(self.gui_grid[row]):
                self.grid[row,col] = bool(cell.state)
    
    def cell_purgatory(self):
        """
        Checks each cell's 8-way neighbourhood to determine if it should be alive or dead
        """
        changed = False
        row, col = self.grid.shape
        for y in range(row):
            for x in range(col):
                alive = 0
                # get the cell's neighbours
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (i,j) != (0,0):
                            if 0 <= y+i < row and 0 <= x+j < col:
                                alive += self.grid[(y+i), (x+j)]
                # check for Underpopulation rule
                if self.grid[y,x] == 1 and alive < 2:
                    self.gui_grid[y][x].kill()
                    self.gui_grid[y][x].draw()
                    changed = True
                # check for Overpopulation rule
                if self.grid[y,x] == 1 and alive>3:
                    self.gui_grid[y][x].kill()
                    self.gui_grid[y][x].draw()
                    changed = True
                # check for Rebirth rule
                if self.grid[y,x] == 0 and alive == 3:
                    self.gui_grid[y][x].birth()
                    self.gui_grid[y][x].draw()
                    changed = True
        # update the grid
        self._update_grid()
        return changed
    
    def start(self):
        """
        Starts the game
        """
        if self.running:
            if self.max_gen is not None and self.current_gen > self.max_gen:
                self.running = False
                return
            changed = self.cell_purgatory()
            time.sleep(1/self.speed)
            self.current_gen += 1
            if not changed:
                self.running = False
                return
            self.start()
    
    
    # events definition and probing
    def _event_coords(self, event):
        """ 
        Returns mouse event coordinates
        """
        row = int(event.y/self.cell_size)
        col = int(event.x/self.cell_size)
        return row, col

    def handleLeftClick(self, event):
        row, col = self._event_coords(event)
        cell = self.gui_grid[row][col]
        if cell.state: # if cell is already alive, kill it
            cell.kill()
        else: # if cell is dead, birth it
            cell.birth()
        cell.draw()
        self.grid[row,col] = bool(cell.state)
    
    def handleRightClick(self, event):
        """_summary_
        Run a single step in the game
        Args:
            event (_type_): _description_
        """
        self.cell_purgatory()
        self.current_gen += 1

    def handleEnter(self, event):
        """_summary_
        Run the game automatically
        Args:
            event (_type_): _description_
        """
        if bool(self.save_path):
            write_grid(self.grid, self.save_path)
        self.running = True
        thread = th.Thread(target=self.start)
        # start thread
        thread.start()
        
        
        
    
    
    
    
    
        
                
        
    
        