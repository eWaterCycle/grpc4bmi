import logging

import bmi
import grpc
import numpy

import bmi_pb2
import bmi_pb2_grpc

log = logging.getLogger(__name__)


class BmiClient(bmi.Bmi):

    occupied_ports = set()
    start_port = 50051

    def __init__(self, channel=None):
        c = BmiClient.create_grpc_channel() if channel is None else channel
        self.stub = bmi_pb2_grpc.BmiServiceStub(c)

    @staticmethod
    def create_grpc_channel(port=0, host=None):
        p, h = port, host
        if p == 0:
            p = BmiClient.get_unique_port()
        elif p in BmiClient.occupied_ports:
            log.error("Attempt to create grpc channel on occupied port %d" % p)
            return None
        if h is None:
            h = "localhost"
        BmiClient.occupied_ports.add(p)
        return grpc.insecure_channel(':'.join([h, str(p)]))

    @staticmethod
    def get_unique_port():
        return sorted(BmiClient.occupied_ports)[-1] + 1 if any(BmiClient.occupied_ports) else BmiClient.start_port

    def initialize(self, filename):
        fname = "" if filename is None else filename
        self.stub.initialize(bmi_pb2.InitializeRequest(config_file=fname))

    def update(self):
        self.stub.update(bmi_pb2.Empty())

    def update_frac(self, time_frac):
        self.stub.updateFrac(bmi_pb2.UpdateFracRequest(frac=time_frac))

    def update_until(self, time):
        self.stub.updateUntil(bmi_pb2.UpdateUntilRequest(until=time))

    def finalize(self):
        self.stub.finalize(bmi_pb2.Empty())

    def get_component_name(self):
        return str(self.stub.getComponentName(bmi_pb2.Empty()).name)

    def get_input_var_names(self):
        return tuple([str(s) for s in self.stub.getInputVarNames(bmi_pb2.Empty()).names])

    def get_output_var_names(self):
        return tuple([str(s) for s in self.stub.getOutputVarNames(bmi_pb2.Empty()).names])

    def get_time_units(self):
        return str(self.stub.getTimeUnits(bmi_pb2.Empty()).units)

    def get_time_step(self):
        return self.stub.getTimeStep(bmi_pb2.Empty()).interval

    def get_current_time(self):
        return self.stub.getCurrentTime(bmi_pb2.Empty()).time

    def get_start_time(self):
        return self.stub.getStartTime(bmi_pb2.Empty()).time

    def get_end_time(self):
        return self.stub.getEndTime(bmi_pb2.Empty()).time

    def get_var_grid(self, var_name):
        return self.stub.getVarGrid(bmi_pb2.GetVarRequest(name=var_name)).grid_id

    def get_var_type(self, var_name):
        return str(self.stub.getVarType(bmi_pb2.GetVarRequest(name=var_name)).type)

    def get_var_itemsize(self, var_name):
        return self.stub.getVarItemSize(bmi_pb2.GetVarRequest(name=var_name)).size

    def get_var_units(self, var_name):
        return str(self.stub.getVarUnits(bmi_pb2.GetVarRequest(name=var_name)).units)

    def get_var_nbytes(self, var_name):
        return self.stub.getVarNBytes(bmi_pb2.GetVarRequest(name=var_name)).nbytes

    def get_value(self, var_name):
        response = self.stub.getValue(bmi_pb2.GetVarRequest(name=var_name))
        return BmiClient.make_array(response)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def get_value_at_indices(self, var_name, indices):
        response = self.stub.getValue(bmi_pb2.GetValueAtIndicesRequest(name=var_name, indices=indices))
        return BmiClient.make_array(response)

    def set_value(self, var_name, src):
        request = None
        if src.dtype == numpy.int32:
            request = bmi_pb2.SetValueRequest(name=var_name, values_int=src.flatten(), shape=src.shape)
        elif src.dtype == numpy.float64:
            request = bmi_pb2.SetValueRequest(name=var_name, values_double=src.flatten(), shape=src.shape)
        self.stub.setValue(request)

    def set_value_at_indices(self, var_name, indices, src):
        request = None
        if src.dtype == numpy.int32:
            request = bmi_pb2.SetValueAtIndicesRequest(name=var_name, indices=indices, values_int=src)
        elif src.dtype == numpy.float64:
            request = bmi_pb2.SetValueRequest(name=var_name, indices=indices, values_double=src)
        self.stub.setValueAtIndices(request)

    def get_grid_size(self, grid_id):
        return self.stub.getGridSize(bmi_pb2.GridRequest(grid_id=grid_id)).size

    def get_grid_rank(self, grid_id):
        return self.stub.getGridRank(bmi_pb2.GridRequest(grid_id=grid_id)).rank

    def get_grid_type(self, grid_id):
        return str(self.stub.getGridType(bmi_pb2.GridRequest(grid_id=grid_id)).type)

    def get_grid_x(self, grid_id):
        return self.stub.getGridX(bmi_pb2.GridRequest(grid_id=grid_id)).coordinates

    def get_grid_y(self, grid_id):
        return self.stub.getGridY(bmi_pb2.GridRequest(grid_id=grid_id)).coordinates

    def get_grid_z(self, grid_id):
        return self.stub.getGridZ(bmi_pb2.GridRequest(grid_id=grid_id)).coordinates

    def get_grid_shape(self, grid_id):
        return self.stub.getGridShape(bmi_pb2.GridRequest(grid_id=grid_id)).shape

    def get_grid_spacing(self, grid_id):
        return self.stub.getGridSpacing(bmi_pb2.GridRequest(grid_id=grid_id)).spacing

    def get_grid_offset(self, grid_id):
        return self.stub.getGridOffset(bmi_pb2.GridRequest(grid_id=grid_id)).offsets

    def get_grid_connectivity(self, grid_id):
        return self.stub.getGridConnectivity(bmi_pb2.GridRequest(grid_id=grid_id)).links

    def get_grid_origin(self, grid_id):
        return self.stub.getGridOrigin(bmi_pb2.GridRequest(grid_id=grid_id)).origin

    @staticmethod
    def make_array(response):
        shape = response.shape
        if any(response.values_int):
            return numpy.reshape(response.values_int, shape)
        if any(response.values_double):
            return numpy.reshape(response.values_double, shape)
        return numpy.array([])
