import math
import time
import cv2
import numpy as np
import serial
from rplidar_parser import RPLidarParser


class LidarOccupancyGrid:

    def __init__(
        self, grid_size: int = 500, resolution: float = 0.02
    ):  # 500x500 cells @ 2cm/cell = 10m x 10m
        self.grid_size = grid_size
        self.resolution = resolution  # meters per pixel
        self.center = grid_size // 2

        # 0 = free/unexplored (black), 255 = occupied/hit (white)
        self.grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

    def clear(self):
        """Clears or decays the grid between full scans."""
        self.grid.fill(0)

    def add_point(self, angle_deg: float, dist_mm: float):
        """Transforms a polar reading into a grid pixel and marks it."""
        if dist_mm <= 0:
            return

        dist_m = dist_mm / 1000.0

        # Convert polar to Cartesian (sensor reference frame)
        rad = math.radians(angle_deg)
        x = dist_m * math.cos(rad)
        y = dist_m * math.sin(rad)

        # Convert Cartesian (meters) to image matrix index (pixels)
        # Flip y so positive y points up on screen
        col = int(self.center + (x / self.resolution))
        row = int(self.center - (y / self.resolution))

        # Check bounds
        if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
            # Mark cell as occupied
            self.grid[row, col] = 255

    def get_display_image(self) -> np.ndarray:
        """Returns the grid with a center marker for the sensor."""
        # Convert grayscale to BGR for visualization
        display = cv2.cvtColor(self.grid, cv2.COLOR_GRAY2BGR)

        # Draw red dot at the sensor origin
        cv2.circle(
            display, (self.center, self.center), radius=3, color=(0, 0, 255), -1
)
        return display