import logging
import os
import socket
from contextlib import closing

import basic_modeling_interface.bmi as bmi
import grpc
import numpy

from grpc_status import rpc_status
from google.rpc import error_details_pb2

from . import bmi_pb2, bmi_pb2_grpc

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


class BmiClient(bmi.Bmi):
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

    occupied_ports = set()

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
        elif p in BmiClient.occupied_ports:
            log.error("Attempt to create grpc channel on occupied port %d" % p)
            return None
        BmiClient.occupied_ports.add(p)
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

    def update_frac(self, time_frac):
        try:
            self.stub.updateFrac(bmi_pb2.UpdateFracRequest(frac=time_frac))
        except grpc.RpcError as e:
            handle_error(e)

    def update_until(self, time):
        try:
            self.stub.updateUntil(bmi_pb2.UpdateUntilRequest(until=time))
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

    def get_var_grid(self, var_name):
        try:
            return self.stub.getVarGrid(bmi_pb2.GetVarRequest(name=var_name)).grid_id
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_type(self, var_name):
        try:
            return str(self.stub.getVarType(bmi_pb2.GetVarRequest(name=var_name)).type)
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_itemsize(self, var_name):
        try:
            return self.stub.getVarItemSize(bmi_pb2.GetVarRequest(name=var_name)).size
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_units(self, var_name):
        try:
            response = str(self.stub.getVarUnits(bmi_pb2.GetVarRequest(name=var_name)).units)
            return None if not response else response
        except grpc.RpcError as e:
            handle_error(e)

    def get_var_nbytes(self, var_name):
        try:
            return self.stub.getVarNBytes(bmi_pb2.GetVarRequest(name=var_name)).nbytes
        except grpc.RpcError as e:
            handle_error(e)

    def get_value(self, var_name):
        try:
            response = self.stub.getValue(bmi_pb2.GetVarRequest(name=var_name))
            return BmiClient.make_array(response)
        except grpc.RpcError as e:
            handle_error(e)

    def get_value_ref(self, var_name):
        """Not possible, unable give reference to data structure in another process and possibly another machine"""
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def get_value_at_indices(self, var_name, indices):
        try:
            index_array = indices
            if indices is list:
                index_array = numpy.array(indices)
            response = self.stub.getValueAtIndices(bmi_pb2.GetValueAtIndicesRequest(name=var_name,
                                                                                    indices=index_array.flatten()))
            return BmiClient.make_array(response)
        except grpc.RpcError as e:
            handle_error(e)

    def set_value(self, var_name, src):
        try:
            if src.dtype in [numpy.int32, numpy.int64]:
                request = bmi_pb2.SetValueRequest(name=var_name,
                                                  values_int=bmi_pb2.IntArrayMessage(values=src.flatten()))
            elif src.dtype == numpy.float32:
                request = bmi_pb2.SetValueRequest(name=var_name,
                                                  values_float=bmi_pb2.FloatArrayMessage(values=src.flatten()))
            elif src.dtype == numpy.float64:
                request = bmi_pb2.SetValueRequest(name=var_name,
                                                  values_double=bmi_pb2.DoubleArrayMessage(values=src.flatten()))
            else:
                raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % src.dtype)
            self.stub.setValue(request)
        except grpc.RpcError as e:
            handle_error(e)

    def set_value_at_indices(self, var_name, indices, src):
        try:
            index_array = indices
            if indices is list:
                index_array = numpy.array(indices)
            if src.dtype in [numpy.int32, numpy.int64]:
                request = bmi_pb2.SetValueAtIndicesRequest(name=var_name,
                                                           indices=index_array.flatten(),
                                                           values_int=bmi_pb2.IntArrayMessage(values=src.flatten()))
            elif src.dtype == numpy.float32:
                request = bmi_pb2.SetValueAtIndicesRequest(name=var_name,
                                                           indices=index_array.flatten(),
                                                           values_float=bmi_pb2.FloatArrayMessage(values=src.flatten()))
            elif src.dtype == numpy.float64:
                request = bmi_pb2.SetValueAtIndicesRequest(name=var_name,
                                                           indices=index_array.flatten(),
                                                           values_double=bmi_pb2.DoubleArrayMessage(values=src.flatten()))
            else:
                raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % src.dtype)
            self.stub.setValueAtIndices(request)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_size(self, grid_id):
        try:
            return self.stub.getGridSize(bmi_pb2.GridRequest(grid_id=grid_id)).size
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_rank(self, grid_id):
        try:
            return self.stub.getGridRank(bmi_pb2.GridRequest(grid_id=grid_id)).rank
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_type(self, grid_id):
        try:
            return str(self.stub.getGridType(bmi_pb2.GridRequest(grid_id=grid_id)).type)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_x(self, grid_id):
        try:
            return numpy.array(self.stub.getGridX(bmi_pb2.GridRequest(grid_id=grid_id)).coordinates)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_y(self, grid_id):
        try:
            return numpy.array(self.stub.getGridY(bmi_pb2.GridRequest(grid_id=grid_id)).coordinates)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_z(self, grid_id):
        try:
            return numpy.array(self.stub.getGridZ(bmi_pb2.GridRequest(grid_id=grid_id)).coordinates)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_shape(self, grid_id):
        try:
            return tuple(self.stub.getGridShape(bmi_pb2.GridRequest(grid_id=grid_id)).shape)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_spacing(self, grid_id):
        try:
            return tuple(self.stub.getGridSpacing(bmi_pb2.GridRequest(grid_id=grid_id)).spacing)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_offset(self, grid_id):
        try:
            return tuple(self.stub.getGridOffset(bmi_pb2.GridRequest(grid_id=grid_id)).offsets)
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_connectivity(self, grid_id):
        try:
            return self.stub.getGridConnectivity(bmi_pb2.GridRequest(grid_id=grid_id)).links
        except grpc.RpcError as e:
            handle_error(e)

    def get_grid_origin(self, grid_id):
        try:
            return tuple(self.stub.getGridOrigin(bmi_pb2.GridRequest(grid_id=grid_id)).origin)
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
