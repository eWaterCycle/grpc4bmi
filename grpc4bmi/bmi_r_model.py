from basic_modeling_interface import Bmi
import rpy2.robjects as robjects
import numpy as np


def build_model(class_name, source_fn=None):
    robjects.r('''
        build_model = function(class, source_fn=NULL) {
            if (!is.null(source_fn)) {
                source(source_fn)
            }
            return(get(class)$new())
        }
    ''')
    return robjects.r['build_model'](class_name, source_fn)


class BmiR(Bmi):
    """Python Wrapper of a R based sub class of bmi::AbstractBmi"""
    def __init__(self, class_name, source_fn=None):
        self.model = build_model(class_name, source_fn)

    # base
    def initialize(self, filename):
        self.model['bmi_initialize'](filename)

    def update(self):
        self.model['update']()

    def update_until(self, time):
        self.model['updateUntil'](time)

    def update_fraq(self, time_frac):
        self.model['updateFrac'](time_frac)

    def finalize(self):
        self.model['bmi_finalize']()

    # info
    def get_component_name(self):
        return self.model['getComponentName']()[0]

    def get_input_var_names(self):
        return self.model['getInputVarNames']()

    def get_output_var_names(self):
        return self.model['getOutputVarNames']()

    # time
    def get_start_time(self):
        return self.model['getStartTime']()[0]

    def get_current_time(self):
        return self.model['getCurrentTime']()[0]

    def get_end_time(self):
        return self.model['getEndTime']()[0]

    def get_time_step(self):
        return self.model['getTimeStep']()[0]

    def get_time_units(self):
        return self.model['getTimeUnits']()[0]

    # vars
    def get_var_type(self, var_name):
        return self.model['getVarType'](var_name)[0]

    def get_var_units(self, var_name):
        return self.model['getVarUnits'](var_name)[0]

    def get_var_itemsize(self, var_name):
        return self.model['getVarItemSize'](var_name)[0]

    def get_var_nbytes(self, var_name):
        return self.model['getVarNBytes'](var_name)[0]

    def get_var_grid(self, var_name):
        return self.model['getVarGrid'](var_name)[0]

    # getter
    def get_value(self, var_name):
        val = self.model['getValue'](var_name)
        return np.array(val)

    def get_value_at_indices(self, var_name, indices):
        rindices = robjects.IntVector(indices)
        val = self.model['getValueAtIndices'](var_name, rindices)
        return np.array(val)

    # setter
    def set_value(self, var_name, src):
        val = np.array(src)
        if val.dtype == np.int32:
            rsrc = robjects.IntVector(val)
        else:
            rsrc = robjects.FloatVector(val)
        self.model['setValue'](var_name, rsrc)

    def set_value_at_indices(self, var_name, indices, src):
        val = np.array(src)
        if val.dtype == np.int32:
            rsrc = robjects.IntVector(val)
        else:
            rsrc = robjects.FloatVector(val)
        rindices = robjects.IntVector(indices)
        self.model['setValueAtIndices'](var_name, rindices, rsrc)

    # grid
    def get_grid_rank(self, grid_id):
        return self.model['getGridRank'](grid_id)[0]

    def get_grid_size(self, grid_id):
        return self.model['getGridSize'](grid_id)[0]

    def get_grid_type(self, grid_id):
        return self.model['getGridType'](grid_id)[0]

    def get_grid_shape(self, grid_id):
        return np.array(self.model['getGridShape'](grid_id))

    def get_grid_x(self, grid_id):
        return np.array(self.model['getGridX'](grid_id))

    def get_grid_y(self, grid_id):
        return np.array(self.model['getGridY'](grid_id))

    def get_grid_z(self, grid_id):
        return np.array(self.model['getGridZ'](grid_id))

    def get_grid_spacing(self, grid_id):
        return np.array(self.model['getGridSpacing'](grid_id))

    def get_grid_origin(self, grid_id):
        return np.array(self.model['getGridOrigin'](grid_id))

    def get_grid_connectivity(self, grid_id):
        return np.array(self.model['getGridConnectivity'](grid_id))

    def get_grid_offset(self, grid_id):
        return np.array(self.model['getGridOffset'](grid_id))
