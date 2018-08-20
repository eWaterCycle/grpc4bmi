import logging

import numpy
import numpy.random
import pytest
from heat import BmiHeat

from grpc4bmi.bmi_client_subproc import BmiClientSubProcess

"""
Unit tests for the BMI client and a server running in a child process. Every test performs cross-checking with a local 
instance of the BMI heat toy model.
"""

logging.basicConfig(level=logging.DEBUG)


def make_bmi_classes(init=False):
    numpy.random.seed(0)
    client = BmiClientSubProcess("heat.BmiHeat")
    local = BmiHeat()
    if init:
        client.initialize(None)
        local.initialize(None)
    return client, local


def test_server_start():
    client, local = make_bmi_classes()
    assert client is not None
    del client


def test_component_name():
    client, local = make_bmi_classes()
    assert client.get_component_name() == local.get_component_name()
    del client


def test_varnames():
    client, local = make_bmi_classes()
    assert client.get_input_var_names() == local.get_input_var_names()
    assert client.get_output_var_names() == local.get_output_var_names()
    del client


def test_initialize():
    client, local = make_bmi_classes(True)
    assert client is not None
    client.finalize()
    del client


def test_update():
    client, local = make_bmi_classes(True)
    client.update()
    assert client is not None
    client.finalize()
    del client


def test_get_time_unit():
    client, local = make_bmi_classes()
    assert client.get_time_units() == local.get_time_units()
    client.finalize()
    del client


def test_get_time_step():
    client, local = make_bmi_classes(True)
    assert client.get_time_step() == local.get_time_step()
    client.finalize()
    del client


def test_get_current_time():
    client, local = make_bmi_classes(True)
    assert client.get_current_time() == local.get_current_time()
    client.finalize()
    del client


def test_get_updated_time():
    client, local = make_bmi_classes(True)
    client.update()
    assert client.get_current_time() != local.get_current_time()
    local.update()
    assert client.get_current_time() == local.get_current_time()
    client.finalize()
    del client


def test_get_start_end_time():
    client, local = make_bmi_classes(True)
    assert client.get_start_time() == local.get_start_time()
    assert client.get_end_time() == local.get_end_time()
    client.finalize()
    del client


def test_get_var_grid():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    assert client.get_var_grid(varname) == local.get_var_grid(varname)
    del client


def test_get_var_type():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    assert client.get_var_type(varname) == local.get_var_type(varname)
    del client


def test_get_var_units():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    assert client.get_var_units(varname) == local.get_var_units(varname)
    del client


def test_get_var_nbytes():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    assert client.get_var_nbytes(varname) == local.get_var_nbytes(varname)
    del client


def test_get_var_values():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    server_values = client.get_value(varname)
    local.set_value(varname, server_values)
    client.update()
    local.update()
    assert numpy.array_equal(client.get_value(varname), local.get_value(varname))
    del client


def test_get_var_ptr():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    with pytest.raises(NotImplementedError):
        client.get_value_ref(varname)
    del client


def test_get_vals_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    server_values = client.get_value(varname)
    local.set_value(varname, server_values)
    client.update()
    local.update()
    indices = numpy.array([29, 8, 19, 81])
    assert numpy.array_equal(client.get_value_at_indices(varname, indices),
                             local.get_value_at_indices(varname, indices))
    del client


def test_get_vals_indices_2d():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    server_values = client.get_value(varname)
    local.set_value(varname, server_values)
    client.update()
    local.update()
    indices = numpy.array([[0, 1], [1, 0], [2, 2]])
    assert numpy.array_equal(client.get_value_at_indices(varname, indices),
                             local.get_value_at_indices(varname, indices))
    del client


def test_set_var_values():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    values = 0.123 * local.get_value(varname)
    client.set_value(varname, values)
    assert numpy.array_equal(client.get_value(varname), values)
    del client


def test_set_values_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([1, 11, 21])
    values = numpy.array([0.123, 4.567, 8.901])
    client.set_value_at_indices(varname, indices, values)
    assert numpy.array_equal(client.get_value_at_indices(varname, indices), values)
    del client


def test_get_grid_size():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_size(grid_id) == local.get_grid_size(grid_id)
    del client


def test_get_grid_rank():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_rank(grid_id) == local.get_grid_rank(grid_id)
    del client


def test_get_grid_type():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_type(grid_id) == local.get_grid_type(grid_id)
    del client


def test_get_grid_shape():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_shape(grid_id) == local.get_grid_shape(grid_id)
    del client


def test_get_grid_spacing():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_spacing(grid_id) == local.get_grid_spacing(grid_id)
    del client


def test_get_grid_offset():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_offset = () if local.get_grid_offset(grid_id) is None else local.get_grid_offset(grid_id)
    assert client.get_grid_offset(grid_id) == local_offset
    del client


def test_get_grid_origin():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_origin(grid_id) == local.get_grid_origin(grid_id)
    del client


def test_get_grid_connectivity():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_connect = [] if local.get_grid_connectivity(grid_id) is None else local.get_grid_connectivity(grid_id)
    assert client.get_grid_connectivity(grid_id) == local_connect
    del client


def test_get_grid_points():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_x = [] if local.get_grid_x(grid_id) is None else local.get_grid_x(grid_id)
    local_y = [] if local.get_grid_y(grid_id) is None else local.get_grid_y(grid_id)
    local_z = [] if local.get_grid_z(grid_id) is None else local.get_grid_z(grid_id)
    assert client.get_grid_x(grid_id) == local_x
    assert client.get_grid_y(grid_id) == local_y
    assert client.get_grid_z(grid_id) == local_z
    del client
