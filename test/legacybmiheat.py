import numpy as np
from heat import BmiHeat

from grpc4bmi.reserve import reserve_grid_padding, reserve_grid_shape, reserve_values, reserve_values_at_indices

class LegacyBmiHeat(BmiHeat):
    """BMI implementing interface defined in basic-modeling-interface 0.2

    https://pypi.org/project/basic-modeling-interface/0.2/

    """
    def get_value(self, var_name):
        dest = reserve_values(self, var_name)
        super(LegacyBmiHeat, self).get_value(var_name, dest)
        return dest

    def get_value_at_indices(self, var_name, indices):
        dest = reserve_values_at_indices(self, var_name, indices)
        super(LegacyBmiHeat, self).get_value_at_indices(var_name, dest, indices)
        return dest

    def get_grid_shape(self, grid):
        dest = reserve_grid_shape(self, grid)
        super(LegacyBmiHeat, self).get_grid_shape(grid, dest)
        return dest

    def get_grid_spacing(self, grid):
        dest = reserve_grid_padding(self, grid)
        super(LegacyBmiHeat, self).get_grid_spacing(grid, dest)
        return dest

    def get_grid_origin(self, grid):
        dest = reserve_grid_padding(self, grid)
        super(LegacyBmiHeat, self).get_grid_origin(grid, dest)
        return dest
