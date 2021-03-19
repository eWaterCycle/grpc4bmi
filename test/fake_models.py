from typing import Tuple

import numpy
import numpy as np
from basic_modeling_interface.bmi import Bmi

from grpc4bmi.constants import GRPC_MAX_MESSAGE_LENGTH


class SomeException(Exception):
    pass


class FailingModel(Bmi):
    def __init__(self, exc):
        self.exc = exc

    def initialize(self, filename):
        raise self.exc

    def update(self):
        raise self.exc

    def update_until(self, time: float) -> None:
        raise self.exc

    def finalize(self):
        raise self.exc

    def get_component_name(self):
        raise self.exc

    def get_input_item_count(self) -> int:
        raise self.exc

    def get_output_item_count(self) -> int:
        raise self.exc

    def get_input_var_names(self):
        raise self.exc

    def get_output_var_names(self):
        raise self.exc

    def get_start_time(self):
        raise self.exc

    def get_current_time(self):
        raise self.exc

    def get_end_time(self):
        raise self.exc

    def get_time_step(self):
        raise self.exc

    def get_time_units(self):
        raise self.exc

    def get_var_type(self, name):
        raise self.exc

    def get_var_units(self, name):
        raise self.exc

    def get_var_itemsize(self, name):
        raise self.exc

    def get_var_nbytes(self, name):
        raise self.exc

    def get_var_grid(self, name):
        raise self.exc

    def get_value(self, name):
        raise self.exc

    def get_value_ptr(self, name):
        raise self.exc

    def get_value_at_indices(self, name, inds):
        raise self.exc

    def set_value(self, name, src):
        raise self.exc

    def set_value_at_indices(self, name, inds, src):
        raise self.exc

    def get_grid_shape(self, grid, shape):
        raise self.exc

    def get_grid_x(self, grid, x):
        raise self.exc

    def get_grid_y(self, grid, y):
        raise self.exc

    def get_grid_z(self, grid, z):
        raise self.exc

    def get_grid_spacing(self, grid, spacing):
        raise self.exc

    def get_grid_origin(self, grid, origin):
        raise self.exc

    def get_grid_rank(self, grid):
        raise self.exc

    def get_grid_size(self, grid):
        raise self.exc

    def get_grid_type(self, grid):
        raise self.exc

    def get_var_location(self, name: str) -> str:
        raise self.exc

    def get_grid_node_count(self, grid: int) -> int:
        raise self.exc

    def get_grid_edge_count(self, grid: int) -> int:
        raise self.exc

    def get_grid_face_count(self, grid: int) -> int:
        raise self.exc

    def get_grid_edge_nodes(self, grid: int, edge_nodes: np.ndarray) -> np.ndarray:
        raise self.exc

    def get_grid_face_nodes(self, grid: int, face_nodes: np.ndarray) -> np.ndarray:
        raise self.exc

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: np.ndarray) -> np.ndarray:
        raise self.exc

    def get_grid_face_edges(self, grid: int, face_edges: np.ndarray) -> np.ndarray:
        raise self.exc


class GridModel(FailingModel):
    def __init__(self):
        super(GridModel, self).__init__(SomeException('not used'))

    def get_output_var_names(self) -> Tuple[str]:
        return 'plate_surface__temperature',

    def get_var_grid(self, name):
        return 0


class DTypeModel(GridModel):
    def __init__(self):
        super().__init__()
        self.dtype = numpy.dtype('float32')
        self.value = numpy.array((1.1, 2.2, 3.3), dtype=self.dtype)

    def get_var_type(self, name):
        return str(self.dtype)

    def get_var_itemsize(self, name):
        return self.dtype.itemsize

    def get_var_nbytes(self, name):
        return self.dtype.itemsize * self.value.size

    def get_value(self, name):
        return self.value

    def get_value_at_indices(self, name, inds):
        return self.value[inds]

    def set_value(self, name, src):
        self.value[:] = src

    def set_value_at_indices(self, name, inds, src):
        self.value[inds] = src


class HugeModel(DTypeModel):
    """Model which has value which does not fit in message body
    Can be run from command line with
    ..code-block:: bash
        run-bmi-server --path $PWD/test --name fake_models.HugeModel --port 55555
    """
    def __init__(self):
        super().__init__()
        self.dtype = numpy.dtype('float64')
        # Create value which is bigger than 4Mb
        dimension = (3 * GRPC_MAX_MESSAGE_LENGTH) // self.dtype.itemsize + 1000
        self.value = numpy.ones((dimension,), dtype=self.dtype)
