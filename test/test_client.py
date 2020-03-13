import logging
from unittest.mock import Mock

import grpc
import numpy
import numpy.random
import pytest
from google.protobuf import any_pb2
from google.rpc import error_details_pb2, status_pb2, code_pb2
from grpc_status import rpc_status

from grpc4bmi.bmi_grpc_server import BmiServer
from grpc4bmi.bmi_grpc_client import BmiClient, RemoteException, handle_error
from grpc4bmi.reserve import reserve_values, reserve_grid_shape, reserve_grid_padding
from test.fake_models import SomeException, FailingModel, Rect3DGridModel, UnstructuredGridBmiModel, UniRectGridModel, \
    Rect2DGridModel, Structured3DQuadrilateralsGridModel, Structured2DQuadrilateralsGridModel, Float32Model, Int32Model, \
    BooleanModel
from test.flatbmiheat import FlatBmiHeat

logging.basicConfig(level=logging.DEBUG)

"""
Unit tests for the BMI client class. Every test performs cross-checking with a local instance of the BMI heat toy model.
"""


class MyRpcError(grpc.RpcError):
    def trailing_metadata(self):
        return []


class ServerWrapper(object):

    def __init__(self, server):
        self.server = server
        self.context = Mock(grpc.ServicerContext)

        def forward(status):
            raise MyRpcError(status.details)

        self.context.abort_with_status.side_effect = forward

    def __getattr__(self, item):
        orig_attr = self.server.__getattribute__(item)
        if callable(orig_attr):
            def add_context(*args, **kwargs):
                kwargs["context"] = self.context
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


def test_input_item_count():
    client, local = make_bmi_classes()
    assert client.get_input_item_count() == local.get_input_item_count()
    del client


def test_output_item_count():
    client, local = make_bmi_classes()
    assert client.get_output_item_count() == local.get_output_item_count()
    del client


def test_input_var_names():
    client, local = make_bmi_classes()
    assert client.get_input_var_names() == local.get_input_var_names()
    del client


def test_output_var_names():
    client, local = make_bmi_classes()
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


def test_update_until():
    client, local = make_bmi_classes(True)
    until = local.get_start_time() + local.get_time_step() + local.get_time_step()
    client.update_until(until)
    assert client.get_current_time() == until
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


def test_get_var_location():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]

    assert client.get_var_location(varname) == local.get_var_location(varname)

    del client


def test_get_var_value():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    actual = client.get_value(varname, reserve_values(client, varname))
    expected = local.get_value(varname, reserve_values(local, varname))
    numpy.testing.assert_allclose(actual, expected)
    del client


def test_get_value_ptr():
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


def test_set_var_value():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    values = 0.123 * local.get_value(varname, reserve_values(local, varname))
    client.set_value(varname, values)
    numpy.testing.assert_allclose(client.get_value(varname, reserve_values(client, varname)), values)


def test_set_values_indices():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    indices = numpy.array([1, 11, 21])
    values = numpy.array([0.123, 4.567, 8.901], dtype=numpy.float64)

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

    result = client.get_grid_shape(grid_id, reserve_grid_shape(client, grid_id))

    expected = local.get_grid_shape(grid_id, reserve_grid_shape(local, grid_id))
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_spacing():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)

    result = client.get_grid_spacing(grid_id, reserve_grid_padding(client, grid_id))

    expected = local.get_grid_spacing(grid_id, reserve_grid_padding(local, grid_id))
    numpy.testing.assert_allclose(result, expected)


def test_get_grid_origin():
    client, local = make_bmi_classes(True)
    varname = local.get_output_var_names()[0]
    grid_id = local.get_var_grid(varname)

    result = client.get_grid_origin(grid_id, reserve_grid_padding(client, grid_id))

    expected = local.get_grid_origin(grid_id, reserve_grid_padding(local, grid_id))
    numpy.testing.assert_allclose(result, expected)


