import logging
import math
import os
import socket
from contextlib import closing

import numpy as np
from bmipy import Bmi
import grpc
import numpy

from grpc_status import rpc_status
from google.rpc import error_details_pb2

from . import bmi_pb2, bmi_pb2_grpc
from .utils import GRPC_MAX_MESSAGE_LENGTH

log = logging.getLogger(__name__)


class RemoteException(grpc.RpcError):
    def __init__(self, message, tb):
        super().__init__(message)
        self.remote_stacktrace = tb


def handle_error(exc):
    """Parsers DebugInfo (https://github.com/googleapis/googleapis/blob/07244bb797ddd6e0c1c15b02b4467a9a5729299f/google/rpc/error_details.proto#L46-L52) from the trailing metadata of a grpc.RpcError

    Args:
        exc (grpc.RpcError): Exception to handle

    Raises: original exception or RemoteException

    """
    status = rpc_status.from_call(exc)
    if status is None:
        raise
    for detail in status.details:
        if detail.Is(error_details_pb2.DebugInfo.DESCRIPTOR):
            info = error_details_pb2.DebugInfo()
            detail.Unpack(info)
            remote_traceback = info.stack_entries
            remote_detail = info.detail
            raise RemoteException(remote_detail, remote_traceback) from exc
    raise


def _fits_in_message(array):
    """Tests whether array can be passed through a gRPC message with a max message size of 4Mb"""
    array_size = array.size * array.itemsize
    return array_size <= GRPC_MAX_MESSAGE_LENGTH


