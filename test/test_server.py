import logging
from unittest.mock import Mock

import numpy
import numpy.random
import pytest
import grpc
from google.rpc import error_details_pb2, status_pb2

from grpc4bmi import bmi_pb2
from grpc4bmi.bmi_grpc_server import BmiServer
from grpc4bmi.reserve import reserve_values, reserve_grid_shape, reserve_grid_padding
from test.fake_models import SomeException, FailingModel, Rect3DGridModel, UnstructuredGridBmiModel
from test.flatbmiheat import FlatBmiHeat

"""
Unit tests for the BMI server class. Every test performs cross-checking with a local instance of the BMI heat toy model.
"""

logging.basicConfig(level=logging.DEBUG)


class RequestStub(object):
    def __init__(self):
        self.config_file = ""

    def HasField(self, name):
        return hasattr(self, name)


class value_wrapper(object):
    def __init__(self, vals):
        self.values = vals.flatten()


def make_string(obj):
    return '' if obj is None else str(obj)


def make_list(obj):
    if obj is list:
        return obj
    if obj is None:
        return []
    return [obj]


def make_bmi_classes(init=False):
    server, local = BmiServer(FlatBmiHeat()), FlatBmiHeat()
    if init:
        req = RequestStub()
        numpy.random.seed(0)
        server.initialize(req, None)
        numpy.random.seed(0)
        local.initialize(None)
    return server, local


def make_var_request(local):
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    return request, varname


def make_grid_request(local):
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)
    setattr(request, "grid_id", grid_id)
    return grid_id, request


def test_server_start():
    server, local = make_bmi_classes()
    assert server is not None
    del server


def test_component_name():
    server, local = make_bmi_classes()
    assert server.getComponentName(None, None).name == local.get_component_name()
    del server


def test_input_var_names():
    server, local = make_bmi_classes()
    assert server.getInputVarNames(None, None).names == list(local.get_input_var_names())
    del server


def test_output_var_names():
    server, local = make_bmi_classes()
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
    request, varname = make_var_request(local)

    assert server.getVarGrid(request, None).grid_id == local.get_var_grid(varname)
    del server


def test_get_var_type():
    server, local = make_bmi_classes(True)
    request, varname = make_var_request(local)

    assert server.getVarType(request, None).type == local.get_var_type(varname)
    del server


def test_get_var_units():
    server, local = make_bmi_classes(True)
    request, varname = make_var_request(local)

    assert server.getVarUnits(request, None).units == local.get_var_units(varname)
    del server


def test_get_var_nbytes():
    server, local = make_bmi_classes(True)
    request, varname = make_var_request(local)

    assert server.getVarNBytes(request, None).nbytes == local.get_var_nbytes(varname)
    del server


def test_get_var_location():
    server, local = make_bmi_classes(True)
    request, varname = make_var_request(local)

    raw_result = server.getVarLocation(request, None).location
    result = bmi_pb2.GetVarLocationResponse.Location.Name(raw_result).lower()

    expected = local.get_var_location(varname)
    assert result == expected
    del server


def test_get_var_value():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    values = local.get_value(varname, reserve_values(local, varname))
    numpy.testing.assert_allclose(
        numpy.reshape(server.getValue(request, reserve_values(local, varname)).values_double.values, values.shape),
        values)


def test_get_var_ptr():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    setattr(request, "name", varname)
    with pytest.raises(NotImplementedError):
        server.getValuePtr(request, None)


def test_get_value_at_indices():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    indices = numpy.array([29, 8, 19, 81])
    setattr(request, "name", varname)
    setattr(request, "indices", indices.flatten())
    setattr(request, "index_size", 1)
    dest = numpy.empty(4)
    values = local.get_value_at_indices(varname, dest, indices)
    numpy.testing.assert_allclose(server.getValueAtIndices(request, None).values_double.values, values.flatten())


def test_get_vals_indices_2d():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    indices = numpy.array([[0, 1], [1, 0], [2, 2]])
    setattr(request, "name", varname)
    setattr(request, "indices", indices.flatten())
    setattr(request, "index_size", 2)
    dest = numpy.empty(6)
    values = local.get_value_at_indices(varname, dest, indices)
    numpy.testing.assert_allclose(server.getValueAtIndices(request, None).values_double.values, values.flatten())


def test_set_var_values():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    dest = reserve_values(local, varname)
    values = 0.123 * local.get_value(varname, dest)
    setattr(request, "name", varname)
    setattr(request, "values_double", value_wrapper(values))
    setattr(request, "shape", values.shape)
    server.setValue(request, None)
    delattr(request, "values_double")
    delattr(request, "shape")
    response = server.getValue(request, None)
    numpy.testing.assert_allclose(values, response.values_double.values)


def test_set_values_indices():
    server, local = make_bmi_classes(True)
    request = RequestStub()
    varname = local.get_output_var_names()[0]
    indices = numpy.array([1, 11, 21])
    values = numpy.array([0.123, 4.567, 8.901])
    setattr(request, "name", varname)
    setattr(request, "values_double", value_wrapper(values))
    setattr(request, "indices", indices.flatten())
    setattr(request, "index_size", 1)
    server.setValueAtIndices(request, None)
    delattr(request, "values_double")
    response = server.getValueAtIndices(request, None)
    values_copy = numpy.array(response.values_double.values)
    numpy.testing.assert_allclose(values, values_copy)


def test_get_grid_size():
    server, local = make_bmi_classes(True)
    grid_id, request = make_grid_request(local)
    assert server.getGridSize(request, None).size == local.get_grid_size(grid_id)


def test_get_grid_rank():
    server, local = make_bmi_classes(True)
    grid_id, request = make_grid_request(local)
    assert server.getGridRank(request, None).rank == local.get_grid_rank(grid_id)


