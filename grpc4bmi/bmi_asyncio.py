
from grpclib.client import Channel
from google.rpc import error_details_pb2
from grpclib.exceptions import GRPCError
import numpy

from . import bmi_pb2, bmi_grpc


class RemoteException(RuntimeError):
    def __init__(self, message, tb):
        super().__init__(message)
        self.remote_stacktrace = tb


def handle_error(exc):
    """Parsers DebugInfo (https://github.com/googleapis/googleapis/blob/07244bb797ddd6e0c1c15b02b4467a9a5729299f/google/rpc/error_details.proto#L46-L52) from the trailing metadata of a GRPCError

    Args:
        exc (GRPCError): Exception to handle

    Raises: original exception or RemoteException

    """
    if exc.details:
        for detail in exc.details:
            if detail.Is(error_details_pb2.DebugInfo.DESCRIPTOR):
                info = error_details_pb2.DebugInfo()
                detail.Unpack(info)
                remote_traceback = info.stack_entries
                remote_detail = info.detail
                raise RemoteException(remote_detail, remote_traceback) from exc
    raise


def make_array(response):
    if response.HasField("values_int"):
        return numpy.array(response.values_int.values)
    if response.HasField("values_float"):
        return numpy.array(response.values_float.values)
    if response.HasField("values_double"):
        return numpy.array(response.values_double.values)


