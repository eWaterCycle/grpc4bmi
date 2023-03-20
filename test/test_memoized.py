from unittest.mock import patch

from heat import BmiHeat
import numpy as np
from numpy.testing import assert_allclose
import pytest

from grpc4bmi.bmi_memoized import MemoizedBmi
from test.fake_models import Rect3DGridModel, UnstructuredGridBmiModel


@pytest.mark.parametrize(
    'model,mut_name,mut_args',
    [
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
        (BmiHeat(), 'get_grid_shape', [0, np.zeros((2,))]),
        (BmiHeat(), 'get_grid_spacing', [0, np.zeros((2,))]),
        (BmiHeat(), 'get_grid_origin', [0, np.zeros((2,))]),
        (Rect3DGridModel(), 'get_grid_x', [0, np.zeros((4,))]),
        (Rect3DGridModel(), 'get_grid_y', [0, np.zeros((3,))]),
        (Rect3DGridModel(), 'get_grid_z', [0, np.zeros((2,))]),
        (UnstructuredGridBmiModel(), 'get_grid_node_count', [0]),
        (UnstructuredGridBmiModel(), 'get_grid_edge_count', [0]),
        (UnstructuredGridBmiModel(), 'get_grid_face_count', [0]),
        (UnstructuredGridBmiModel(), 'get_grid_edge_nodes', [0, np.zeros((16,))]),
        (UnstructuredGridBmiModel(), 'get_grid_face_edges', [0, np.zeros((11,))]),
        (UnstructuredGridBmiModel(), 'get_grid_face_nodes', [0, np.zeros((11,))]),
        (UnstructuredGridBmiModel(), 'get_grid_nodes_per_face', [0, np.zeros((3,))]),
    ]
)
def test_memoized_methods(model, mut_name, mut_args):
    with patch.object(model, mut_name, wraps=getattr(model, mut_name)) as mock_method:
        client = MemoizedBmi(model)
        client.initialize(None)
        mot = getattr(client, mut_name)

        first_result = mot(*mut_args)
        second_result = mot(*mut_args)

        if isinstance(first_result, np.ndarray):
            assert_allclose(first_result, second_result)
        else:
            assert first_result == second_result
        assert mock_method.call_count == 1


@pytest.mark.parametrize(
    'mut_name,mut_args',
    [
        ('update', tuple()),
        ('update_until', [2]),
        ('finalize', tuple()),
        ('get_current_time', tuple()),
        ('get_value', ['plate_surface__temperature', np.zeros((200,))]),
        ('get_value_ptr', ['plate_surface__temperature']),
        ('get_value_at_indices', ['plate_surface__temperature', np.array([0, 0, 0]), [1, 2, 3]]),
        ('set_value', ['plate_surface__temperature', np.ones((200,))]),
        ('set_value_at_indices', ['plate_surface__temperature', [1, 2, 3], [4, 5, 6]]),
    ]
)
def test_nonmemoized_methods(mut_name, mut_args):
    model = BmiHeat()
    with patch.object(model, mut_name, wraps=getattr(model, mut_name)) as mock_method:
        client = MemoizedBmi(model)
        client.initialize(None)
        mot = getattr(client, mut_name)

        mot(*mut_args)
        mot(*mut_args)

        assert mock_method.call_count == 2


def test_initialize_clears_cache():
    model = BmiHeat()
    client = MemoizedBmi(model)
    client.initialize(None)
    # Fill cache
    client.get_start_time()
    # Clear cache
    client.initialize(None)

    with patch.object(model, 'get_start_time', wraps=model.get_start_time) as mock_method:
        client.get_start_time()
        assert mock_method.call_count == 1
