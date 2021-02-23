from argparse import ArgumentParser
import numpy as np
import random
import os, sys
# Import Landscape (then more)

# from sim_functions import Landscape

def assert_non_neg_int(key, value):
    error_msg = "{} must be a non-negative integer, currently equals {}.".format(key, value)
    if value < 0:
        raise ValueError(error_msg)
    elif not isinstance(value, int):
        raise TypeError(error_msg)
    else:
        return value


def assert_non_neg_float(key, value):
    error_msg = "{} must be non-negative floating point number, currently equals {}.".format(key, value)
    if value < 0:
        raise ValueError(error_msg)
    elif not isinstance(value, float):
        raise TypeError(error_msg)
    else:
        return value


def assert_working_file(file):
    file_path = "./" + file
    if file.split(".")[-1] != "dat":
        raise ValueError("File must be a '.dat' file.")
    elif not os.path.isfile(file_path):
        raise ValueError("This file cannot be found, choose a file in the working directory.")
    else:
        return file


def assert_non_zero(key, value):
    if value == 0:
        raise ValueError("{} must be non-zero.".format(key))


# TODO: import Arguments function instead of defining within sim
class Arguments:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("-r", "--birth-hares", type=float, default=0.08, help="Birth rate of hares")
        parser.add_argument("-a", "--death-hares", type=float, default=0.04, help="Rate at which pumas eat hares")
        parser.add_argument("-k", "--diffusion-hares", type=float, default=0.2, help="Diffusion rate of hares")
        parser.add_argument("-b", "--birth-pumas", type=float, default=0.02, help="Birth rate of pumas")
        parser.add_argument("-m", "--death-pumas", type=float, default=0.06, help="Rate at which pumas starve")
        parser.add_argument("-l", "--diffusion-pumas", type=float, default=0.2, help="Diffusion rate of pumas")
        parser.add_argument("-dt", "--delta-t", type=float, default=0.4, help="Time step size")
        parser.add_argument("-t", "--time_step", type=int, default=10,
                            help="Number of time steps at which to output files")
        parser.add_argument("-d", "--duration", type=int, default=500,
                            help="Time to run the simulation (in time-steps)")
        parser.add_argument("-f", "--landscape-file", type=str, required=True, help="Input landscape file")
        parser.add_argument("-hs", "--hare-seed", type=int, default=1,
                            help="Random seed for initialising hare densities")
        parser.add_argument("-ps", "--puma-seed", type=int, default=1,
                            help="Random seed for initialising puma densities")
        self.args = parser.parse_args()
        self.dict = vars(self.args)


def filter_args(test_dict):
    for key, value in test_dict.items():
        if key in {'birth_hares', 'death_hares', 'diffusion_hares', 'birth_pumas', 'death_pumas', 'diffusion_pumas',
                   'delta_t'}:
            assert_non_neg_float(key, value)
        elif key in {'time_step', 'duration', 'hare_seed', 'puma_seed'}:
            assert_non_neg_int(key, value)
        elif key == 'landscape_file':
            assert_working_file(value)
        else:
            raise ValueError("The argument {} is not recognised.".format(key))
        if key in {'delta-t', 'time-step', 'duration'}:
            assert_non_zero(key, value)
    return test_dict


