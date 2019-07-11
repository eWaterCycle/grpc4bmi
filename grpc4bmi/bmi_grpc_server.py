import logging

import numpy
from bmipy import Bmi

from . import bmi_pb2, bmi_pb2_grpc

log = logging.getLogger(__name__)


class BmiServer(bmi_pb2_grpc.BmiServiceServicer):
    """
    BMI Server class, wrapping an existing python implementation and exposing it via GRPC across the memory space (to
    listening client processes). The class takes a package, module and class name and instantiates the BMI
    implementation by assuming a default constructor with no arguments.
    """

    def __init__(self, model):
        # type: (BmiServer, Bmi) -> None
        super(bmi_pb2_grpc.BmiServiceServicer, self).__init__()
        self.bmi_model_ = model

    def initialize(self, request, context):
        ifile = str(request.config_file)
        if not ifile:
            ifile = None
        self.bmi_model_.initialize(ifile)
        return bmi_pb2.Empty()

    def update(self, request, context):
        self.bmi_model_.update()
        return bmi_pb2.Empty()

    def finalize(self, request, context):
        self.bmi_model_.finalize()
        return bmi_pb2.Empty()

    def getComponentName(self, request, context):
        return bmi_pb2.GetComponentNameResponse(name=self.bmi_model_.get_component_name())

    def getInputVarNames(self, request, context):
        return bmi_pb2.GetVarNamesResponse(names=self.bmi_model_.get_input_var_names())

    def getOutputVarNames(self, request, context):
        return bmi_pb2.GetVarNamesResponse(names=self.bmi_model_.get_output_var_names())

    def getTimeUnits(self, request, context):
        return bmi_pb2.GetTimeUnitsResponse(units=self.bmi_model_.get_time_units())

    def getTimeStep(self, request, context):
        return bmi_pb2.GetTimeStepResponse(interval=self.bmi_model_.get_time_step())

    def getCurrentTime(self, request, context):
        return bmi_pb2.GetTimeResponse(time=self.bmi_model_.get_current_time())

    def getStartTime(self, request, context):
        return bmi_pb2.GetTimeResponse(time=self.bmi_model_.get_start_time())

    def getEndTime(self, request, context):
        return bmi_pb2.GetTimeResponse(time=self.bmi_model_.get_end_time())

    def getVarGrid(self, request, context):
        return bmi_pb2.GetVarGridResponse(grid_id=self.bmi_model_.get_var_grid(request.name))

    def getVarType(self, request, context):
        return bmi_pb2.GetVarTypeResponse(type=self.bmi_model_.get_var_type(request.name))

    def getVarItemSize(self, request, context):
        return bmi_pb2.GetVarItemSizeResponse(size=self.bmi_model_.get_var_itemsize(request.name))

    def getVarUnits(self, request, context):
        return bmi_pb2.GetVarUnitsResponse(units=self.bmi_model_.get_var_units(request.name))

    def getVarNBytes(self, request, context):
        return bmi_pb2.GetVarNBytesResponse(nbytes=self.bmi_model_.get_var_nbytes(request.name))

    def getVarLocation(self, request, context):
        location = self.bmi_model_.get_var_location(request.name)
        lookup = {
            "node": bmi_pb2.GetVarLocationResponse.Location.NODE,
            "edge": bmi_pb2.GetVarLocationResponse.Location.EDGE,
            "face": bmi_pb2.GetVarLocationResponse.Location.FACE,
        }
        return bmi_pb2.GetVarLocationResponse(location=lookup[location])

    def _reserve_values(self, name):
        dtype = self.bmi_model_.get_var_type(name)
        item_size = self.bmi_model_.get_var_itemsize(name)
        total_size = self.bmi_model_.get_var_nbytes(name)
        size = total_size // item_size
        return numpy.empty(size, dtype=dtype)

    def getValue(self, request, context):
        values = self._reserve_values(request.name)
        values = self.bmi_model_.get_value(request.name, values)
        if values.dtype == numpy.int32:
            return bmi_pb2.GetValueResponse(values_int=bmi_pb2.IntArrayMessage(values=values.flatten()))
        if values.dtype == numpy.float32:
            return bmi_pb2.GetValueResponse(values_float=bmi_pb2.FloatArrayMessage(values=values.flatten()))
        if values.dtype == numpy.float64:
            return bmi_pb2.GetValueResponse(values_double=bmi_pb2.DoubleArrayMessage(values=values.flatten()))
        raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % values.dtype)

    def getValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def getValueAtIndices(self, request, context):
        indices = numpy.array(request.indices)
        values = numpy.empty(len(indices), dtype=self.bmi_model_.get_var_type(request.name))
        values = self.bmi_model_.get_value_at_indices(request.name, values, indices)
        if values.dtype == numpy.int32:
            return bmi_pb2.GetValueAtIndicesResponse(values_int=bmi_pb2.IntArrayMessage(values=values.flatten()))
        if values.dtype == numpy.float32:
            return bmi_pb2.GetValueAtIndicesResponse(values_float=bmi_pb2.FloatArrayMessage(values=values.flatten()))
        if values.dtype == numpy.float64:
            return bmi_pb2.GetValueAtIndicesResponse(values_double=bmi_pb2.DoubleArrayMessage(values=values.flatten()))
        raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % values.dtype)

    def setValue(self, request, context):
        if request.HasField("values_int"):
            self.bmi_model_.set_value(request.name, request.values_int.values)
        if request.HasField("values_float"):
            self.bmi_model_.set_value(request.name, request.values_float.values)
        if request.HasField("values_double"):
            self.bmi_model_.set_value(request.name, request.values_double.values)
        return bmi_pb2.Empty()

    def setValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def setValueAtIndices(self, request, context):
        index_array = numpy.array(request.indices)
        if request.HasField("values_int"):
            array = numpy.array(request.values_int.values, dtype=numpy.int32)
            self.bmi_model_.set_value_at_indices(request.name, index_array, array)
        if request.HasField("values_float"):
            array = numpy.array(request.values_int.values, dtype=numpy.float32)
            self.bmi_model_.set_value_at_indices(request.name, index_array, array)
        if request.HasField("values_double"):
            array = numpy.array(request.values_double.values, dtype=numpy.float64)
            self.bmi_model_.set_value_at_indices(request.name, index_array, array)
        return bmi_pb2.Empty()

    def getGridSize(self, request, context):
        return bmi_pb2.GetGridSizeResponse(size=self.bmi_model_.get_grid_size(request.grid_id))

    def getGridRank(self, request, context):
        return bmi_pb2.GetGridRankResponse(rank=self.bmi_model_.get_grid_rank(request.grid_id))

    def getGridType(self, request, context):
        return bmi_pb2.GetGridTypeResponse(type=self.bmi_model_.get_grid_type(request.grid_id))

    def _reserve_grid_values(self, grid_id):
        return numpy.empty(self.bmi_model_.get_grid_rank(grid_id), dtype=numpy.int32)

    def getGridShape(self, request, context):
        values = self._reserve_grid_values(request.grid_id)
        return bmi_pb2.GetGridShapeResponse(shape=self.bmi_model_.get_grid_shape(request.grid_id, values))

    def getGridSpacing(self, request, context):
        values = self._reserve_grid_values(request.grid_id)
        return bmi_pb2.GetGridSpacingResponse(spacing=self.bmi_model_.get_grid_spacing(request.grid_id, values))

    def getGridOrigin(self, request, context):
        values = self._reserve_grid_values(request.grid_id)
        return bmi_pb2.GetGridOriginResponse(origin=self.bmi_model_.get_grid_origin(request.grid_id, values))

    def _reserve_shape(self, grid_id, dim_index):
        shape = self.bmi_model_.get_grid_shape(grid_id, self._reserve_grid_values(grid_id))
        return numpy.empty(shape[dim_index], dtype=numpy.float64)

    def getGridX(self, request, context):
        values = self._reserve_shape(request.grid_id, 0)
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_x(request.grid_id, values))

    def getGridY(self, request, context):
        values = self._reserve_shape(request.grid_id, 1)
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_y(request.grid_id, values))

    def getGridZ(self, request, context):
        values = self._reserve_shape(request.grid_id, 2)
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_z(request.grid_id, values))

    def getGridNodeCount(self, request, context):
        return bmi_pb2.GetGridElementCountResponse(count=self.bmi_model_.get_grid_node_count(request.grid_id))

    def getGridEdgeCount(self, request, context):
        return bmi_pb2.GetGridElementCountResponse(count=self.bmi_model_.get_grid_edge_count(request.grid_id))

    def getGridFaceCount(self, request, context):
        return bmi_pb2.GetGridElementCountResponse(count=self.bmi_model_.get_grid_edge_count(request.grid_id))

    def getGridEdgeNodes(self, request, context):
        size = 2 * self.bmi_model_.get_grid_node_count(request.grid_id)
        links = numpy.empty(size, dtype=numpy.int64)
        links = self.bmi_model_.get_grid_edge_nodes(request.grid_id, links)
        return bmi_pb2.GetGridEdgeNodesResponse(links=links)

    def getGridFaceNodes(self, request, context):
        nodes_per_face = self._get_grid_nodes_per_face(request.grid_id)
        size = numpy.sum(nodes_per_face)
        links = numpy.empty(size, dtype=numpy.int64)
        links = self.bmi_model_.get_grid_face_nodes(request.grid_id, links)
        return bmi_pb2.GetGridFaceNodesResponse(links=links)

    def _get_grid_nodes_per_face(self, grid_id):
        size = self.bmi_model_.get_grid_face_count(grid_id)
        links = numpy.empty(size, dtype=numpy.int64)
        return self.bmi_model_.get_grid_nodes_per_face(grid_id, links)

    def getGridNodesPerFace(self, request, context):
        links = self._get_grid_nodes_per_face(request.grid_id)
        return bmi_pb2.GetGridNodesPerFaceResponse(links=links)
