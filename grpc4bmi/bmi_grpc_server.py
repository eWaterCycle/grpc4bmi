import logging

import numpy
from bmipy import Bmi
from grpc_status import rpc_status
from google.protobuf import any_pb2
from google.rpc import code_pb2, status_pb2, error_details_pb2
import traceback

from grpc4bmi.reserve import reserve_values, reserve_grid_shape, reserve_grid_nodes, reserve_grid_padding, \
    reserve_values_at_indices
from . import bmi_pb2, bmi_pb2_grpc

log = logging.getLogger(__name__)


class BmiServer(bmi_pb2_grpc.BmiServiceServicer):
    """
    BMI Server class, wrapping an existing python implementation and exposing it via GRPC across the memory space (to
    listening client processes). The class takes a package, module and class name and instantiates the BMI
    implementation by assuming a default constructor with no arguments.

    Args:
        model: Bmi model object which must be wrapped by grpc
        debug: If true then returns stacktrace in an error response.
                The stacktrace is returned in the trailing metadata as a DebugInfo (https://github.com/googleapis/googleapis/blob/07244bb797ddd6e0c1c15b02b4467a9a5729299f/google/rpc/error_details.proto#L46-L52) message.
    """

    def __init__(self, model, debug=False):
        # type: (BmiServer, Bmi, bool) -> None
        super(bmi_pb2_grpc.BmiServiceServicer, self).__init__()
        self.bmi_model_ = model
        self.debug = debug

    def exception_handler(self, exc, context):
        log.exception(exc)
        detail = any_pb2.Any()
        if self.debug:
            detail.Pack(
                error_details_pb2.DebugInfo(
                    stack_entries=traceback.format_stack(),
                    detail=repr(exc)
                )
            )
        status = status_pb2.Status(
            code=code_pb2.INTERNAL,
            message=str(exc),
            details=[detail]
        )
        context.abort_with_status(rpc_status.to_status(status))

    def initialize(self, request, context):
        ifile = str(request.config_file)
        if not ifile:
            ifile = None
        try:
            self.bmi_model_.initialize(ifile)
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def update(self, request, context):
        try:
            self.bmi_model_.update()
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def updateUntil(self, request, context):
        try:
            self.bmi_model_.update_until(request.time)
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def finalize(self, request, context):
        try:
            self.bmi_model_.finalize()
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def getComponentName(self, request, context):
        try:
            return bmi_pb2.GetComponentNameResponse(name=self.bmi_model_.get_component_name())
        except Exception as e:
            self.exception_handler(e, context)

    def getInputItemCount(self, request, context):
        try:
            return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_input_item_count())
        except Exception as e:
            self.exception_handler(e, context)

    def getOutputItemCount(self, request, context):
        try:
            return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_output_item_count())
        except Exception as e:
            self.exception_handler(e, context)

    def getInputVarNames(self, request, context):
        try:
            return bmi_pb2.GetVarNamesResponse(names=self.bmi_model_.get_input_var_names())
        except Exception as e:
            self.exception_handler(e, context)

    def getOutputVarNames(self, request, context):
        try:
            return bmi_pb2.GetVarNamesResponse(names=self.bmi_model_.get_output_var_names())
        except Exception as e:
            self.exception_handler(e, context)

    def getTimeUnits(self, request, context):
        try:
            return bmi_pb2.GetTimeUnitsResponse(units=self.bmi_model_.get_time_units())
        except Exception as e:
            self.exception_handler(e, context)

    def getTimeStep(self, request, context):
        try:
            return bmi_pb2.GetTimeStepResponse(interval=self.bmi_model_.get_time_step())
        except Exception as e:
            self.exception_handler(e, context)

    def getCurrentTime(self, request, context):
        try:
            return bmi_pb2.GetTimeResponse(time=self.bmi_model_.get_current_time())
        except Exception as e:
            self.exception_handler(e, context)

    def getStartTime(self, request, context):
        try:
            return bmi_pb2.GetTimeResponse(time=self.bmi_model_.get_start_time())
        except Exception as e:
            self.exception_handler(e, context)

    def getEndTime(self, request, context):
        try:
            return bmi_pb2.GetTimeResponse(time=self.bmi_model_.get_end_time())
        except Exception as e:
            self.exception_handler(e, context)

    def getVarGrid(self, request, context):
        try:
            return bmi_pb2.GetVarGridResponse(grid_id=self.bmi_model_.get_var_grid(request.name))
        except Exception as e:
            self.exception_handler(e, context)

    def getVarType(self, request, context):
        try:
            return bmi_pb2.GetVarTypeResponse(type=self.bmi_model_.get_var_type(request.name))
        except Exception as e:
            self.exception_handler(e, context)

    def getVarItemSize(self, request, context):
        try:
            return bmi_pb2.GetVarItemSizeResponse(size=self.bmi_model_.get_var_itemsize(request.name))
        except Exception as e:
            self.exception_handler(e, context)

    def getVarUnits(self, request, context):
        try:
            return bmi_pb2.GetVarUnitsResponse(units=self.bmi_model_.get_var_units(request.name))
        except Exception as e:
            self.exception_handler(e, context)

    def getVarNBytes(self, request, context):
        try:
            return bmi_pb2.GetVarNBytesResponse(nbytes=self.bmi_model_.get_var_nbytes(request.name))
        except Exception as e:
            self.exception_handler(e, context)

    def getVarLocation(self, request, context):
        location_name = self.bmi_model_.get_var_location(request.name)
        location = bmi_pb2.GetVarLocationResponse.Location.Value(location_name.upper())
        return bmi_pb2.GetVarLocationResponse(location=location)

    def getValue(self, request, context):
        try:
            values = reserve_values(self.bmi_model_, request.name)
            values = self.bmi_model_.get_value(request.name, values)
            if values.dtype in (numpy.int64, numpy.int32, numpy.int16):
                return bmi_pb2.GetValueResponse(values_int=bmi_pb2.IntArrayMessage(values=values.flatten()))
            if values.dtype in (numpy.float32, numpy.float16):
                return bmi_pb2.GetValueResponse(values_float=bmi_pb2.FloatArrayMessage(values=values.flatten()))
            if values.dtype == numpy.float64:
                return bmi_pb2.GetValueResponse(values_double=bmi_pb2.DoubleArrayMessage(values=values.flatten()))
            raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % values.dtype)
        except Exception as e:
            self.exception_handler(e, context)

    def getValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def getValueAtIndices(self, request, context):
        try:
            indices = numpy.array(request.indices)
            values = reserve_values_at_indices(self.bmi_model_, request.name, indices)
            values = self.bmi_model_.get_value_at_indices(request.name, values, indices)
            if values.dtype in (numpy.int64, numpy.int32, numpy.int16):
                return bmi_pb2.GetValueAtIndicesResponse(values_int=bmi_pb2.IntArrayMessage(values=values.flatten()))
            if values.dtype in (numpy.float32, numpy.float16):
                return bmi_pb2.GetValueAtIndicesResponse(values_float=bmi_pb2.FloatArrayMessage(values=values.flatten()))
            if values.dtype == numpy.float64:
                return bmi_pb2.GetValueAtIndicesResponse(values_double=bmi_pb2.DoubleArrayMessage(values=values.flatten()))
            raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % values.dtype)
        except Exception as e:
            self.exception_handler(e, context)

    def setValue(self, request, context):
        try:
            if request.HasField("values_int"):
                array = numpy.array(request.values_int.values, dtype=numpy.int64)
                self.bmi_model_.set_value(request.name, array)
            if request.HasField("values_float"):
                array = numpy.array(request.values_float.values, dtype=numpy.float32)
                self.bmi_model_.set_value(request.name, array)
            if request.HasField("values_double"):
                array = numpy.array(request.values_double.values, dtype=numpy.float64)
                self.bmi_model_.set_value(request.name, array)
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def setValueAtIndices(self, request, context):
        try:
            index_array = numpy.array(request.indices)
            if request.HasField("values_int"):
                array = numpy.array(request.values_int.values, dtype=numpy.int64)
                self.bmi_model_.set_value_at_indices(request.name, index_array, array)
            if request.HasField("values_float"):
                array = numpy.array(request.values_float.values, dtype=numpy.float32)
                self.bmi_model_.set_value_at_indices(request.name, index_array, array)
            if request.HasField("values_double"):
                array = numpy.array(request.values_double.values, dtype=numpy.float64)
                self.bmi_model_.set_value_at_indices(request.name, index_array, array)
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def getGridSize(self, request, context):
        try:
            return bmi_pb2.GetGridSizeResponse(size=self.bmi_model_.get_grid_size(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridRank(self, request, context):
        try:
            return bmi_pb2.GetGridRankResponse(rank=self.bmi_model_.get_grid_rank(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridType(self, request, context):
        try:
            return bmi_pb2.GetGridTypeResponse(type=self.bmi_model_.get_grid_type(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridShape(self, request, context):
        try:
            values = reserve_grid_shape(self.bmi_model_, request.grid_id)
            return bmi_pb2.GetGridShapeResponse(shape=self.bmi_model_.get_grid_shape(request.grid_id, values))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridSpacing(self, request, context):
        try:
            values = reserve_grid_padding(self.bmi_model_, request.grid_id)
            return bmi_pb2.GetGridSpacingResponse(spacing=self.bmi_model_.get_grid_spacing(request.grid_id, values))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridOrigin(self, request, context):
        try:
            values = reserve_grid_padding(self.bmi_model_, request.grid_id)
            return bmi_pb2.GetGridOriginResponse(origin=self.bmi_model_.get_grid_origin(request.grid_id, values))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridX(self, request, context):
        try:
            values = reserve_grid_nodes(self.bmi_model_, request.grid_id, 0)
            return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_x(request.grid_id, values))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridY(self, request, context):
        try:
            values = reserve_grid_nodes(self.bmi_model_, request.grid_id, 1)
            return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_y(request.grid_id, values))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridZ(self, request, context):
        try:
            values = reserve_grid_nodes(self.bmi_model_, request.grid_id, 2)
            return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_z(request.grid_id, values))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridNodeCount(self, request, context):
        try:
            return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_node_count(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridEdgeCount(self, request, context):
        try:
            return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_edge_count(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridFaceCount(self, request, context):
        try:
            return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_face_count(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridEdgeNodes(self, request, context):
        try:
            size = 2 * self.bmi_model_.get_grid_edge_count(request.grid_id)
            links = numpy.empty(size, dtype=numpy.int64)
            links = self.bmi_model_.get_grid_edge_nodes(request.grid_id, links)
            return bmi_pb2.GetGridEdgeNodesResponse(edge_nodes=links)
        except Exception as e:
            self.exception_handler(e, context)

    def _get_grid_nodes_per_face(self, grid_id):
        size = self.bmi_model_.get_grid_face_count(grid_id)
        links = numpy.empty(size, dtype=numpy.int64)
        return self.bmi_model_.get_grid_nodes_per_face(grid_id, links)

    def getGridFaceNodes(self, request, context):
        try:
            nodes_per_face = self._get_grid_nodes_per_face(request.grid_id)
            size = numpy.sum(nodes_per_face)
            links = numpy.empty(size, dtype=numpy.int64)
            links = self.bmi_model_.get_grid_face_nodes(request.grid_id, links)
            return bmi_pb2.GetGridFaceNodesResponse(face_nodes=links)
        except Exception as e:
            self.exception_handler(e, context)

    def getGridFaceEdges(self, request, context):
        try:
            nodes_per_face = self._get_grid_nodes_per_face(request.grid_id)
            size = numpy.sum(nodes_per_face)
            face_edges = numpy.empty(size, dtype=numpy.int64)
            face_edges = self.bmi_model_.get_grid_face_edges(request.grid_id, face_edges)
            return bmi_pb2.GetGridFaceEdgesResponse(face_edges=face_edges)
        except Exception as e:
            self.exception_handler(e, context)

    def getGridNodesPerFace(self, request, context):
        try:
            nodes_per_face = self._get_grid_nodes_per_face(request.grid_id)
            return bmi_pb2.GetGridNodesPerFaceResponse(nodes_per_face=nodes_per_face)
        except Exception as e:
            self.exception_handler(e, context)

    def __repr__(self):
        # type: (BmiServer) -> str
        return self.bmi_model_.__repr__()
