import numpy
from heat import BmiHeat


class FlatBmiHeat(BmiHeat):
    """The BmiHeat returns multi dimensional arrays, but

    """
    def get_value(self, var_name):
        return super(FlatBmiHeat, self).get_value(var_name).flatten()

    def get_value_at_indices(self, var_name, indices):
        return super(FlatBmiHeat, self).get_value_at_indices(var_name, indices).flatten()

    def set_value(self, var_name, src):
        shape = super(FlatBmiHeat, self).get_grid_shape(super(FlatBmiHeat, self).get_var_grid(var_name))
        reshaped = numpy.reshape(src, shape)
        super(FlatBmiHeat, self).set_value(var_name, reshaped)