@pytest.mark.parametrize("client_method,client_request", [
    ('initialize', ('config.ini',)),
    ('update', ()),
    ('update_until', (42,)),
    ('finalize', ()),
    ('get_component_name', ()),
    ('get_input_item_count', ()),
    ('get_output_item_count', ()),
    ('get_input_var_names', ()),
    ('get_output_var_names', ()),
    ('get_time_units', ()),
    ('get_time_step', ()),
    ('get_current_time', ()),
    ('get_start_time', ()),
    ('get_end_time', ()),
    ('get_var_grid', ('something',)),
    ('get_var_type', ('something',)),
    ('get_var_itemsize', ('something',)),
    ('get_var_units', ('something',)),
    ('get_var_nbytes', ('something',)),
    ('get_var_location', ('something',)),
    ('get_value', ('something', numpy.empty(0))),
    ('get_value_at_indices', ('something', numpy.empty(0), numpy.array([42]))),
    ('set_value', ('something', numpy.array([1234]))),
    ('set_value_at_indices', ('something', numpy.array([42]), numpy.array([1234]))),
    ('get_grid_size', (42,)),
    ('get_grid_type', (42,)),
    ('get_grid_rank', (42,)),
    ('get_grid_x', (42, numpy.empty(0))),
    ('get_grid_y', (42, numpy.empty(0))),
    ('get_grid_z', (42, numpy.empty(0))),
    ('get_grid_shape', (42, numpy.empty(0))),
    ('get_grid_spacing', (42, numpy.empty(0))),
    ('get_grid_origin', (42, numpy.empty(0))),
    ('get_grid_node_count', (42,)),
    ('get_grid_edge_count', (42,)),
    ('get_grid_face_count', (42,)),
    ('get_grid_edge_nodes', (42, numpy.empty(0))),
    ('get_grid_face_nodes', (42, numpy.empty(0))),
    ('get_grid_face_edges', (42, numpy.empty(0))),
    ('get_grid_nodes_per_face', (42, numpy.empty(0))),
])
def test_method_exception(client_method, client_request):
    exc = SomeException('bmi method always fails')
    model = FailingModel(exc)
    client = BmiClient(stub=ServerWrapper(BmiServer(model)))

    with pytest.raises(Exception) as excinfo:
        getattr(client, client_method)(*client_request)

    assert "bmi method always fails" in str(excinfo.value)


class TestUniRectGridModel:
    @pytest.fixture
    def bmiclient(self):
        model = UniRectGridModel()
        client = BmiClient(stub=ServerWrapper(BmiServer(model)))
        yield client
        del client

    def test_grid_type(self, bmiclient):
        assert bmiclient.get_grid_type(0) == 'uniform_rectilinear'

    def test_grid_size(self, bmiclient):
        assert bmiclient.get_grid_size(0) == 24

    def test_grid_rank(self, bmiclient):
        assert bmiclient.get_grid_rank(0) == 3

    def test_grid_shape(self, bmiclient):
        result = bmiclient.get_grid_shape(0, numpy.empty(3))
        expected = (2, 3, 4)
        numpy.testing.assert_allclose(result, expected)

    def test_grid_origin(self, bmiclient):
        result = bmiclient.get_grid_origin(0, numpy.empty(3))
        expected = (0.1, 1.1, 2.1)
        numpy.testing.assert_allclose(result, expected)

    def test_grid_spacing(self, bmiclient):
        result = bmiclient.get_grid_spacing(0, numpy.empty(3))
        expected = (0.1, 0.2, 0.3)
        numpy.testing.assert_allclose(result, expected)


class TestRect3DGridModel:
    @pytest.fixture
    def bmiclient(self):
        model = Rect3DGridModel()
        client = BmiClient(stub=ServerWrapper(BmiServer(model)))
        yield client
        del client

    def test_grid_size(self, bmiclient):
        assert bmiclient.get_grid_size(0) == 24

    def test_grid_rank(self, bmiclient):
        assert bmiclient.get_grid_rank(0) == 3

    def test_grid_x(self, bmiclient):
        result = bmiclient.get_grid_x(0, numpy.empty(4))
        expected = [0.1, 0.2, 0.3, 0.4]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_y(self, bmiclient):
        result = bmiclient.get_grid_y(0, numpy.empty(3))
        expected = [1.1, 1.2, 1.3]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_z(self, bmiclient):
        result = bmiclient.get_grid_z(0, numpy.empty(2))
        expected = [2.1, 2.2]
        numpy.testing.assert_allclose(result, expected)


class TestRect2DGridModel:
    @pytest.fixture
    def bmiclient(self):
        model = Rect2DGridModel()
        client = BmiClient(stub=ServerWrapper(BmiServer(model)))
        yield client
        del client

    def test_grid_size(self, bmiclient):
        assert bmiclient.get_grid_size(0) == 12

    def test_grid_rank(self, bmiclient):
        assert bmiclient.get_grid_rank(0) == 2

    def test_grid_x(self, bmiclient):
        result = bmiclient.get_grid_x(0, numpy.empty(4))
        expected = [0.1, 0.2, 0.3, 0.4]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_y(self, bmiclient):
        result = bmiclient.get_grid_y(0, numpy.empty(3))
        expected = [1.1, 1.2, 1.3]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_z(self, bmiclient):
        with pytest.raises(MyRpcError) as excinfo:
            bmiclient.get_grid_z(0, numpy.empty(4))

        assert 'out of bounds' in str(excinfo.value)