def test_get_grid_type():
    server, local = make_bmi_classes(True)
    grid_id, request = make_grid_request(local)
    assert server.getGridType(request, None).type == local.get_grid_type(grid_id)


def test_get_grid_shape():
    server, local = make_bmi_classes(True)
    grid_id, request = make_grid_request(local)
    result = server.getGridShape(request, reserve_grid_shape(local, grid_id)).shape
    expected = local.get_grid_shape(grid_id, reserve_grid_shape(local, grid_id))
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_spacing():
    server, local = make_bmi_classes(True)
    grid_id, request = make_grid_request(local)
    result = server.getGridSpacing(request, reserve_grid_padding(local, grid_id)).spacing
    expected = local.get_grid_spacing(grid_id, reserve_grid_padding(local, grid_id))
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_origin():
    server, local = make_bmi_classes(True)
    grid_id, request = make_grid_request(local)
    result = server.getGridOrigin(request, reserve_grid_padding(local, grid_id)).origin
    expected = local.get_grid_origin(grid_id, reserve_grid_padding(local, grid_id))
    numpy.testing.assert_allclose(result, expected)


@pytest.mark.parametrize("server_method,server_request", [
    ('initialize', bmi_pb2.InitializeRequest(config_file='/data/config.ini')),
    ('update', bmi_pb2.Empty()),
    ('updateUntil', bmi_pb2.GetTimeResponse(time=42)),
    ('finalize', bmi_pb2.Empty()),
    ('getComponentName', bmi_pb2.Empty()),
    ('getInputItemCount', bmi_pb2.Empty()),
    ('getOutputItemCount', bmi_pb2.Empty()),
    ('getInputVarNames', bmi_pb2.Empty()),
    ('getOutputVarNames', bmi_pb2.Empty()),
    ('getTimeUnits', bmi_pb2.Empty()),
    ('getTimeStep', bmi_pb2.Empty()),
    ('getCurrentTime', bmi_pb2.Empty()),
    ('getStartTime', bmi_pb2.Empty()),
    ('getEndTime', bmi_pb2.Empty()),
    ('getVarGrid', bmi_pb2.GetVarRequest(name='something')),
    ('getVarType', bmi_pb2.GetVarRequest(name='something')),
    ('getVarItemSize', bmi_pb2.GetVarRequest(name='something')),
    ('getVarUnits', bmi_pb2.GetVarRequest(name='something')),
    ('getVarNBytes', bmi_pb2.GetVarRequest(name='something')),
    ('getValue', bmi_pb2.GetVarRequest(name='something')),
    ('getValueAtIndices', bmi_pb2.GetValueAtIndicesRequest(name='something', indices=(42,))),
    ('setValue', bmi_pb2.SetValueRequest(name='something', values_int=bmi_pb2.IntArrayMessage(values=(42,)))),
    ('setValueAtIndices', bmi_pb2.SetValueAtIndicesRequest(name='something', indices=(43,),
                                                           values_int=bmi_pb2.IntArrayMessage(values=(1234,)))),
    ('getGridSize', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridType', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridRank', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridShape', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridSpacing', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridOrigin', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridX', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridY', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridZ', bmi_pb2.GridRequest(grid_id=42)),

    ('getGridNodeCount', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridEdgeCount', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridFaceCount', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridEdgeNodes', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridFaceNodes', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridFaceEdges', bmi_pb2.GridRequest(grid_id=42)),
    ('getGridNodesPerFace', bmi_pb2.GridRequest(grid_id=42)),
])
def test_method_exceptions_with_stacktrace(server_method, server_request):
    exc = SomeException('Bmi method always fails')
    model = FailingModel(exc)
    server = BmiServer(model, True)
    context = Mock(grpc.ServicerContext)

    getattr(server, server_method)(server_request, context)

    context.abort_with_status.assert_called_once()
    status = context.abort_with_status.call_args[0][0]
    assert status.code == grpc.StatusCode.INTERNAL
    assert status.details == 'Bmi method always fails'
    metadata = status_pb2.Status.FromString(status.trailing_metadata[0][1])
    debuginfo = error_details_pb2.DebugInfo()
    metadata.details[0].Unpack(debuginfo)
    assert debuginfo.detail == "SomeException('Bmi method always fails',)"
    assert len(debuginfo.stack_entries) > 0


def test_get_grid_x():
    model = Rect3DGridModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridX(request, None).coordinates

    expected = numpy.array([0.1, 0.2, 0.3, 0.4])
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_y():
    model = Rect3DGridModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridY(request, None).coordinates

    expected = numpy.array([1.1, 1.2, 1.3])
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_z():
    model = Rect3DGridModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridZ(request, None).coordinates

    expected = numpy.array([2.1, 2.2])
    numpy.testing.assert_allclose(result, expected)


def test_grid_node_count():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridNodeCount(request, None).count

    assert result == 6


def test_grid_edge_count():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridEdgeCount(request, None).count

    assert result == 8


def test_grid_face_count():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridFaceCount(request, None).count

    assert result == 3


def test_get_grid_edge_nodes():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridEdgeNodes(request, None).edge_nodes

    expected = (0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3)
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_face_nodes():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridFaceNodes(request, None).face_nodes

    expected = (0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3)
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_face_edges():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridFaceEdges(request, None).face_edges

    expected = (0, 1, 2, 3, 4, 5, 6, 1, 6, 7, 2)
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_nodes_per_face():
    model = UnstructuredGridBmiModel()
    server = BmiServer(model, True)
    grid_id, request = make_grid_request(model)

    result = server.getGridNodesPerFace(request, None).nodes_per_face

    numpy.testing.assert_allclose(result, (4, 4, 3))
