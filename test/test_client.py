import logging

import numpy
import numpy.random
import pytest

from grpc4bmi.bmi_grpc_server import BmiServer
from grpc4bmi.bmi_grpc_client import BmiClient
from test.flatbmiheat import FlatBmiHeat

logging.basicConfig(level=logging.DEBUG)

"""
Unit tests for the BMI client class. Every test performs cross-checking with a local instance of the BMI heat toy model.
"""


class ServerWrapper(object):

    def __init__(self, server):
        self.server = server

    def __getattr__(self, item):
        orig_attr = self.server.__getattribute__(item)
        if callable(orig_attr):
            def add_context(*args, **kwargs):
                kwargs["context"] = None
                return orig_attr(*args, **kwargs)

            return add_context
        return orig_attr


def make_bmi_classes(init=False):
    client = BmiClient(stub=ServerWrapper(BmiServer(FlatBmiHeat())))
    local = FlatBmiHeat()
    if init:
        numpy.random.seed(0)
        client.initialize(None)
        numpy.random.seed(0)
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


def test_initialize_with_nonstring():
    client, local = make_bmi_classes(False)
    assert client is not None
    with pytest.raises(TypeError, match='got int instead'):
        client.initialize(42)
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
    actual = client.get_value(varname)
    desired = local.get_value(varname)
    numpy.testing.assert_allclose(actual, desired)
    del client


def test_get_var_ptr():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    with pytest.raises(NotImplementedError):
        client.get_value_ref(varname)


def test_get_vals_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([29, 8, 19, 81])
    numpy.testing.assert_allclose(client.get_value_at_indices(varname, indices),
                                  local.get_value_at_indices(varname, indices))


def test_get_vals_indices_2d():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([[0, 1], [1, 0], [2, 2]])
    numpy.testing.assert_allclose(client.get_value_at_indices(varname, indices),
                                  local.get_value_at_indices(varname, indices))


def test_set_var_values():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    values = 0.123 * local.get_value(varname)
    client.set_value(varname, values)
    numpy.testing.assert_allclose(client.get_value(varname), values)


def test_set_values_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([1, 11, 21])
    values = numpy.array([0.123, 4.567, 8.901])
    client.set_value_at_indices(varname, indices, values)
    numpy.testing.assert_allclose(client.get_value_at_indices(varname, indices), values)


def test_get_grid_size():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_size(grid_id) == local.get_grid_size(grid_id)


def test_get_grid_rank():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_rank(grid_id) == local.get_grid_rank(grid_id)


def test_get_grid_type():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_type(grid_id) == local.get_grid_type(grid_id)


def test_get_grid_shape():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_shape(grid_id) == local.get_grid_shape(grid_id)


def test_get_grid_spacing():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_spacing(grid_id) == local.get_grid_spacing(grid_id)


def test_get_grid_offset():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_offset = () if local.get_grid_offset(grid_id) is None else local.get_grid_offset(grid_id)
    assert client.get_grid_offset(grid_id) == local_offset


def test_get_grid_origin():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_origin(grid_id) == local.get_grid_origin(grid_id)


def test_get_grid_connectivity():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_connect = [] if local.get_grid_connectivity(grid_id) is None else local.get_grid_connectivity(grid_id)
    assert client.get_grid_connectivity(grid_id) == local_connect


def test_get_grid_points():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_x = [] if local.get_grid_x(grid_id) is None else numpy.array(local.get_grid_x(grid_id))
    local_y = [] if local.get_grid_y(grid_id) is None else numpy.array(local.get_grid_y(grid_id))
    local_z = [] if local.get_grid_z(grid_id) is None else numpy.array(local.get_grid_z(grid_id))
    assert numpy.array_equal(client.get_grid_x(grid_id), local_x)
    assert numpy.array_equal(client.get_grid_y(grid_id), local_y)
    assert numpy.array_equal(client.get_grid_z(grid_id), local_z)


class TestCreateGrpcChannel:
    def test_defaults(self):
        with BmiClient.create_grpc_channel() as channel:
            target = channel._channel.target()
            assert target == b'localhost:50051'

    def test_custom(self):
        with BmiClient.create_grpc_channel(51234, 'somehost') as channel:
            target = channel._channel.target()
            assert target == b'somehost:51234'

    def test_same_port_twice(self):
        port = 51235
        with BmiClient.create_grpc_channel(port) as channel1, BmiClient.create_grpc_channel(port) as channel2:
            assert channel1._channel.target() == b'localhost:51235'
            assert channel2._channel.target() == b'localhost:51235'
