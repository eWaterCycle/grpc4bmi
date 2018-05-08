import logging
import importlib

import numpy

import bmi_pb2
import bmi_pb2_grpc

log = logging.getLogger(__name__)


class BmiServer(bmi_pb2_grpc.BmiServiceServicer):

    def __init__(self, class_name, module_name, package_name=None):
        super(bmi_pb2_grpc.BmiServiceServicer, self).__init__()
        log.info("Starting BMI class %s in module %s..." % (module_name, class_name))
        class_ = getattr(importlib.import_module(module_name, package_name), class_name)
        self.bmi_model_ = class_()

    def initialize(self, request, context):
        ifile = str(request.config_file)
        if not ifile:
            ifile = None
        self.bmi_model_.initialize(ifile)
        return bmi_pb2.Empty()

    def update(self, request, context):
        self.bmi_model_.update()
        return bmi_pb2.Empty()

    def updateUntil(self, request, context):
        self.bmi_model_.update_until(request.until)
        return bmi_pb2.Empty()

    def updateFrac(self, request, context):
        self.bmi_model_.update_frac(request.frac)
        return bmi_pb2.Empty()

    def finalize(self, request, context):
        self.bmi_model_.finalize()
        return bmi_pb2.Empty()

    def runModel(self, request, context):
        self.bmi_model_.run_model()
        return bmi_pb2.Empty()

    def getComponentName(self, request, context):
        return bmi_pb2.GetComponentNameResponse(name=self.bmi_model_.get_component_name())

    def getInputVarNameCount(self, request, context):
        return bmi_pb2.GetVarNameCountResponse(count=len(self.bmi_model_.get_input_var_names()))

    def getOutputVarNameCount(self, request, context):
        return bmi_pb2.GetVarNameCountResponse(count=len(self.bmi_model_.get_output_var_names()))

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

    def getValue(self, request, context):
        vals = self.bmi_model_.get_value(request.name)
        if vals.dtype == int:
            return bmi_pb2.GetValueResponse(shape=vals.shape, values_int=vals.flatten())
        if vals.dtype == float:
            return bmi_pb2.GetValueResponse(shape=vals.shape, values_double=vals.flatten())
        raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % vals.dtype)

    def getValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def getValueAtIndices(self, request, context):
        vals = self.bmi_model_.get_value_at_indices(request.name, request.indices)
        if vals.dtype == numpy.int32:
            return bmi_pb2.GetValueAtIndicesResponse(values_int=vals)
        if vals.dtype == numpy.float64:
            return bmi_pb2.GetValueAtIndicesResponse(values_double=vals)
        raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % vals.dtype)

    def setValue(self, request, context):
        if any(request.values_int):
            self.bmi_model_.set_value(request.name, numpy.reshape(numpy.array(request.values_int, dtype=numpy.int32),
                                                                  request.shape))
            #TODO: warn if ALSO doubles are in the buffer
        elif any(request.values_double):
            self.bmi_model_.set_value(request.name,
                                      numpy.reshape(numpy.array(request.values_double, dtype=numpy.float64),
                                                    request.shape)
                                      )
        return bmi_pb2.Empty()

    def setValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def setValueAtIndices(self, request, context):
        if any(request.values_int):
            self.bmi_model_.set_value_at_indices(request.name, request.indices, numpy.array(request.values_int,
                                                                                            dtype=numpy.int32))
            #TODO: warn if ALSO doubles are in the buffer
        elif any(request.values_double):
            self.bmi_model_.set_value(request.name, request.indices, numpy.array(request.values_double,
                                                                                 dtype=numpy.float64))
        return bmi_pb2.Empty()

    def getGridSize(self, request, context):
        return bmi_pb2.GetGridSizeResponse(size=self.bmi_model_.get_grid_size(request.grid_id))

    def getGridRank(self, request, context):
        return bmi_pb2.GetGridRankResponse(rank=self.bmi_model_.get_grid_rank(request.grid_id))

    def getGridType(self, request, context):
        return bmi_pb2.GetGridTypeResponse(type=self.bmi_model_.get_grid_type(request.grid_id))

    def getGridShape(self, request, context):
        return bmi_pb2.GetGridShapeResponse(shape=self.bmi_model_.get_grid_shape(request.grid_id))

    def getGridSpacing(self, request, context):
        return bmi_pb2.GetGridSpacingResponse(spacing=self.bmi_model_.get_grid_spacing(request.grid_id))

    def getGridOrigin(self, request, context):
        return bmi_pb2.GetGridOriginResponse(origin=self.bmi_model_.get_grid_spacing(request.grid_id))

    def getGridX(self, request, context):
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_spacing(request.grid_id))

    def getGridY(self, request, context):
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_spacing(request.grid_id))

    def getGridZ(self, request, context):
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_spacing(request.grid_id))

    def getGridCellCount(self, request, context):
        return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_cell_count(request.grid_id))

    def getGridPointCount(self, request, context):
        return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_cell_count(request.grid_id))

    def getGridVertexCount(self, request, context):
        return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_cell_count(request.grid_id))

    def getGridConnectivity(self, request, context):
        return bmi_pb2.GetGridConnectivityResponse(links=self.bmi_model_.get_grid_cell_count(request.grid_id))

    def getGridOffset(self, request, context):
        return bmi_pb2.GetGridOffsetResponse(offsets=self.bmi_model_.get_grid_offset(request.grid_id))


