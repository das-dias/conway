import pickle
import numpy as np
import os
from loguru import logger as log

def read_grid(path) -> np.ndarray:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File {path} not found")
    grid = None
    try:
        grid = np.load(path)
    except:
        log.error(f"Error reading file {path}. Must be a .npy file.")
    print(grid)
    return grid if isinstance(grid, np.ndarray) else None
    