class TestStructured3DQuadrilateralsGridModel:
    @pytest.fixture
    def bmiclient(self):
        model = Structured3DQuadrilateralsGridModel()
        client = BmiClient(stub=ServerWrapper(BmiServer(model)))
        yield client
        del client

    def test_grid_size(self, bmiclient):
        assert bmiclient.get_grid_size(0) == 4

    def test_grid_rank(self, bmiclient):
        assert bmiclient.get_grid_rank(0) == 3

    def test_grid_shape(self, bmiclient):
        result = bmiclient.get_grid_shape(0, numpy.empty(3))
        expected = [1, 2, 2]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_x(self, bmiclient):
        result = bmiclient.get_grid_x(0, numpy.empty(4))
        expected = [1.1, 0.1, 1.1, 2.1]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_y(self, bmiclient):
        result = bmiclient.get_grid_y(0, numpy.empty(4))
        expected = [2.2, 1.2, 0.2, 2.2]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_z(self, bmiclient):
        result = bmiclient.get_grid_z(0, numpy.empty(4))
        expected = [1.1, 2.2, 3.3, 4.4]
        numpy.testing.assert_allclose(result, expected)


class TestStructured2DQuadrilateralsGridModel:
    @pytest.fixture
    def bmiclient(self):
        model = Structured2DQuadrilateralsGridModel()
        client = BmiClient(stub=ServerWrapper(BmiServer(model)))
        yield client
        del client

    def test_grid_size(self, bmiclient):
        assert bmiclient.get_grid_size(0) == 4

    def test_grid_rank(self, bmiclient):
        assert bmiclient.get_grid_rank(0) == 2

    def test_grid_shape(self, bmiclient):
        result = bmiclient.get_grid_shape(0, numpy.empty(2))
        expected = [2, 2]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_x(self, bmiclient):
        result = bmiclient.get_grid_x(0, numpy.empty(4))
        expected = [1.1, 0.1, 1.1, 2.1]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_y(self, bmiclient):
        result = bmiclient.get_grid_y(0, numpy.empty(4))
        expected = [2.2, 1.2, 0.2, 2.2]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_z(self, bmiclient):
        with pytest.raises(MyRpcError) as excinfo:
            bmiclient.get_grid_z(0, numpy.empty(4))

        assert 'Do not know what z is' in str(excinfo.value)


class TestUnstructuredGridBmiModel:
    @pytest.fixture
    def bmiclient(self):
        model = UnstructuredGridBmiModel()
        client = BmiClient(stub=ServerWrapper(BmiServer(model)))
        yield client
        del client

    def test_get_grid_shape(self, bmiclient):
        with pytest.raises(MyRpcError) as excinfo:
            bmiclient.get_grid_shape(0, numpy.empty(3))

        assert 'Do not know what shape is' in str(excinfo.value)

    def test_grid_size(self, bmiclient):
        assert bmiclient.get_grid_size(0) == 6

    def test_grid_rank(self, bmiclient):
        assert bmiclient.get_grid_rank(0) == 2

    def test_get_grid_node_count(self, bmiclient):
        result = bmiclient.get_grid_node_count(0)

        assert result == 6

    def test_get_grid_edge_count(self, bmiclient):
        result = bmiclient.get_grid_edge_count(0)

        assert result == 8

    def test_get_grid_face_count(self, bmiclient):
        result = bmiclient.get_grid_face_count(0)

        assert result == 3

    def test_get_grid_edge_nodes(self, bmiclient):
        placeholder = numpy.empty(16, dtype=numpy.int)

        result = bmiclient.get_grid_edge_nodes(0, placeholder)

        expected = (0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3)
        numpy.testing.assert_allclose(result, expected)

    def test_grid_face_nodes(self, bmiclient):
        placeholder = numpy.empty(11, dtype=numpy.int)

        result = bmiclient.get_grid_face_nodes(0, placeholder)

        expected = (0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3)
        numpy.testing.assert_allclose(result, expected)

    def test_grid_face_edges(self, bmiclient):
        placeholder = numpy.empty(11, dtype=numpy.int)

        result = bmiclient.get_grid_face_edges(0, placeholder)

        expected = (0, 1, 2, 3, 4, 5, 6, 1, 6, 7, 2)
        numpy.testing.assert_allclose(result, expected)

    def test_grid_nodes_per_face(self, bmiclient):
        placeholder = numpy.empty(3, dtype=numpy.int)

        result = bmiclient.get_grid_nodes_per_face(0, placeholder)

        expected = (4, 4, 3)
        numpy.testing.assert_allclose(result, expected)

    def test_grid_x(self, bmiclient):
        result = bmiclient.get_grid_x(0, numpy.empty(6))
        expected = [0., 1., 2., 1., 3., 4.]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_y(self, bmiclient):
        result = bmiclient.get_grid_y(0, numpy.empty(6))
        expected = [3., 1., 2., 4., 0., 3.]
        numpy.testing.assert_allclose(result, expected)

    def test_grid_z(self, bmiclient):
        with pytest.raises(MyRpcError) as excinfo:
            bmiclient.get_grid_z(0, numpy.empty(4))

        assert 'Do not know what z is' in str(excinfo.value)


