import logging
import traceback

import numpy
from google.protobuf import any_pb2
from google.rpc import error_details_pb2, status_pb2, code_pb2
from grpc_status import rpc_status

from . import bmi_pb2, bmi_pb2_grpc

log = logging.getLogger(__name__)


class BmiLegacyServer02(bmi_pb2_grpc.BmiServiceServicer):
    """
    BMI Server class, wrapping an existing python implementation and exposing it via GRPC across the memory space (to
    listening client processes). The class takes a package, module and class name and instantiates the BMI
    implementation by assuming a default constructor with no arguments.

    For models implementing the bmi interface defined https://pypi.org/project/basic-modeling-interface/0.2/

    Args:
        model: Bmi model object which must be wrapped by grpc
        debug: If true then returns stacktrace in an error response.
                The stacktrace is returned in the trailing metadata as a DebugInfo (https://github.com/googleapis/googleapis/blob/07244bb797ddd6e0c1c15b02b4467a9a5729299f/google/rpc/error_details.proto#L46-L52) message.
    """

    def __init__(self, model, debug=False):
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

    def getValue(self, request, context):
        try:
            vals = self.bmi_model_.get_value(request.name)
            if vals.dtype == numpy.int32:
                return bmi_pb2.GetValueResponse(values_int=bmi_pb2.IntArrayMessage(values=vals.flatten()))
            if vals.dtype == numpy.float32:
                return bmi_pb2.GetValueResponse(values_float=bmi_pb2.FloatArrayMessage(values=vals.flatten()))
            if vals.dtype == numpy.float64:
                return bmi_pb2.GetValueResponse(values_double=bmi_pb2.DoubleArrayMessage(values=vals.flatten()))
            raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % vals.dtype)
        except Exception as e:
            self.exception_handler(e, context)

    def getValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def getValueAtIndices(self, request, context):
        try:
            indices = numpy.array(request.indices)
            vals = self.bmi_model_.get_value_at_indices(request.name, indices)
            if vals.dtype == numpy.int32:
                return bmi_pb2.GetValueAtIndicesResponse(values_int=bmi_pb2.IntArrayMessage(values=vals.flatten()))
            if vals.dtype == numpy.float32:
                return bmi_pb2.GetValueAtIndicesResponse(values_float=bmi_pb2.FloatArrayMessage(values=vals.flatten()))
            if vals.dtype == numpy.float64:
                return bmi_pb2.GetValueAtIndicesResponse(values_double=bmi_pb2.DoubleArrayMessage(values=vals.flatten()))
            raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % vals.dtype)
        except Exception as e:
            self.exception_handler(e, context)

    def setValue(self, request, context):
        try:
            if request.HasField("values_int"):
                self.bmi_model_.set_value(request.name, request.values_int.values)
            if request.HasField("values_float"):
                self.bmi_model_.set_value(request.name, request.values_float.values)
            if request.HasField("values_double"):
                self.bmi_model_.set_value(request.name, request.values_double.values)
            return bmi_pb2.Empty()
        except Exception as e:
            self.exception_handler(e, context)

    def setValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def setValueAtIndices(self, request, context):
        try:
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
            return bmi_pb2.GetGridShapeResponse(shape=self.bmi_model_.get_grid_shape(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridSpacing(self, request, context):
        try:
            return bmi_pb2.GetGridSpacingResponse(spacing=self.bmi_model_.get_grid_spacing(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridOrigin(self, request, context):
        try:
            return bmi_pb2.GetGridOriginResponse(origin=self.bmi_model_.get_grid_origin(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridX(self, request, context):
        try:
            return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_x(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridY(self, request, context):
        try:
            return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_y(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def getGridZ(self, request, context):
        try:
            return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_z(request.grid_id))
        except Exception as e:
            self.exception_handler(e, context)

    def __repr__(self) -> str:
        return self.bmi_model_.__repr__()