class BmiClient(Bmi):
    """
    Client BMI interface, implementing BMI by forwarding every function call via GRPC to the server connected to the
    same port. A GRPC channel can be passed to the constructor; if not, it constructs an insecure channel on a free
    port itself. The timeout parameter indicates the model BMI startup timeout parameter (s).

    >>> import grpc
    >>> from grpc4bmi.bmi_grpc_client import BmiClient
    >>> mymodel = BmiClient(grpc.insecure_channel("localhost:<PORT>"))
    >>> print(mymodel.get_component_name())
    Hello world
    """

    def __init__(self, channel=None, timeout=None, stub=None):
        if stub is None:
            c = BmiClient.create_grpc_channel() if channel is None else channel
            self.stub = bmi_pb2_grpc.BmiServiceStub(c)
            future = grpc.channel_ready_future(c)
            future.result(timeout=timeout)
        else:
            self.stub = stub

    def __del__(self):
        del self.stub

    @staticmethod
    def create_grpc_channel(port=0, host=None):
        p, h = port, host
        if h is None:
            h = "localhost"
        if p == 0:
            p = os.environ.get("BMI_PORT", 50051)
        return grpc.insecure_channel(':'.join([h, str(p)]))

    @staticmethod
    def get_unique_port(host=None):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("" if host is None else host, 0))
            return int(s.getsockname()[1])

    def initialize(self, filename):
        fname = "" if filename is None else filename
        try:
            return self.stub.initialize(bmi_pb2.InitializeRequest(config_file=fname))
        except grpc.RpcError as e:
            handle_error(e)

    def update(self):
        try:
            self.stub.update(bmi_pb2.Empty())
        except grpc.RpcError as e:
            handle_error(e)

    def update_until(self, time: float) -> None:
        try:
            self.stub.updateUntil(bmi_pb2.GetTimeResponse(time=time))
        except grpc.RpcError as e:
            handle_error(e)

    def finalize(self):
        try:
            self.stub.finalize(bmi_pb2.Empty())
        except grpc.RpcError as e:
            handle_error(e)

    def get_component_name(self):
        try:
            return str(self.stub.getComponentName(bmi_pb2.Empty()).name)
        except grpc.RpcError as e:
            handle_error(e)

    def get_input_item_count(self) -> int:
        try:
            return self.stub.getInputItemCount(bmi_pb2.Empty()).count
        except grpc.RpcError as e:
            handle_error(e)

    def get_output_item_count(self) -> int:
        try:
            return self.stub.getOutputItemCount(bmi_pb2.Empty()).count
        except grpc.RpcError as e:
            handle_error(e)

    def get_input_var_names(self):
        try:
            return tuple([str(s) for s in self.stub.getInputVarNames(bmi_pb2.Empty()).names])
        except grpc.RpcError as e:
            handle_error(e)

    def get_output_var_names(self):
        try:
            return tuple([str(s) for s in self.stub.getOutputVarNames(bmi_pb2.Empty()).names])
        except grpc.RpcError as e:
            handle_error(e)

    def get_time_units(self):
        try:
            response = str(self.stub.getTimeUnits(bmi_pb2.Empty()).units)
            return None if not response else response
        except grpc.RpcError as e:
            handle_error(e)

    def get_time_step(self):
        try:
            return self.stub.getTimeStep(bmi_pb2.Empty()).interval
        except grpc.RpcError as e:
            handle_error(e)

    def get_current_time(self):
        try:
            return self.stub.getCurrentTime(bmi_pb2.Empty()).time
        except grpc.RpcError as e:
            handle_error(e)

    def get_start_time(self):
        try:
            return self.stub.getStartTime(bmi_pb2.Empty()).time
        except grpc.RpcError as e:
            handle_error(e)

    def get_end_time(self):
        try:
            return self.stub.getEndTime(bmi_pb2.Empty()).time
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_grid(self, name):
        try:
            return self.stub.getVarGrid(bmi_pb2.GetVarRequest(name=name)).grid_id
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_type(self, name):
        try:
            return str(self.stub.getVarType(bmi_pb2.GetVarRequest(name=name)).type)
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_itemsize(self, name):
        try:
            return self.stub.getVarItemSize(bmi_pb2.GetVarRequest(name=name)).size
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_units(self, name):
        try:
            response = str(self.stub.getVarUnits(bmi_pb2.GetVarRequest(name=name)).units)
            return None if not response else response
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_nbytes(self, name):
        try:
            return self.stub.getVarNBytes(bmi_pb2.GetVarRequest(name=name)).nbytes
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_location(self, name: str) -> str:
        try:
            location = self.stub.getVarLocation(bmi_pb2.GetVarRequest(name=name)).location
            return bmi_pb2.GetVarLocationResponse.Location.Name(location).lower()
        except grpc.RpcError as e:
            handle_error(e)

    def get_value(self, name, dest):
        fits = _fits_in_message(dest)
        if not fits:
            return self._chunked_get_value(name, dest)
        try:
            response = self.stub.getValue(bmi_pb2.GetVarRequest(name=name))
            numpy.copyto(src=BmiClient.make_array(response), dst=dest)
            return dest
        except grpc.RpcError as e:
            handle_error(e)

    def _chunked_get_value(self, name: str, dest: np.array) -> np.array:
        # Make chunk one item smaller than maximum (4Mb)
        chunk_size = math.floor(GRPC_MAX_MESSAGE_LENGTH / dest.dtype.itemsize) - dest.dtype.itemsize
        chunks = []
        log.info(f'Too many items ({dest.size}) for single call, '
                 f'using multiple get_value_at_indices() with into chunks of {chunk_size} items')
        for i in range(0, dest.size, chunk_size):
            start = i
            stop = i + chunk_size
            # Last chunk can be smaller
            if stop > dest.size:
                stop = dest.size
            chunks.append(self._get_value_at_range(name, start, stop))

        numpy.concatenate(chunks, out=dest)
        return dest

    def _get_value_at_range(self, name, start, stop):
        log.info(f'Fetching value range {start} - {stop}')
        try:
            response = self.stub.getValueAtIndices(bmi_pb2.GetValueAtIndicesRequest(name=name,
                                                                                    indices=range(start, stop)))
            return BmiClient.make_array(response)
        except grpc.RpcError as e:
            handle_error(e)

    def get_value_ptr(self, name: str) -> np.ndarray:
        """Not possible, unable give reference to data structure in another process and possibly another machine"""
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def get_value_at_indices(self, name, dest, indices):
        try:
            index_array = indices
            if indices is list:
                index_array = numpy.array(indices)
            response = self.stub.getValueAtIndices(bmi_pb2.GetValueAtIndicesRequest(name=name,
                                                                                    indices=index_array.flatten()))
            numpy.copyto(src=BmiClient.make_array(response), dst=dest)
            return dest
        except grpc.RpcError as e:
            handle_error(e)

    def set_value(self, name, values):
        try:
            if values.dtype in (numpy.int16, numpy.int32, numpy.int64):
                request = bmi_pb2.SetValueRequest(name=name,
                                                  values_int=bmi_pb2.IntArrayMessage(values=values.flatten()))
            elif values.dtype in (numpy.float32, numpy.float16):
                request = bmi_pb2.SetValueRequest(name=name,
                                                  values_float=bmi_pb2.FloatArrayMessage(values=values.flatten()))
            elif values.dtype == numpy.float64:
                request = bmi_pb2.SetValueRequest(name=name,
                                                  values_double=bmi_pb2.DoubleArrayMessage(values=values.flatten()))
            else:
                raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % values.dtype)
            self.stub.setValue(request)
        except grpc.RpcError as e:
            handle_error(e)

    def set_value_at_indices(self, name, inds, src):
        try:
            index_array = inds
            if inds is list:
                index_array = numpy.array(inds)
            if src.dtype in (numpy.int32, numpy.int64):
                request = bmi_pb2.SetValueAtIndicesRequest(name=name,
                                                           indices=index_array.flatten(),
                                                           values_int=bmi_pb2.IntArrayMessage(values=src.flatten()))
            elif src.dtype in (numpy.float32, numpy.float16):
                request = bmi_pb2.SetValueAtIndicesRequest(name=name,
                                                           indices=index_array.flatten(),
                                                           values_float=bmi_pb2.FloatArrayMessage(values=src.flatten()))
            elif src.dtype == numpy.float64:
                request = bmi_pb2.SetValueAtIndicesRequest(name=name,
                                                           indices=index_array.flatten(),
                                                           values_double=bmi_pb2.DoubleArrayMessage(values=src.flatten()))
            else:
                raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % src.dtype)
            self.stub.setValueAtIndices(request)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_size(self, grid):
        try:
            return self.stub.getGridSize(bmi_pb2.GridRequest(grid_id=grid)).size
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_rank(self, grid):
        try:
            return self.stub.getGridRank(bmi_pb2.GridRequest(grid_id=grid)).rank
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_type(self, grid):
        try:
            return str(self.stub.getGridType(bmi_pb2.GridRequest(grid_id=grid)).type)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_x(self, grid, x):
        try:
            src = numpy.array(self.stub.getGridX(bmi_pb2.GridRequest(grid_id=grid)).coordinates)
            numpy.copyto(src=src, dst=x)
            return x
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_y(self, grid, y):
        try:
            src = numpy.array(self.stub.getGridY(bmi_pb2.GridRequest(grid_id=grid)).coordinates)
            numpy.copyto(src=src, dst=y)
            return y
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_z(self, grid, z):
        try:
            src = numpy.array(self.stub.getGridZ(bmi_pb2.GridRequest(grid_id=grid)).coordinates)
            numpy.copyto(src=src, dst=z)
            return z
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_shape(self, grid, shape):
        try:
            src = tuple(self.stub.getGridShape(bmi_pb2.GridRequest(grid_id=grid)).shape)
            numpy.copyto(src=src, dst=shape)
            return shape
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_spacing(self, grid, spacing):
        try:
            src = tuple(self.stub.getGridSpacing(bmi_pb2.GridRequest(grid_id=grid)).spacing)
            numpy.copyto(src=src, dst=spacing)
            return spacing
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_origin(self, grid, origin):
        try:
            src = tuple(self.stub.getGridOrigin(bmi_pb2.GridRequest(grid_id=grid)).origin)
            numpy.copyto(src=src, dst=origin)
            return origin
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_node_count(self, grid: int) -> int:
        try:
            return self.stub.getGridNodeCount(bmi_pb2.GridRequest(grid_id=grid)).count
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_edge_count(self, grid: int) -> int:
        try:
            return self.stub.getGridEdgeCount(bmi_pb2.GridRequest(grid_id=grid)).count
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_face_count(self, grid: int) -> int:
        try:
            return self.stub.getGridFaceCount(bmi_pb2.GridRequest(grid_id=grid)).count
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_edge_nodes(self, grid: int, edge_nodes: np.ndarray) -> np.ndarray:
        try:
            links = self.stub.getGridEdgeNodes(bmi_pb2.GridRequest(grid_id=grid)).edge_nodes
            numpy.copyto(src=links, dst=edge_nodes)
            return edge_nodes
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_face_nodes(self, grid: int, face_nodes: np.ndarray) -> np.ndarray:
        try:
            links = self.stub.getGridFaceNodes(bmi_pb2.GridRequest(grid_id=grid)).face_nodes
            numpy.copyto(src=links, dst=face_nodes)
            return face_nodes
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_face_edges(self, grid: int, face_edges: np.ndarray) -> np.ndarray:
        try:
            links = self.stub.getGridFaceEdges(bmi_pb2.GridRequest(grid_id=grid)).face_edges
            numpy.copyto(src=links, dst=face_edges)
            return face_edges
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: np.ndarray) -> np.ndarray:
        try:
            links = self.stub.getGridNodesPerFace(bmi_pb2.GridRequest(grid_id=grid)).nodes_per_face
            numpy.copyto(src=links, dst=nodes_per_face)
            return nodes_per_face
        except grpc.RpcError as e:
            handle_error(e)

    @staticmethod
    def make_array(response):
        if response.HasField("values_int"):
            return numpy.array(response.values_int.values)
        if response.HasField("values_float"):
            return numpy.array(response.values_float.values)
        if response.HasField("values_double"):
            return numpy.array(response.values_double.values)
