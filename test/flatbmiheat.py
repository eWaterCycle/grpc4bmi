import numpy
from heat import BmiHeat


class FlatBmiHeat(BmiHeat):
    """The BmiHeat returns multi dimensional arrays, but grpc interface uses flat arrays

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

    def get_grid_shape(self, grid_id, dest=None):
        val = super(FlatBmiHeat, self).get_grid_shape(grid_id)
        if dest is None:
            return numpy.array(val)
        numpy.copyto(src=val, dst=dest)
        return dest

    def get_grid_spacing(self, grid_id, dest):
        val = super(FlatBmiHeat, self).get_grid_spacing(grid_id)
        numpy.copyto(src=val, dst=dest)
        return dest

    def get_grid_origin(self, grid_id, dest):
        val = super(FlatBmiHeat, self).get_grid_origin(grid_id)
        numpy.copyto(src=val, dst=dest)
        return dest


class FlatLegacyBmiHeat(BmiHeat):
    """BMI implementing interface defined in basic-modeling-interface 0.2

    https://pypi.org/project/basic-modeling-interface/0.2/

    """
    def set_value(self, var_name, src):
        shape = super(FlatLegacyBmiHeat, self).get_grid_shape(super(FlatLegacyBmiHeat, self).get_var_grid(var_name))
        reshaped = numpy.reshape(src, shape)
        super(FlatLegacyBmiHeat, self).set_value(var_name, reshaped)

    def get_value(self, var_name):
        val = super(FlatLegacyBmiHeat, self).get_value(var_name)
        return val.flatten()

    def get_value_at_indices(self, var_name, indices):
        return super(FlatLegacyBmiHeat, self).get_value_at_indices(var_name, indices).flatten()
