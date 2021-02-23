include config.mk

# Create averages files

## dats		: Take input .dat files containing the landscapes
.PHONY : dats
dats : map.dat maps/map_land.dat maps/map_sea.dat maps/map_alternating.dat


## 
test_averages/hare_birth_rate/negative_birth_hares.csv : map.dat
	$(SIM_AVGS_EXE) -f map.dat -r -1 test_averages/hare_birth_rate/negative_birth_hares.csv


test_averages/averages_default_alternating.csv : maps/map_alternating.dat
	$(SIM_AVGS_EXE) -f maps/map_alternating.dat test_averages/averages_default_alternating.csv

## clean	: Remove auto-generated files.
.PHONY : clean
clean :
	rm -f averages.csv map_****.ppm

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<