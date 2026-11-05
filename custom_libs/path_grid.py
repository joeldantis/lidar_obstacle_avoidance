from custom_libs.lidar_grid import LidarGrid
import numpy as np

class PathGrid():
    def __init__(self, map: LidarGrid):
        self.grid = np.zeros((map.grid_size, map.grid_size), dtype=np.uint8)

    def clear(self):
        self.grid.fill(0)

    def drawLine(self, map:LidarGrid):
        x0 = map.center
        y0 = map.center
        x1 = map.dest[0]
        y1 = map.dest[1]

        if abs(x1-x0) > abs(y1-y0):
            self.drawLineH(x0, y0, x1, y1)

        else:
            self.drawLineV(x0, y0, x1, y1)

    def drawLineH(self, x0:int, x1: int, y0: int, y1: int):
        if x0 > x1:
            x0,x1 = x1, x0
            y0,y1 = y1, y0

        dx = x1-x0
        dy = y1-y0

        dir = -1 if dy < 0 else 1
        dy *= dir

        if dx != 0:
            y = y0
            p = 2*dy - dx
            for i in range(dx+1):
                self.grid[x0+i, y]
                if p >= 0:
                    y += dir
                    p  = p - 2*dx
                p = p + 2*dy

    def drawLineV(self, x0:int, x1: int, y0: int, y1: int):
        if y0 > y1:
            x0,x1 = x1, x0
            y0,y1 = y1, y0

        dx = x1-x0
        dy = y1-y0

        dir = -1 if dx < 0 else 1
        dx *= dir

        if dy != 0:
            x = x0
            p = 2*dx - dy
            for i in range(dy+1):
                self.grid[x, y0+i]
                if p >= 0:
                    x += dir
                    p  = p - 2*dy
                p = p + 2*dx