import numpy
from heat import BmiHeat


class FlatBmiHeat(BmiHeat):
    """The BmiHeat returns multi dimensional arrays, but

    """
    def get_value_at_indices(self, var_name, dest, indices):
        val = super(FlatBmiHeat, self).get_value_at_indices(var_name, indices).flatten()
        numpy.copyto(src=val, dst=dest)
        return dest

    def set_value(self, var_name, src):
        shape = super(FlatBmiHeat, self).get_grid_shape(super(FlatBmiHeat, self).get_var_grid(var_name))
        reshaped = numpy.reshape(src, shape)
        super(FlatBmiHeat, self).set_value(var_name, reshaped)

    def get_value(self, var_name, dest):
        val = super(FlatBmiHeat, self).get_value(var_name)
        numpy.copyto(src=val.flatten(), dst=dest)
        return dest

    def get_grid_shape(self, grid_id, dest):
        val = super(FlatBmiHeat, self).get_grid_shape(grid_id)
        numpy.copyto(src=val, dst=dest)
        return dest