# TODO extend from Bmi interface
class BmiClientAsync:
    def __init__(self, port, host='127.0.0.1', ssl=None):
        self.channel = Channel(host=host, port=port, ssl=ssl)
        self.stub = bmi_grpc.BmiServiceStub(self.channel)

    def __del__(self):
        self.channel.close()

    async def initialize(self, filename):
        fname = "" if filename is None else filename
        try:
            return await self.stub.initialize(bmi_pb2.InitializeRequest(config_file=fname))
        except GRPCError as e:
            handle_error(e)

    async def update(self):
        try:
            await self.stub.update(bmi_pb2.Empty())
        except GRPCError as e:
            handle_error(e)

    async def update_frac(self, time_frac):
        try:
            await self.stub.updateFrac(bmi_pb2.UpdateFracRequest(frac=time_frac))
        except GRPCError as e:
            handle_error(e)

    async def update_until(self, time):
        try:
            await self.stub.updateUntil(bmi_pb2.UpdateUntilRequest(until=time))
        except GRPCError as e:
            handle_error(e)

    async def finalize(self):
        try:
            await self.stub.finalize(bmi_pb2.Empty())
        except GRPCError as e:
            handle_error(e)

    async def get_component_name(self):
        try:
            return str((await self.stub.getComponentName(bmi_pb2.Empty())).name)
        except GRPCError as e:
            handle_error(e)

    async def get_input_var_names(self):
        try:
            return tuple([str(s) for s in (await self.stub.getInputVarNames(bmi_pb2.Empty())).names])
        except GRPCError as e:
            handle_error(e)

    async def get_output_var_names(self):
        try:
            return tuple([str(s) for s in (await self.stub.getOutputVarNames(bmi_pb2.Empty())).names])
        except GRPCError as e:
            handle_error(e)

    async def get_time_units(self):
        try:
            response = str((await self.stub.getTimeUnits(bmi_pb2.Empty())).units)
            return None if not response else response
        except GRPCError as e:
            handle_error(e)

    async def get_time_step(self):
        try:
            return (await self.stub.getTimeStep(bmi_pb2.Empty())).interval
        except GRPCError as e:
            handle_error(e)

    async def get_current_time(self):
        try:
            return (await self.stub.getCurrentTime(bmi_pb2.Empty())).time
        except GRPCError as e:
            handle_error(e)

    async def get_start_time(self):
        try:
            return (await self.stub.getStartTime(bmi_pb2.Empty())).time
        except GRPCError as e:
            handle_error(e)

    async def get_end_time(self):
        try:
            return (await self.stub.getEndTime(bmi_pb2.Empty())).time
        except GRPCError as e:
            handle_error(e)

    async def get_var_grid(self, var_name):
        try:
            return (await self.stub.getVarGrid(bmi_pb2.GetVarRequest(name=var_name))).grid_id
        except GRPCError as e:
            handle_error(e)

    async def get_var_type(self, var_name):
        try:
            return str((await self.stub.getVarType(bmi_pb2.GetVarRequest(name=var_name))).type)
        except GRPCError as e:
            handle_error(e)

    async def get_var_itemsize(self, var_name):
        try:
            return (await self.stub.getVarItemSize(bmi_pb2.GetVarRequest(name=var_name))).size
        except GRPCError as e:
            handle_error(e)

    async def get_var_units(self, var_name):
        try:
            response = str((await self.stub.getVarUnits(bmi_pb2.GetVarRequest(name=var_name))).units)
            return None if not response else response
        except GRPCError as e:
            handle_error(e)

    async def get_var_nbytes(self, var_name):
        try:
            return (await self.stub.getVarNBytes(bmi_pb2.GetVarRequest(name=var_name))).nbytes
        except GRPCError as e:
            handle_error(e)

    async def get_value(self, var_name):
        try:
            response = await self.stub.getValue(bmi_pb2.GetVarRequest(name=var_name))
            return make_array(response)
        except GRPCError as e:
            handle_error(e)

    async def get_value_ref(self, var_name):
        """Not possible, unable give reference to data structure in another process and possibly another machine"""
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    async def get_value_at_indices(self, var_name, indices):
        try:
            index_array = indices
            if indices is list:
                index_array = numpy.array(indices)
            response = await self.stub.getValueAtIndices(bmi_pb2.GetValueAtIndicesRequest(name=var_name,
                                                                                          indices=index_array.flatten()))
            return make_array(response)
        except GRPCError as e:
            handle_error(e)

    async def set_value(self, var_name, src):
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
            await self.stub.setValue(request)
        except GRPCError as e:
            handle_error(e)

    async def set_value_at_indices(self, var_name, indices, src):
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
            await self.stub.setValueAtIndices(request)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_size(self, grid_id):
        try:
            return (await self.stub.getGridSize(bmi_pb2.GridRequest(grid_id=grid_id))).size
        except GRPCError as e:
            handle_error(e)

    async def get_grid_rank(self, grid_id):
        try:
            return (await self.stub.getGridRank(bmi_pb2.GridRequest(grid_id=grid_id))).rank
        except GRPCError as e:
            handle_error(e)

    async def get_grid_type(self, grid_id):
        try:
            return str((await self.stub.getGridType(bmi_pb2.GridRequest(grid_id=grid_id))).type)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_x(self, grid_id):
        try:
            return numpy.array((await self.stub.getGridX(bmi_pb2.GridRequest(grid_id=grid_id))).coordinates)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_y(self, grid_id):
        try:
            return numpy.array((await self.stub.getGridY(bmi_pb2.GridRequest(grid_id=grid_id))).coordinates)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_z(self, grid_id):
        try:
            return numpy.array((await self.stub.getGridZ(bmi_pb2.GridRequest(grid_id=grid_id))).coordinates)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_shape(self, grid_id):
        try:
            return tuple((await self.stub.getGridShape(bmi_pb2.GridRequest(grid_id=grid_id))).shape)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_spacing(self, grid_id):
        try:
            return tuple((await self.stub.getGridSpacing(bmi_pb2.GridRequest(grid_id=grid_id))).spacing)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_offset(self, grid_id):
        try:
            return tuple((await self.stub.getGridOffset(bmi_pb2.GridRequest(grid_id=grid_id))).offsets)
        except GRPCError as e:
            handle_error(e)

    async def get_grid_connectivity(self, grid_id):
        try:
            return (await self.stub.getGridConnectivity(bmi_pb2.GridRequest(grid_id=grid_id))).links
        except GRPCError as e:
            handle_error(e)

    async def get_grid_origin(self, grid_id):
        try:
            return tuple((await self.stub.getGridOrigin(bmi_pb2.GridRequest(grid_id=grid_id))).origin)
        except GRPCError as e:
            handle_error(e)
