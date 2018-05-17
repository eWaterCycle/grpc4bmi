import logging

import numpy
import numpy.random
import pytest
from heat import BmiHeat

from grpc4bmi.bmi_grpc_server import BmiServer

logging.basicConfig(level=logging.DEBUG)


class RequestStub(object):
    def __init__(self):
        self.config_file = ""


def make_string(obj):
    return '' if obj is None else str(obj)


def make_bmi_classes(init=False):
    server, local = BmiServer("BmiHeat", "heat"), BmiHeat()
    local = BmiHeat()
    if init:
        req = RequestStub()
        numpy.random.seed(0)
        server.initialize(req, None)
        numpy.random.seed(0)
        local.initialize(None)
    return server, local


def test_server_start():
    server, local = make_bmi_classes()
    assert server is not None
    del server


def test_component_name():
    server, local = make_bmi_classes()
    assert server.getComponentName(None, None).name == local.get_component_name()
    del server


def test_varname_counts():
    server, local = make_bmi_classes()
    assert server.getInputVarNameCount(None, None).count == len(local.get_input_var_names())
    assert server.getOutputVarNameCount(None, None).count == len(local.get_output_var_names())
    del server


def test_varnames():
    server, local = make_bmi_classes()
    assert server.getInputVarNames(None, None).names == list(local.get_input_var_names())
    assert server.getOutputVarNames(None, None).names == list(local.get_output_var_names())
    del server


def test_initialize():
    server, local = make_bmi_classes(True)
    assert server is not None
    server.finalize(None, None)
    del server


def test_update():
    server, local = make_bmi_classes(True)
    server.update(None, None)
    assert server is not None
    server.finalize(None, None)
    del server


def test_get_time_unit():
    server, local = make_bmi_classes()
    assert server.getTimeUnits(None, None).units == make_string(local.get_time_units())
    server.finalize(None, None)
    del server


def test_get_time_step():
    server, local = make_bmi_classes(True)
    assert server.getTimeStep(None, None).interval == local.get_time_step()
    server.finalize(None, None)
    del server


def test_get_current_time():
    server, local = make_bmi_classes(True)
    assert server.getCurrentTime(None, None).time == local.get_current_time()
    server.finalize(None, None)
    del server


def test_get_updated_time():
    server, local = make_bmi_classes(True)
    server.update(None, None)
    assert server.getCurrentTime(None, None).time != local.get_current_time()
    local.update()
    assert server.getCurrentTime(None, None).time == local.get_current_time()
    server.finalize(None, None)
    del server


def test_get_start_end_time():
    server, local = make_bmi_classes(True)
    assert server.getStartTime(None, None).time == local.get_start_time()
    assert server.getEndTime(None, None).time == local.get_end_time()
    server.finalize(None, None)
    del server


def test_get_var_grid():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    assert server.getVarGrid(request, None).grid_id == local.get_var_grid(varname)
    del server


def test_get_var_type():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    assert server.getVarType(request, None).type == local.get_var_type(varname)
    del server


def test_get_var_units():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    assert server.getVarUnits(request, None).units == local.get_var_units(varname)
    del server


def test_get_var_nbytes():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    assert server.getVarNBytes(request, None).nbytes == local.get_var_nbytes(varname)
    del server


def test_get_var_values():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    values = local.get_value(varname)
    assert tuple(server.getValue(request, None).shape) == values.shape
    assert numpy.array_equal(numpy.reshape(server.getValue(request, None).values_double, values.shape), values)


def test_get_var_ptr():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    with pytest.raises(NotImplementedError):
        server.getValuePtr(request, None)


# def test_get_vals_indices():
#     server, local = make_bmi_classes(True)
#     request = RequestStub()
#     varname = local.get_output_var_names()[0]
#     setattr(request, "name", varname)
#     values = local.get_value(varname)
#     assert tuple(server.getValue(request, None).shape) == values.shape
#     assert numpy.array_equal(numpy.reshape(server.getValue(request, None).values_double, values.shape), values)
