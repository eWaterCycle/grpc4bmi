import numpy
from heat import BmiHeat

from grpc4bmi.reserve import reserve_values, reserve_values_at_indices, reserve_grid_shape, reserve_grid_padding


class FlatBmiHeat(BmiHeat):
    """The BmiHeat returns multi dimensional arrays, but grpc interface uses flat arrays

    """
    def set_value(self, var_name, src):
        grid_id = super(FlatBmiHeat, self).get_var_grid(var_name)
        shape = super(FlatBmiHeat, self).get_grid_shape(grid_id, reserve_grid_shape(self, grid_id))
        reshaped = numpy.reshape(src, shape)
        super(FlatBmiHeat, self).set_value(var_name, reshaped)


class FlatLegacyBmiHeat(BmiHeat):
    """BMI implementing interface defined in basic-modeling-interface 0.2

    https://pypi.org/project/basic-modeling-interface/0.2/

    """
    def set_value(self, var_name, src):
        grid_id = super(FlatLegacyBmiHeat, self).get_var_grid(var_name)
        shape = super(FlatLegacyBmiHeat, self).get_grid_shape(grid_id, reserve_grid_shape(self, grid_id))
        reshaped = numpy.reshape(src, shape)
        super(FlatLegacyBmiHeat, self).set_value(var_name, reshaped)

    def get_value(self, var_name):
        dest = reserve_values(self, var_name)
        val = super(FlatLegacyBmiHeat, self).get_value(var_name, dest)
        return val.flatten()

    def get_value_at_indices(self, var_name, indices):
        dest = reserve_values_at_indices(self, var_name, indices)
        return super(FlatLegacyBmiHeat, self).get_value_at_indices(var_name, dest, indices).flatten()

    def get_grid_shape(self, grid_id):
        dest = reserve_grid_shape(self, grid_id)
        return super(FlatLegacyBmiHeat, self).get_grid_shape(grid_id, dest)

    def get_grid_spacing(self, grid_id):
        dest = reserve_grid_padding(self, grid_id)
        return super(FlatLegacyBmiHeat, self).get_grid_spacing(grid_id, dest)

    def get_grid_origin(self, grid_id):
        dest = reserve_grid_padding(self, grid_id)
        return super(FlatLegacyBmiHeat, self).get_grid_origin(grid_id, dest)