class TestFloat32Model:
    name = 'plate_surface__temperature'

    @pytest.fixture
    def bmimodel(self):
        return Float32Model()

    @pytest.fixture
    def bmiclient(self, bmimodel):
        client = BmiClient(stub=ServerWrapper(BmiServer(bmimodel)))
        yield client
        del client

    def test_get_value(self, bmiclient):
        result = bmiclient.get_value(self.name, numpy.empty(3))

        expected = numpy.array((1.1, 2.2, 3.3), dtype=numpy.float32)
        numpy.testing.assert_allclose(result, expected)

    def test_get_value_at_indices(self, bmiclient):
        result = bmiclient.get_value_at_indices(self.name, numpy.empty(1), numpy.array([1]))

        expected = numpy.array([2.2], dtype=numpy.float32)
        numpy.testing.assert_allclose(result, expected)

    def test_set_value(self, bmimodel, bmiclient):
        value = numpy.array((2.1, 3.2, 4.3), dtype=numpy.float32)
        bmiclient.set_value(self.name, value)

        numpy.testing.assert_allclose(value, bmimodel.value)

    def test_set_value_at_indices(self, bmimodel, bmiclient):
        value = numpy.array([8.8], dtype=numpy.float32)
        bmiclient.set_value_at_indices(self.name, numpy.array([1]), value)

        expected = numpy.array((1.1, 8.8, 3.3), dtype=numpy.float32)
        numpy.testing.assert_allclose(expected, bmimodel.value)


class TestInt32Model:
    name = 'plate_surface__temperature'

    @pytest.fixture
    def bmimodel(self):
        model = Int32Model()
        yield model
        del model

    @pytest.fixture
    def bmiclient(self, bmimodel):
        client = BmiClient(stub=ServerWrapper(BmiServer(bmimodel)))
        yield client
        del client

    def test_get_value(self, bmiclient):
        result = bmiclient.get_value(self.name, numpy.empty(3))

        expected = numpy.array((12, 24, 36), dtype=numpy.int32)
        numpy.testing.assert_allclose(result, expected)

    def test_get_value_at_indices(self, bmiclient):
        result = bmiclient.get_value_at_indices(self.name, numpy.empty(1), numpy.array([1]))

        expected = numpy.array([24], dtype=numpy.int32)
        numpy.testing.assert_allclose(result, expected)

    def test_set_value(self, bmimodel, bmiclient):
        value = numpy.array((48, 50, 62), dtype=numpy.int32)
        bmiclient.set_value(self.name, value)

        numpy.testing.assert_allclose(value, bmimodel.value)

    def test_set_value_at_indices(self, bmimodel, bmiclient):
        value = numpy.array([88], dtype=numpy.int32)
        bmiclient.set_value_at_indices(self.name, numpy.array([1]), value)

        expected = numpy.array((12, 88, 36), dtype=numpy.int32)
        numpy.testing.assert_allclose(expected, bmimodel.value)


class TestBooleanModel:
    name = 'plate_surface__temperature'

    @pytest.fixture
    def bmimodel(self):
        return BooleanModel()

    @pytest.fixture
    def bmiclient(self, bmimodel):
        client = BmiClient(stub=ServerWrapper(BmiServer(bmimodel)))
        yield client
        del client

    def test_get_value(self, bmiclient):
        with pytest.raises(MyRpcError):
            bmiclient.get_value(self.name, numpy.empty(3))

    def test_get_value_at_indices(self, bmiclient):
        with pytest.raises(MyRpcError):
            bmiclient.get_value_at_indices(self.name, numpy.empty(1, dtype=numpy.bool), numpy.array([1]))

    def test_set_value(self, bmiclient):
        value = numpy.array((False, False, False), dtype=numpy.bool)

        with pytest.raises(NotImplementedError):
            bmiclient.set_value(self.name, value)

    def test_set_value_at_indices(self, bmiclient):
        value = numpy.array([False], dtype=numpy.bool)

        with pytest.raises(NotImplementedError):
            bmiclient.set_value_at_indices(self.name, numpy.array([1]), value)


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
