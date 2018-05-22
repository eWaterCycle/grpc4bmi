import logging

import numpy
import numpy.random
import pytest
from heat import BmiHeat

from grpc4bmi.bmi_grpc_server import BmiServer

"""
Unit tests for the BMI server class. Every test performs cross-checking with a local instance of the BMI heat toy model.
"""

logging.basicConfig(level=logging.DEBUG)


class RequestStub(object):
    def __init__(self):
        self.config_file = ""


def make_string(obj):
    return '' if obj is None else str(obj)


def make_list(obj):
    if obj is list:
        return obj
    if obj is None:
        return []
    return [obj]


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


def test_get_vals_indices():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    indices = numpy.array([29, 8, 19, 81])
    setattr(request, "name", varname)
    setattr(request, "indices", indices.flatten())
    setattr(request, "index_size", 1)
    values = local.get_value_at_indices(varname, indices)
    assert numpy.array_equal(server.getValueAtIndices(request, None).values_double, values.flatten())


def test_get_vals_indices_2d():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    indices = numpy.array([[0, 1], [1, 0], [2, 2]])
    setattr(request, "name", varname)
    setattr(request, "indices", indices.flatten())
    setattr(request, "index_size", 2)
    values = local.get_value_at_indices(varname, indices)
    assert numpy.array_equal(server.getValueAtIndices(request, None).values_double, values.flatten())


def test_set_var_values():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    values = 0.123 * local.get_value(varname)
    setattr(request, "name", varname)
    setattr(request, "values_double", values.flatten())
    setattr(request, "values_float", [])
    setattr(request, "values_int", [])
    setattr(request, "shape", values.shape)
    server.setValue(request, None)
    delattr(request, "values_double")
    delattr(request, "values_float")
    delattr(request, "values_int")
    delattr(request, "shape")
    response = server.getValue(request, None)
    values_copy = numpy.reshape(response.values_double, response.shape)
    assert numpy.array_equal(values, values_copy)


def test_set_values_indices():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    indices = numpy.array([1, 11, 21])
    values = numpy.array([0.123, 4.567, 8.901])
    setattr(request, "name", varname)
    setattr(request, "values_double", values.flatten())
    setattr(request, "values_float", [])
    setattr(request, "values_int", [])
    setattr(request, "indices", indices.flatten())
    setattr(request, "index_size", 1)
    server.setValueAtIndices(request, None)
    delattr(request, "values_double")
    delattr(request, "values_float")
    delattr(request, "values_int")
    response = server.getValueAtIndices(request, None)
    values_copy = numpy.array(response.values_double)
    assert numpy.array_equal(values, values_copy)


def test_get_grid_size():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert server.getGridSize(request, None).size == local.get_grid_size(grid_id)


def test_get_grid_rank():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert server.getGridRank(request, None).rank == local.get_grid_rank(grid_id)


def test_get_grid_type():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert server.getGridType(request, None).type == local.get_grid_type(grid_id)


def test_get_grid_shape():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert tuple(server.getGridShape(request, None).shape) == local.get_grid_shape(grid_id)


def test_get_grid_spacing():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert tuple(server.getGridSpacing(request, None).spacing) == local.get_grid_spacing(grid_id)


def test_get_grid_origin():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert tuple(server.getGridOrigin(request, None).origin) == local.get_grid_origin(grid_id)


def test_get_grid_points():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert server.getGridX(request, None).coordinates == make_list(local.get_grid_x(grid_id))
    assert server.getGridY(request, None).coordinates == make_list(local.get_grid_y(grid_id))
    assert server.getGridZ(request, None).coordinates == make_list(local.get_grid_z(grid_id))


def test_get_grid_connectivity():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    assert server.getGridConnectivity(request, None).links == make_list(local.get_grid_connectivity(grid_id))
