import logging
import importlib

import numpy

import bmi_pb2
import bmi_pb2_grpc

log = logging.getLogger(__name__)


class BmiServer(bmi_pb2_grpc.BmiServiceServicer):

    """
    BMI Server class, wrapping an existing python implementation and exposing it via GRPC across the memory space (to
    listening client processes). The class takes a package, module and class name and instantiates the BMI
    implementation by assuming a default constructor with no arguments.
    """

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
        if vals.dtype == numpy.int32:
            return bmi_pb2.GetValueResponse(shape=vals.shape, values_int=vals.flatten())
        if vals.dtype == numpy.float64:
            return bmi_pb2.GetValueResponse(shape=vals.shape, values_double=vals.flatten())
        raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % vals.dtype)

    def getValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    def getValueAtIndices(self, request, context):
        indices = request.indices
        index_size = request.index_size
        if index_size == 2:
            num_indices = len(request.indices)/index_size
            indices = numpy.reshape(indices,(num_indices, index_size))
        vals = self.bmi_model_.get_value_at_indices(request.name, indices)
        if vals.dtype == numpy.int32:
            return bmi_pb2.GetValueAtIndicesResponse(values_int=vals.flatten(), shape=vals.shape)
        if vals.dtype == numpy.float64:
            return bmi_pb2.GetValueAtIndicesResponse(values_double=vals.flatten(), shape=vals.shape)
        raise NotImplementedError("Arrays with type %s cannot be transmitted through this GRPC channel" % vals.dtype)

    # TODO: warn if both ints and doubles are in the buffer
    def setValue(self, request, context):
        if any(request.values_int):
            array = numpy.reshape(numpy.array(request.values_int, dtype=numpy.int32), request.shape)
            self.bmi_model_.set_value(request.name, array)
        elif any(request.values_double):
            array = numpy.reshape(numpy.array(request.values_double, dtype=numpy.float64), request.shape)
            self.bmi_model_.set_value(request.name, array)
        return bmi_pb2.Empty()

    def setValuePtr(self, request, context):
        raise NotImplementedError("Array references cannot be transmitted through this GRPC channel")

    # TODO: warn if both ints and doubles are in the buffer
    def setValueAtIndices(self, request, context):
        index_size = request.index_size
        num_indices = len(request.indices)/index_size
        index_array = numpy.reshape(request.indices, newshape=(num_indices, index_size))
        if any(request.values_int):
            array = numpy.array(request.values_int, dtype=numpy.int32)
            self.bmi_model_.set_value_at_indices(request.name, indices=index_array, src=array)
        elif any(request.values_double):
            array = numpy.array(request.values_double, dtype=numpy.float64)
            self.bmi_model_.set_value_at_indices(request.name, indices=index_array, src=array)
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
        return bmi_pb2.GetGridOriginResponse(origin=self.bmi_model_.get_grid_origin(request.grid_id))

    def getGridX(self, request, context):
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_x(request.grid_id))

    def getGridY(self, request, context):
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_y(request.grid_id))

    def getGridZ(self, request, context):
        return bmi_pb2.GetGridPointsResponse(coordinates=self.bmi_model_.get_grid_z(request.grid_id))

    # def getGridCellCount(self, request, context):
    #     return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_cell_count(request.grid_id))
    #
    # def getGridPointCount(self, request, context):
    #     return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_point_count(request.grid_id))
    #
    # def getGridVertexCount(self, request, context):
    #     return bmi_pb2.GetCountResponse(count=self.bmi_model_.get_grid_vertex_count(request.grid_id))

    def getGridConnectivity(self, request, context):
        return bmi_pb2.GetGridConnectivityResponse(links=self.bmi_model_.get_grid_connectivity(request.grid_id))

    def getGridOffset(self, request, context):
        return bmi_pb2.GetGridOffsetResponse(offsets=self.bmi_model_.get_grid_offset(request.grid_id))


