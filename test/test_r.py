import numpy as np
import pytest

from grpc4bmi.run_server import BmiR, build_r

@pytest.fixture
def model():
    return build_r('FakeFailingRModel', 'test/fake.r')

@pytest.mark.skipif(not BmiR, reason='R and its dependencies are not installed')
class TestFakeFailingRModel:
    @pytest.mark.parametrize(
    'fn_name,fn_args',
    [
        ('get_component_name', tuple()),
        ('get_input_item_count', tuple()),
        ('get_output_item_count', tuple()),
        ('get_input_var_names', tuple()),
        ('get_output_var_names', tuple()),
        ('get_start_time', tuple()),
        ('get_end_time', tuple()),
        ('get_time_step', tuple()),
        ('get_time_units', tuple()),
        ('get_var_type', ['plate_surface__temperature']),
        ('get_var_units', ['plate_surface__temperature']),
        ('get_var_itemsize', ['plate_surface__temperature']),
        ('get_var_nbytes', ['plate_surface__temperature']),
        ('get_var_grid', ['plate_surface__temperature']),
        ('get_var_location', ['plate_surface__temperature']),
        ('get_grid_shape', [0, np.zeros((1,))]),
        ('get_grid_x', [0, np.zeros((1,))]),
        ('get_grid_y', [0, np.zeros((1,))]),
        ('get_grid_z', [0, np.zeros((1,))]),
        ('get_grid_spacing', [0, np.zeros((1,))]),
        ('get_grid_origin', [0, np.zeros((1,))]),
        ('get_grid_rank', [0]),
        ('get_grid_size', [0]),
        ('get_grid_type', [0]),
        ('initialize', ['config.ini']),
        ('update', tuple()),
        ('update_until', [2]),
        ('finalize', tuple()),
        ('get_current_time', tuple()),
        ('get_value', ['plate_surface__temperature', np.zeros((1,))]),
        ('get_value_at_indices', ['plate_surface__temperature', np.zeros((1,)), [1, 2, 3]]),
        ('set_value', ['plate_surface__temperature', np.ones((10, 20))]),
        ('set_value_at_indices', ['plate_surface__temperature', [1, 2, 3], [4, 5, 6]]),
        ('get_grid_node_count', (0,)),
        ('get_grid_edge_count', (0,)),
        ('get_grid_face_count', (0,)),
        ('get_grid_edge_nodes', (0, np.empty(0))),
        ('get_grid_face_nodes', (0, np.empty(0))),
        ('get_grid_face_edges', (0, np.empty(0))),
        ('get_grid_nodes_per_face', (42, np.empty(0))),
    ]
)
    def test_r_function_is_called(self, model: BmiR, fn_name, fn_args):
        # Every method in 'test/fake.r' executes the stop error action
        # So if no stop then no r function is called
        from rpy2.rinterface_lib.embedded import RRuntimeError
        with pytest.raises(RRuntimeError, match="Always fails"):
            fn = getattr(model, fn_name)
            fn(*fn_args)

    @pytest.mark.parametrize('fn_name,fn_args', [
        ('get_value_ptr', ['plate_surface__temperature']),
    ])
    def test_notimplemented(self, model: BmiR, fn_name, fn_args):
        with pytest.raises(NotImplementedError):
            fn = getattr(model, fn_name)
            fn(*fn_args)
        