def simulate(args_dict):
    args_dict = filter_args(args_dict)

    hare_birth_rate = args_dict['birth_hares']
    hare_death_rate = args_dict['death_hares']
    hare_diffusion_rate = args_dict['diffusion_hares']
    puma_birth_rate = args_dict['birth_pumas']
    puma_death_rate = args_dict['death_pumas']
    puma_diffusion_rate = args_dict['diffusion_pumas']
    time_step_size = args_dict['delta_t']
    number_time_steps = args_dict['time_step']
    duration = args_dict['duration']
    landscape_file = args_dict['landscape_file']
    hare_random_seed = args_dict['hare_seed']
    puma_random_seed = args_dict['puma_seed']

    landscape_grid = Landscape(landscape_file)
    grid_width, grid_height = landscape_grid.width, landscape_grid.height
    print("Width: {} Height: {}".format(grid_width, grid_height))

    halo_landscape_grid = landscape_grid.halo_grid

    num_land_squares = landscape_grid.count_dry_squares
    print("Number of land-only squares: {}".format(num_land_squares))
    # Pre-calculate number of land neighbours of each land square.
    neighbours = landscape_grid.calculate_neighbours()

    hs = landscape_grid.generate_grid_densities(hare_random_seed)
    ps = landscape_grid.generate_grid_densities(puma_random_seed)

    # Create copies of initial maps and arrays for PPM file maps.
    # Reuse these so we don't need to create new arrays going
    # round the simulation loop.
    # TODO: Remove poor commenting, refactor below to avoid 'copy'ing hs, ps
    hs_nu = hs.copy()
    ps_nu = ps.copy()
    hcols = np.zeros((grid_height, grid_width), int)
    pcols = np.zeros((grid_height, grid_width), int)
    # TODO: Form method to perform the below 'average hs/ps'
    if num_land_squares != 0:
        ah = np.sum(hs) / num_land_squares
        ap = np.sum(ps) / num_land_squares
    else:
        ah = 0
        ap = 0
    # TODO: Refactor print statement to terminal to include 0'th iteration in loop
    print("Averages. Timestep: {} Time (s): {} Hares: {} Pumas: {}".format(0, 0, ah, ap))
    # TODO: Change so 'averages.csv' is only opened once, header written, then iterated through
    with open("averages.csv", "w") as f:
        hdr = "Timestep,Time,Hares,Pumas\n"
        f.write(hdr)
    # TODO: Refactor 'total timesteps' to be clearer
    tot_ts = int(duration / time_step_size)
    # TODO: Refactor entire loop over timesteps
    for i in range(0, tot_ts):
        if not i % number_time_steps:
            mh = np.max(hs)
            mp = np.max(ps)
            # TODO: Remove one of the definitions for average grid_height/p's
            if num_land_squares != 0:
                ah = np.sum(hs) / num_land_squares
                ap = np.sum(ps) / num_land_squares
            else:
                ah = 0
                ap = 0
            print("Averages. Timestep: {} Time (s): {} Hares: {} Pumas: {}".format(i, i * time_step_size, ah, ap))
            with open("averages.csv".format(i), "a") as f:
                f.write("{},{},{},{}\n".format(i, i * time_step_size, ah, ap))
            for x in range(1, grid_height + 1):
                for y in range(1, grid_width + 1):
                    if halo_landscape_grid[x, y]:
                        if mh != 0:
                            hcol = (hs[x, y] / mh) * 255
                        else:
                            hcol = 0
                        if mp != 0:
                            pcol = (ps[x, y] / mp) * 255
                        else:
                            pcol = 0
                        hcols[x - 1, y - 1] = hcol
                        pcols[x - 1, y - 1] = pcol
            with open("map_{:04d}.ppm".format(i), "w") as f:
                hdr = "P3\n{} {}\n{}\n".format(grid_width, x, 255)
                f.write(hdr)
                for x in range(0, grid_height):
                    for y in range(0, grid_width):
                        if halo_landscape_grid[x + 1, y + 1]:
                            f.write("{} {} {}\n".format(hcols[x, y], pcols[x, y], 0))
                        else:
                            f.write("{} {} {}\n".format(0, 0, 255))
        for x in range(1, grid_height + 1):
            for y in range(1, grid_width + 1):
                if halo_landscape_grid[x, y]:
                    hs_nu[x, y] = hs[x, y] \
                                  + time_step_size * ((hare_birth_rate * hs[x, y])
                                                      - (hare_death_rate * hs[x, y] * ps[x, y])
                                                      + hare_diffusion_rate * ((hs[x - 1, y]
                                                                                + hs[x + 1, y]
                                                                                + hs[x, y - 1]
                                                                                + hs[x, y + 1])
                                                                               - (neighbours[x, y] * hs[x, y])))
                    if hs_nu[x, y] < 0:
                        hs_nu[x, y] = 0
                    ps_nu[x, y] = ps[x, y] \
                                  + time_step_size * ((puma_birth_rate * hs[x, y] * ps[x, y])
                                                      - (puma_death_rate * ps[x, y])
                                                      + puma_diffusion_rate * ((ps[x - 1, y]
                                                                                + ps[x + 1, y]
                                                                                + ps[x, y - 1]
                                                                                + ps[x, y + 1])
                                                                               - (neighbours[x, y] * ps[x, y])))
                    if ps_nu[x, y] < 0:
                        ps_nu[x, y] = 0
        # Swap arrays for next iteration.
        hs, hs_nu = hs_nu, hs
        ps, ps_nu = ps_nu, ps


if __name__ == "__main__":
    from sim_functions import Landscape
    simulation_args = Arguments().dict
    simulate(simulation_args)

