from .simulate_predator_prey import simulate
import sys
from argparse import ArgumentParser


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
        parser.add_argument("-d", "--duration", type=int, default=500, help="Time to run the simulation (in timesteps)")
        parser.add_argument("-f", "--landscape-file", type=str, required=True, help="Input landscape file")
        parser.add_argument("-hs", "--hare-seed", type=int, default=1,
                            help="Random seed for initialising hare densities")
        parser.add_argument("-ps", "--puma-seed", type=int, default=1,
                            help="Random seed for initialising puma densities")
        self.args = parser.parse_args()


if __name__ == "__main__":
    input_parameters = sys.argv[1:-1]
    output_file = sys.argv[-1]
    del sys.argv[-1]
    simulation_args = vars(Arguments().args)
    simulate(simulation_args)
    with open(output_file, "w") as new_output:
        with open("averages.csv", "r") as averages:
            to_write = averages.readlines()
            new_output.writelines(to_write)
