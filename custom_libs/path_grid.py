from custom_libs.lidar_grid import LidarGrid
import numpy as np

class PathGrid():
    def __init__(self, map: LidarGrid):
        self.grid = np.zeros((map.grid_size, map.grid_size), dtype=np.uint8)

    def clear(self):
        self.grid.fill(0)

    def drawline(self, map:LidarGrid):
        x0 = map.center
        y0 = map.center
        x1 = map.dest[0]
        y1 = map.dest[1]

        

