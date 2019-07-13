from typing import Tuple

import numpy
import numpy as np
import pytest
from bmipy import Bmi


def write_config(p, data_fn='/data/input/PEQ_Hupsel.dat'):
    p.write_text(f"""data: {data_fn}
parameters:
  cW: 200
  cV: 4
  cG: 5.0e+6
  cQ: 10
  cS: 4
  dG0: 1250
  cD: 1500
  aS: 0.01
  st: loamy_sand
start: 367416 # 2011120000
end: 367616 # 2011120200
step: 1
centroid:
  lon: 6.65443600418465
  lat: 52.06132311280826
""")


def write_datafile(p):
    p.write_text(""""date" "P" "ETpot" "Q"
2011113023 0 0 0.0039
2011120100 0 0 0.0044
2011120101 0 0 0.0039
2011120102 0 0 0.0039
2011120103 0 0 0.0044
2011120104 0 0 0.0044
2011120105 0 0 0.0044
2011120106 0.5 0 0.0044
2011120107 0.3 0.0016 0.0044
2011120108 0 0.0078 0.0044
2011120109 0 0.0422 0.0044
2011120110 0 0.0438 0.005
2011120111 0 0.0672 0.005
2011120112 0 0.025 0.005
2011120113 0.2 0.0094 0.005
2011120114 0 0.0031 0.005
2011120115 0.4 0 0.005
2011120116 0 0 0.0055
2011120117 0 0 0.0055
2011120118 0 0 0.0055
2011120119 1 0 0.0061
2011120120 1.2 0 0.0061
2011120121 0.3 0 0.0066
2011120122 0.3 0 0.0072
2011120123 0 0 0.0078
2011120200 0 0 0.0083
2011120201 0 0 0.0089
""")


@pytest.fixture
def walrus_input(tmp_path):
    cfg = tmp_path / 'config.yml'
    write_config(cfg)
    write_datafile(tmp_path / 'PEQ_Hupsel.dat')
    return cfg


@pytest.fixture()
def walrus_input_on_extra_volume(tmp_path):
    # Have config in input dir and forcings data file on extra volume
    input_dir = tmp_path / 'input'
    input_dir.mkdir()
    cfg = input_dir / 'config.yml'
    write_config(cfg, '/forcings/PEQ_Hupsel.dat')
    extra_dir = tmp_path / 'forcings'
    extra_dir.mkdir()
    write_datafile(extra_dir / 'PEQ_Hupsel.dat')
    extra_volumes = {extra_dir: {'bind': '/forcings', 'mode': 'ro'}}
    return input_dir, extra_volumes


class SomeException(Exception):
    pass


class FailingModel(Bmi):
    def __init__(self, exc):
        self.exc = exc

    def initialize(self, filename):
        raise self.exc

    def update(self):
        raise self.exc

    def finalize(self):
        raise self.exc

    def get_component_name(self):
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

    def get_var_type(self, var_name):
        raise self.exc

    def get_var_units(self, var_name):
        raise self.exc

    def get_var_itemsize(self, var_name):
        raise self.exc

    def get_var_nbytes(self, var_name):
        raise self.exc

    def get_var_grid(self, var_name):
        raise self.exc

    def get_value(self, var_name, dest):
        raise self.exc

    def get_value_ptr(self, var_name):
        raise self.exc

    def get_value_at_indices(self, var_name, dest, indices):
        raise self.exc

    def set_value(self, var_name, src):
        raise self.exc

    def set_value_at_indices(self, var_name, indices, src):
        raise self.exc

    def get_grid_shape(self, grid_id, dest):
        raise self.exc

    def get_grid_x(self, grid_id, dest):
        raise self.exc

    def get_grid_y(self, grid_id, dest):
        raise self.exc

    def get_grid_z(self, grid_id, dest):
        raise self.exc

    def get_grid_spacing(self, grid_id, dest):
        raise self.exc

    def get_grid_origin(self, grid_id, dest):
        raise self.exc

    def get_grid_rank(self, grid_id):
        raise self.exc

    def get_grid_size(self, grid_id):
        raise self.exc

    def get_grid_type(self, grid_id):
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


class RectGridBmiModel(FailingModel):
    def __init__(self):
        super(RectGridBmiModel, self).__init__(SomeException('not used'))

    def get_grid_type(self, grid):
        return 'rectilinear'

    def get_output_var_names(self) -> Tuple[str]:
        return 'plate_surface__temperature',

    def get_grid_rank(self, grid: int) -> int:
        return 3

    def get_var_grid(self, name):
        return 0

    def get_grid_shape(self, grid: int, shape: np.ndarray) -> np.ndarray:
        numpy.copyto(src=[4, 3, 2], dst=shape)
        return shape

    def get_grid_x(self, grid: int, x: np.ndarray) -> np.ndarray:
        numpy.copyto(src=[0.1, 0.2, 0.3, 0.4], dst=x)
        return x

    def get_grid_y(self, grid: int, y: np.ndarray) -> np.ndarray:
        numpy.copyto(src=[1.1, 1.2, 1.3], dst=y)
        return y

    def get_grid_z(self, grid: int, z: np.ndarray) -> np.ndarray:
        numpy.copyto(src=[2.1, 2.2], dst=z)
        return z


class UnstructuredGridBmiModel(RectGridBmiModel):
    # Grid shape:
    #    0
    #   /|\
    #  / | \
    # 3  |  1
    #  \ |  /
    #   \| /
    #    2
    #
    def get_grid_type(self, grid):
        return 'unstructured'

    def get_grid_rank(self, grid: int) -> int:
        return 2

    def get_grid_node_count(self, grid: int) -> int:
        return 4

    def get_grid_edge_count(self, grid: int) -> int:
        return 5

    def get_grid_face_count(self, grid: int) -> int:
        return 2

    def get_grid_edge_nodes(self, grid: int, edge_nodes: np.ndarray) -> np.ndarray:
        numpy.copyto(src=(0, 3, 3, 1, 2, 1, 1, 0, 2, 0), dst=edge_nodes)
        return edge_nodes

    def get_grid_face_nodes(self, grid: int, face_nodes: np.ndarray) -> np.ndarray:
        numpy.copyto(src=(0, 3, 2, 0, 2, 1), dst=face_nodes)
        return face_nodes

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: np.ndarray) -> np.ndarray:
        numpy.copyto(src=(3, 3,), dst=nodes_per_face)
        return nodes_per_face