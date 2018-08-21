#ifndef BMI_GRPC_SERVER_H_INCLUDED
#define BMI_GRPC_SERVER_H_INCLUDED

#include "bmi.grpc.pb.h"
#include "bmi_cpp_base.h"

class BmiGRPCService final: public grpc::Service
{
    public:
        BmiGRPCService(BmiCppBase* const bmi_);
        ~BmiGRPCService();
        grpc::Status initialize(grpc::ServerContext* context, const bmi::InitializeRequest* request, bmi::Empty* response);
        grpc::Status update(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response);
        grpc::Status updateUntil(grpc::ServerContext* context, const bmi::UpdateUntilRequest* request, bmi::Empty* response);
        grpc::Status updateFrac(grpc::ServerContext* context, const bmi::UpdateFracRequest* request, bmi::Empty* response);
        grpc::Status runModel(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response);
        grpc::Status getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response);
        grpc::Status getInputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response);
        grpc::Status getOutputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response);
        grpc::Status getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response);
        grpc::Status getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response);
        grpc::Status getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response);
        grpc::Status getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response);
        grpc::Status getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response);
        grpc::Status getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response);
        grpc::Status getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response);
        grpc::Status getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response);
        grpc::Status getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response);
        grpc::Status getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response);
        grpc::Status getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response);
        grpc::Status getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response);
        grpc::Status getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response);
        grpc::Status getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response);
        grpc::Status getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response);
        grpc::Status setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response);
        grpc::Status setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response);
        grpc::Status setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response);
        grpc::Status getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response);
        grpc::Status getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response);
        grpc::Status getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response);
        grpc::Status getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response);
        grpc::Status getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response);
        grpc::Status getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response);
        grpc::Status getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response);
        grpc::Status getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response);
        grpc::Status getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response);
        grpc::Status getGridCellCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response);
        grpc::Status getGridPointCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response);
        grpc::Status getGridVertexCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response);
        grpc::Status getGridConnectivity(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridConnectivityResponse* response);
        grpc::Status getGridOffset(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOffsetResponse* response);
    private:
        BmiCppBase* const bmi;
};

#endif
