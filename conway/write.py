import pickle
import numpy as np
import os
from loguru import logger as log

def write_grid(grid: np.ndarray, path: str):
    head, tail = os.path.split(path)
    if not os.path.exists(head):
        raise FileNotFoundError(f"File {head} not found")
    name, ext = os.path.splitext(tail)
    if ext != ".npy":
        raise ValueError(f"File {path} must be a .npy file")
    try:
        np.save(path, grid)
    except Exception as e:
        log.error(f"Error writting to file {path} - {e}")