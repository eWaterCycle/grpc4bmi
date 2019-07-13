from bmipy import Bmi
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
    """Python Wrapper of a R based sub class of bmi::AbstractBmi .

    AbstractBmi is available in https://github.com/eWaterCycle/bmi-r repo.

    Args:
        class_name (str): Name of R class which extends bmi::AbstractBmi
        source_fn (str): R file which contains `class_name` class
    """
    def __init__(self, class_name, source_fn=None):
        self.model = build_model(class_name, source_fn)

    # base
    def initialize(self, filename):
        self.model['bmi_initialize'](filename)

    def update(self):
        self.model['update']()

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
    def get_var_type(self, name):
        return self.model['getVarType'](name)[0]

    def get_var_units(self, name):
        return self.model['getVarUnits'](name)[0]

    def get_var_itemsize(self, name):
        return self.model['getVarItemSize'](name)[0]

    def get_var_nbytes(self, name):
        return self.model['getVarNBytes'](name)[0]

    def get_var_grid(self, name):
        return self.model['getVarGrid'](name)[0]

    def get_var_location(self, name: str) -> str:
        return self.model['getVarLocation'](name)[0]

    # getter
    def get_value(self, name, dest):
        val = self.model['getValue'](name)
        np.copyto(src=val, dst=dest)
        return dest

    def get_value_at_indices(self, name, dest, indices):
        rindices = robjects.IntVector(indices)
        val = self.model['getValueAtIndices'](name, rindices)
        np.copyto(src=val, dst=dest)
        return dest

    def get_value_ptr(self, name):
        msg = 'Unable to implement get_value_ptr(), not possible to pass pointer between R and Python'
        raise NotImplementedError(msg)

    # setter
    def set_value(self, name, src):
        val = np.array(src)
        if val.dtype == np.int32:
            rsrc = robjects.IntVector(val)
        else:
            rsrc = robjects.FloatVector(val)
        self.model['setValue'](name, rsrc)

    def set_value_at_indices(self, name, indices, src):
        val = np.array(src)
        if val.dtype == np.int32:
            rsrc = robjects.IntVector(val)
        else:
            rsrc = robjects.FloatVector(val)
        rindices = robjects.IntVector(indices)
        self.model['setValueAtIndices'](name, rindices, rsrc)

    # grid
    def get_grid_rank(self, grid):
        return self.model['getGridRank'](grid)[0]

    def get_grid_size(self, grid):
        return self.model['getGridSize'](grid)[0]

    def get_grid_type(self, grid):
        return self.model['getGridType'](grid)[0]

    def get_grid_shape(self, grid, shape):
        val = self.model['getGridShape'](grid)
        np.copyto(src=val, dst=shape)
        return shape

    def get_grid_x(self, grid, x):
        val = np.array(self.model['getGridX'](grid))
        np.copyto(src=val, dst=x)
        return x

    def get_grid_y(self, grid, y):
        val = np.array(self.model['getGridY'](grid))
        np.copyto(src=val, dst=y)
        return y

    def get_grid_z(self, grid, z):
        val = np.array(self.model['getGridZ'](grid))
        np.copyto(src=val, dst=z)
        return z

    def get_grid_spacing(self, grid, spacing):
        val = np.array(self.model['getGridSpacing'](grid))
        np.copyto(src=val, dst=spacing)
        return spacing

    def get_grid_origin(self, grid, origin):
        val = np.array(self.model['getGridOrigin'](grid))
        np.copyto(src=val, dst=origin)
        return origin

    def get_grid_node_count(self, grid):
        return self.model['getGridNodeCount'](grid)[0]

    def get_grid_edge_count(self, grid):
        return self.model['getGridEdgeCount'](grid)[0]

    def get_grid_face_count(self, grid):
        return self.model['getGridFaceCount'](grid)[0]

    def get_grid_edge_nodes(self, grid, edge_nodes):
        result = self.model['getGridEdgeNodes'](grid)
        np.copyto(src=result, dst=edge_nodes)
        return edge_nodes

    def get_grid_face_nodes(self, grid, face_nodes):
        result = self.model['getGridFaceNodes'](grid)
        np.copyto(src=result, dst=face_nodes)
        return face_nodes

    def get_grid_nodes_per_face(self, grid, edge_nodes):
        result = self.model['getGridNodesPerFace'](grid)
        np.copyto(src=result, dst=edge_nodes)
        return edge_nodes
