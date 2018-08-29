#ifndef BMI_GRPC_SERVER_H_INCLUDED
#define BMI_GRPC_SERVER_H_INCLUDED

#include "bmi.grpc.pb.h"
#include "bmi.h"

class BmiGRPCService final: public grpc::Service
{
    public:
        BmiGRPCService(Bmi* const bmi_);
        ~BmiGRPCService();
        grpc::Status initialize(grpc::ServerContext* context, const bmi::InitializeRequest* request, bmi::Empty* response);
        grpc::Status update(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response);
        grpc::Status updateUntil(grpc::ServerContext* context, const bmi::UpdateUntilRequest* request, bmi::Empty* response);
        grpc::Status updateFrac(grpc::ServerContext* context, const bmi::UpdateFracRequest* request, bmi::Empty* response);
        grpc::Status runModel(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response);
        grpc::Status getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response) const;
        grpc::Status getInputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response) const;
        grpc::Status getOutputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response) const;
        grpc::Status getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const;
        grpc::Status getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const;
        grpc::Status getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response) const;
        grpc::Status getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response) const;
        grpc::Status getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const;
        grpc::Status getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const;
        grpc::Status getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const;
        grpc::Status getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response) const;
        grpc::Status getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response) const;
        grpc::Status getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response) const;
        grpc::Status getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response) const;
        grpc::Status getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response) const;
        grpc::Status getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response) const;
        grpc::Status getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response);
        grpc::Status getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response) const;
        grpc::Status setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response);
        grpc::Status setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response);
        grpc::Status setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response);
        grpc::Status getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response) const;
        grpc::Status getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response) const;
        grpc::Status getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response) const;
        grpc::Status getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response) const;
        grpc::Status getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response) const;
        grpc::Status getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response) const;
        grpc::Status getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) const;
        grpc::Status getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) const;
        grpc::Status getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) const;
        grpc::Status getGridCellCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) const;
        grpc::Status getGridPointCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) const;
        grpc::Status getGridVertexCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) const;
        grpc::Status getGridConnectivity(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridConnectivityResponse* response) const;
        grpc::Status getGridOffset(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOffsetResponse* response) const;
    private:
        Bmi* const bmi;
        char find_type(const std::string& varname) const;
        static grpc::Status translate_status(int);
};

#endif
