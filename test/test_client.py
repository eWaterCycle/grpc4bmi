import logging

import grpc
import numpy
import numpy.random
import pytest
from google.protobuf import any_pb2
from google.rpc import error_details_pb2, status_pb2, code_pb2
from grpc_status import rpc_status

from grpc4bmi.bmi_grpc_server import BmiServer
from grpc4bmi.bmi_grpc_client import BmiClient, RemoteException, handle_error
from grpc4bmi.reserve import reserve_values, reserve_grid_values, reserve_shape
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
    actual = client.get_value(varname, reserve_values(client, varname))
    expected = local.get_value(varname, reserve_values(local, varname))
    numpy.testing.assert_allclose(actual, expected)
    del client


def test_get_var_ptr():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    with pytest.raises(NotImplementedError):
        client.get_value_ptr(varname)


def test_get_vals_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([29, 8, 19, 81])
    result = numpy.empty(len(indices), dtype=client.get_var_type(varname))
    result = client.get_value_at_indices(varname, result, indices)
    expected = numpy.empty(len(indices), dtype=local.get_var_type(varname))
    expected = local.get_value_at_indices(varname, expected, indices)
    numpy.testing.assert_allclose(result, expected)


def test_set_var_values():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    values = 0.123 * local.get_value(varname, reserve_values(local, varname))
    client.set_value(varname, values)
    numpy.testing.assert_allclose(client.get_value(varname, reserve_values(client, varname)), values)


def test_set_values_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([1, 11, 21])
    values = numpy.array([0.123, 4.567, 8.901])
    client.set_value_at_indices(varname, indices, values)
    expected = numpy.empty(len(indices), dtype=client.get_var_type(varname))
    expected = client.get_value_at_indices(varname, expected, indices)
    numpy.testing.assert_allclose(expected, values)


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
    result = client.get_grid_shape(grid_id, reserve_grid_values(client, grid_id))
    expected = local.get_grid_shape(grid_id, reserve_grid_values(local, grid_id))
    assert result == expected


def test_get_grid_spacing():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_spacing(grid_id, reserve_grid_values(client, grid_id)) == local.get_grid_spacing(grid_id)


def test_get_grid_origin():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    assert client.get_grid_origin(grid_id, reserve_grid_values(client, grid_id)) == local.get_grid_origin(grid_id)


def test_get_grid_points():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    local_x = local.get_grid_x(grid_id, reserve_shape(local, grid_id, 0))
    local_y = local.get_grid_y(grid_id, reserve_shape(local, grid_id, 1))
    local_z = local.get_grid_z(grid_id, reserve_shape(local, grid_id, 2))
    assert numpy.array_equal(client.get_grid_x(grid_id, reserve_shape(client, grid_id, 0)), local_x)
    assert numpy.array_equal(client.get_grid_y(grid_id, reserve_shape(client, grid_id, 1)), local_y)
    assert numpy.array_equal(client.get_grid_z(grid_id, reserve_shape(client, grid_id, 2)), local_z)


class MyCall(grpc.RpcError):
    def __init__(self, message, exc, stack_entries):
        super().__init__(message)
        if stack_entries is not None:
            detail = any_pb2.Any()
            detail.Pack(
                error_details_pb2.DebugInfo(
                    stack_entries=stack_entries,
                    detail=repr(exc)
                )
            )
            status = status_pb2.Status(
                code=code_pb2.INTERNAL,
                message=str(exc),
                details=[detail]
            )
        else:
            status = status_pb2.Status(
                code=code_pb2.INTERNAL,
                message=str(exc)
            )
        self.impl = rpc_status.to_status(status)

    def trailing_metadata(self):
        return self.impl.trailing_metadata

    def code(self):
        return self.impl.code

    def details(self):
        return self.impl.details


def test_handle_error_with_stacktrace():
    exc = Exception('Some exception thrown by model on server')
    stack_entries = [
        '  File "/somewhere/on/server/model.py, line 42, in initialize\n  open(fn)',
    ]
    call = MyCall('Server error message', exc, stack_entries)

    with pytest.raises(RemoteException) as excinfo:
        handle_error(call)

        assert excinfo.value.remote_stacktrace == stack_entries
        assert str(excinfo.value) == 'Some exception thrown by model on server'
        assert excinfo.value.__cause == exc


def test_handle_error_without_stacktrace():
    exc = Exception('Some exception thrown by model on server')
    stack_entries = None
    call = MyCall('Server error message', exc, stack_entries)

    with pytest.raises(MyCall) as excinfo:
        try:
            raise call
        except MyCall:
            handle_error(call)

        assert excinfo.value == exc


class OtherCall(grpc.RpcError):
    def __init__(self, message, exc):
        super().__init__(message)
        self.exc = exc

    def trailing_metadata(self):
        return []

    def code(self):
        return code_pb2.INTERNAL

    def details(self):
        return str(self.exc)


def test_handle_error_without_status():
    exc = Exception('Some exception thrown by model on server')
    call = OtherCall('Server error message', exc)

    with pytest.raises(OtherCall) as excinfo:
        try:
            raise call
        except MyCall:
            handle_error(call)

        assert excinfo.value == call
