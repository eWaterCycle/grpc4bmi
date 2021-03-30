from unittest.mock import patch

import numpy as np
import pytest

from grpc4bmi.bmi_memoized import MemoizedBmi
from test.flatbmiheat import FlatBmiHeat


@pytest.mark.parametrize(
    'mut_name,mut_args',
    [
        ('get_component_name', tuple()),
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
        ('get_grid_shape', [0]),
        ('get_grid_x', [0]),
        ('get_grid_y', [0]),
        ('get_grid_z', [0]),
        ('get_grid_spacing', [0]),
        ('get_grid_origin', [0]),
        ('get_grid_connectivity', [0]),
        ('get_grid_offset', [0]),
        ('get_grid_rank', [0]),
        ('get_grid_size', [0]),
        ('get_grid_type', [0]),
    ]
)
def test_memoized_methods(mut_name, mut_args):
    model = FlatBmiHeat()
    with patch.object(model, mut_name, wraps=getattr(model, mut_name)) as mock_method:
        client = MemoizedBmi(model)
        client.initialize(None)
        mot = getattr(client, mut_name)

        first_result = mot(*mut_args)
        second_result = mot(*mut_args)

        assert first_result == second_result
        assert mock_method.call_count == 1


@pytest.mark.parametrize(
    'mut_name,mut_args',
    [
        ('update', tuple()),
        ('update_until', [2]),
        ('update_frac', [0.5]),
        ('finalize', tuple()),
        ('get_current_time', tuple()),
        ('get_value', ['plate_surface__temperature']),
        ('get_value_ref', ['plate_surface__temperature']),
        ('get_value_at_indices', ['plate_surface__temperature', [1, 2, 3]]),
        ('set_value', ['plate_surface__temperature', np.ones((10, 20))]),
        ('set_value_at_indices', ['plate_surface__temperature', [1, 2, 3], [4, 5, 6]]),
    ]
)
def test_nonmemoized_methods(mut_name, mut_args):
    model = FlatBmiHeat()
    with patch.object(model, mut_name, wraps=getattr(model, mut_name)) as mock_method:
        client = MemoizedBmi(model)
        client.initialize(None)
        mot = getattr(client, mut_name)

        mot(*mut_args)
        mot(*mut_args)

        assert mock_method.call_count == 2


def test_initialize_clears_cache():
    model = FlatBmiHeat()
    client = MemoizedBmi(model)
    client.initialize(None)
    # Fill cache
    client.get_start_time()
    # Clear cache
    client.initialize(None)

    with patch.object(model, 'get_start_time', wraps=model.get_start_time) as mock_method:
        client.get_start_time()
        assert mock_method.call_count == 1
