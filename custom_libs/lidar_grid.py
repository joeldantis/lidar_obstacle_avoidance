import math
import numpy as np

class LidarOccupancyGrid:

    def __init__(self, grid_size: int =100, resolution: float = 0.05):
        self.grid_size = grid_size
        self.resolution = resolution  # meters per pixel
        self.center = grid_size // 2

        # 0 = free/unexplored (black), 255 = occupied/hit (white)
        self.grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

    def clear(self):
        self.grid.fill(0)

    def plot(self, angle_deg: float, dist_mm: float):
        """Transforms a polar reading into a grid pixel and marks it."""
        if dist_mm <= 0:
            return

        dist_m = dist_mm / 1000.0

        # Convert polar to Cartesian (sensor reference frame)
        rad = math.radians(angle_deg)
        x = dist_m * math.cos(rad)
        y = dist_m * math.sin(rad)

        # Convert Cartesian (meters) to matrix index
        # Flip y so positive y points up on screen
        col = int(self.center + (x / self.resolution))
        row = int(self.center - (y / self.resolution))

        try:
            self.grid[row, col] = 255
        except IndexError:
            pass

    def current_pos(self):
        self.grid[self.center, self.center] = 50

    def dest(self, dist: float):
        row = round(dist/self.resolution)
        col = self.center
        self.grid[row, col]