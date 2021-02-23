import unittest
import sys
import os
# Import simulate (then more)
print("IN TEST_SIM, SYS.PATH = ", sys.path)
print("IN TEST_SIM, OS.CWD = ", os.getcwd())


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class TestSimulationPredatorPrey(unittest.TestCase):

    def setUp(self):
        print("\nSetting Up ...")
        self.test_dict = {'birth_hares': 0.08, 'death_hares': 0.04, 'diffusion_hares': 0.2,
                          'birth_pumas': 0.02, 'death_pumas': 0.06, 'diffusion_pumas': 0.2,
                          'delta_t': 0.4, 'time_step': 10, 'duration': 500,
                          'landscape_file': 'map.dat', 'hare_seed': 1, 'puma_seed': 1}
        pass

    def tearDown(self):
        print("Tearing Down ...")
        pass

    # TODO: Implement test for all 3 maps in one
    # def test_maps(self):
    #     for map in

    def test_map_land(self):
        print("Testing map: map_land.dat")
        with open("test_averages/averages_default_land.csv", "r") as saved_land_averages:
            land_averages = saved_land_averages.readlines()
        self.test_dict['landscape_file'] = 'maps/map_land.dat'
        with HiddenPrints():
            simulate(self.test_dict)
        with open("averages.csv", "r") as averages:
            current_averages = averages.readlines()
        self.assertEqual(current_averages, land_averages)

    def test_map_sea(self):
        print("Testing map: map_sea.dat")
        with open("test_averages/averages_default_sea.csv", "r") as saved_sea_averages:
            sea_averages = saved_sea_averages.readlines()
        self.test_dict['landscape_file'] = 'maps/map_sea.dat'
        with HiddenPrints():
            simulate(self.test_dict)
        with open("averages.csv", "r") as averages:
            current_averages = averages.readlines()
        self.assertEqual(current_averages, sea_averages)

    def test_map_alternating(self):
        print("Testing map: map_alternating.dat")
        with open("test_averages/averages_default_alternating.csv", "r") as saved_alternating_averages:
            alternating_averages = saved_alternating_averages.readlines()
        self.test_dict['landscape_file'] = 'maps/map_alternating.dat'
        with HiddenPrints():
            simulate(self.test_dict)
        with open("averages.csv", "r") as averages:
            current_averages = averages.readlines()
        self.assertEqual(current_averages, alternating_averages)

    def test_negative_values(self):
        print("Testing negative values.")
        for key in self.test_dict.keys():
            if key != 'landscape_file':
                self.test_dict[key] = -1
                self.assertRaises(ValueError, simulate, self.test_dict)

    def test_zero_values(self):
        print("Testing zero values.")
        for key in {'delta-t', 'time-step', 'duration'}:
            self.test_dict[key] = 0
            self.assertRaises(ValueError, simulate, self.test_dict)

    def test_delta_greater_than_duration(self):
        print("Testing delta_t greater than duration")
        self.test_dict['delta_t'] = 2.0
        self.test_dict['duration'] = 1
        with HiddenPrints():
            simulate(self.test_dict)

if __name__ == '__main__':
    unittest.main()
