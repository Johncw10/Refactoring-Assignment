import numpy as np
import random


class Landscape:
    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as open_file:
            self.width, self.height = [int(i) for i in open_file.readline().split(" ")]
            self.original_grid = np.zeros((self.height, self.width), int)
            for j, row in enumerate(open_file.readlines()):
                self.original_grid[j] = [int(square) for square in row.split(" ")]
        self.width_with_halo = self.width + 2
        self.height_with_halo = self.height + 2

    @property
    def halo_grid(self):
        new_grid = np.pad(self.original_grid, pad_width=1, mode='constant')
        return new_grid

    @property
    def count_dry_squares(self):
        return np.count_nonzero(self.halo_grid)

    def calculate_neighbours(self):
        neighbours = np.zeros((self.height_with_halo, self.width_with_halo), int)
        for x in range(1, self.height + 1):
            for y in range(1, self.width + 1):
                neighbours[x, y] = self.halo_grid[x - 1, y] \
                                   + self.halo_grid[x + 1, y] \
                                   + self.halo_grid[x, y - 1] \
                                   + self.halo_grid[x, y + 1]
        return neighbours

    def hare_density(self, hare_seed):
        return self.generate_grid_densities(hare_seed)

    def puma_density(self, puma_seed):
        return self.generate_grid_densities(puma_seed)

    def generate_grid_densities(self, random_seed):
        density_grid = self.halo_grid.astype(float)
        random.seed(random_seed)
        for x in range(1, self.height + 1):
            for y in range(1, self.width + 1):
                if self.halo_grid[x, y] == 1:
                    density_grid[x, y] = random.uniform(0, 5)
                else:
                    density_grid[x, y] = 0
        return density_grid
