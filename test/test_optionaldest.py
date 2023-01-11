import numpy as np
from heat import BmiHeat
from numpy.testing import assert_allclose
import pytest

from grpc4bmi.bmi_optionaldest import OptionalDestBmi
from test.fake_models import Rect3DGridModel, UnstructuredGridBmiModel


@pytest.mark.parametrize(
    'orig_model,method_name,method_args,expected_shape',
    [
        (BmiHeat(), 'get_value', ('plate_surface__temperature',), (200,)),
        (BmiHeat(), 'get_value', ('plate_surface__temperature', np.zeros(200)), (200,)),
        (BmiHeat(), 'get_grid_shape', (0,), (2,)),
        (BmiHeat(), 'get_grid_shape', (0, np.zeros(2)), (2,)),
        (BmiHeat(), 'get_grid_spacing', (0,), (2,)),
        (BmiHeat(), 'get_grid_spacing', (0, np.zeros(2)), (2,)),
        (BmiHeat(), 'get_grid_origin', (0,), (2,)),
        (BmiHeat(), 'get_grid_origin', (0, np.zeros(2)), (2,)),
        (BmiHeat(), 'get_value_at_indices', ['plate_surface__temperature', [1, 2, 3]], (3,)),
        (Rect3DGridModel(), 'get_grid_x', [0], (4,)),
        (Rect3DGridModel(), 'get_grid_x', [0, np.zeros((4,))], (4,)),
        (Rect3DGridModel(), 'get_grid_y', [0], (3,)),
        (Rect3DGridModel(), 'get_grid_y', [0, np.zeros((3,))], (3,)),
        (Rect3DGridModel(), 'get_grid_z', [0], (2,)),        
        (Rect3DGridModel(), 'get_grid_z', [0, np.zeros((2,))], (2,)),        
        (UnstructuredGridBmiModel(), 'get_grid_edge_nodes', [0], (16,)),
        (UnstructuredGridBmiModel(), 'get_grid_edge_nodes', [0, np.zeros((16,))], (16,)),
        (UnstructuredGridBmiModel(), 'get_grid_face_edges', [0], (11,)),
        (UnstructuredGridBmiModel(), 'get_grid_face_edges', [0, np.zeros((11,))], (11,)),
        (UnstructuredGridBmiModel(), 'get_grid_face_nodes', [0], (11,)),
        (UnstructuredGridBmiModel(), 'get_grid_face_nodes', [0, np.zeros((11,))], (11,)),
        (UnstructuredGridBmiModel(), 'get_grid_nodes_per_face', [0], (3,)),        
        (UnstructuredGridBmiModel(), 'get_grid_nodes_per_face', [0, np.zeros((3,))], (3,)),        
    ]
)
def test_methods_with_optional_dest(orig_model, method_name, method_args, expected_shape):
    model = OptionalDestBmi(orig_model)
    model.initialize(None)

    method = getattr(model, method_name)
    result = method(*method_args)

    assert result.shape == expected_shape


@pytest.mark.parametrize(
    'orig_model, method_name, method_args', 
    [
        (BmiHeat(), 'update', tuple()),
        (BmiHeat(), 'update_until', [2]),
        (BmiHeat(), 'finalize', tuple()),
        (BmiHeat(), 'get_current_time', tuple()),
        (BmiHeat(), 'get_component_name', tuple()),
        (BmiHeat(), 'get_input_item_count', tuple()),
        (BmiHeat(), 'get_output_item_count', tuple()),
        (BmiHeat(), 'get_input_var_names', tuple()),
        (BmiHeat(), 'get_output_var_names', tuple()),
        (BmiHeat(), 'get_start_time', tuple()),
        (BmiHeat(), 'get_end_time', tuple()),
        (BmiHeat(), 'get_time_step', tuple()),
        (BmiHeat(), 'get_time_units', tuple()),
        (BmiHeat(), 'get_var_type', ['plate_surface__temperature']),
        (BmiHeat(), 'get_var_units', ['plate_surface__temperature']),
        (BmiHeat(), 'get_var_itemsize', ['plate_surface__temperature']),
        (BmiHeat(), 'get_var_nbytes', ['plate_surface__temperature']),
        (BmiHeat(), 'get_var_grid', ['plate_surface__temperature']),
        (BmiHeat(), 'get_var_location', ['plate_surface__temperature']),
        (BmiHeat(), 'get_grid_rank', [0]),
        (BmiHeat(), 'get_grid_size', [0]),
        (BmiHeat(), 'get_grid_type', [0]),
        (BmiHeat(), 'get_value_ptr', ['plate_surface__temperature']),
        (BmiHeat(), 'set_value', ['plate_surface__temperature', np.ones((200,))]),
        (BmiHeat(), 'set_value_at_indices', ['plate_surface__temperature', [1, 2, 3], [4, 5, 6]]),
        (UnstructuredGridBmiModel(), 'get_grid_node_count', [0]),
        (UnstructuredGridBmiModel(), 'get_grid_edge_count', [0]),
        (UnstructuredGridBmiModel(), 'get_grid_face_count', [0]),
    ]
)
def test_methods_with_no_dest(orig_model, method_name, method_args):
    model = OptionalDestBmi(orig_model)
    model.initialize(None)

    method = getattr(model, method_name)
    result = method(*method_args)

    expected = getattr(orig_model, method_name)(*method_args)
    if isinstance(result, np.ndarray):
            assert_allclose(result, expected)
    else:
        assert result == expected
