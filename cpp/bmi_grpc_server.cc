#include "bmi_grpc_server.h"


BmiGRPCService::BmiGRPCService(BmiCppBase* const bmi_):bmi(bmi_){}

BmiGRPCService::~BmiGRPCService(){}

grpc::Status BmiGRPCService::initialize(grpc::ServerContext* context, const bmi::InitializeRequest* request, bmi::Empty* response)
{
    this->bmi->Initialize(request->config_file());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::update(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response)
{
    this->bmi->Update();
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::updateUntil(grpc::ServerContext* context, const bmi::UpdateUntilRequest* request, bmi::Empty* response)
{
    this->bmi->UpdateUntil(request->until());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::updateFrac(grpc::ServerContext* context, const bmi::UpdateFracRequest* request, bmi::Empty* response)
{
    this->bmi->UpdateFrac(request->frac());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::runModel(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response)
{
    this->bmi->runModel();
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response)
{
    response->set_name(this->bmi->GetComponentName());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response)
{
    response->set_count(this->bmi->GetInputVarNames().size());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response)
{
    response->set_count(this->bmi->GetOutputVarNames().size());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response)
{
    std::vector<std::string> input_vars = this->bmi->GetInputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < input_vars.size(); i++)
    {
        response->set_names(i,input_vars[i]);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response)
{
    std::vector<std::string> output_vars = this->bmi->GetOutputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < output_vars.size(); i++)
    {
        response->set_names(i,output_vars[i]);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response);
grpc::Status BmiGRPCService::getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response);
grpc::Status BmiGRPCService::getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response);
grpc::Status BmiGRPCService::getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response);
grpc::Status BmiGRPCService::getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response);
grpc::Status BmiGRPCService::getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response);
grpc::Status BmiGRPCService::getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response);
grpc::Status BmiGRPCService::getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response);
grpc::Status BmiGRPCService::getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response);
grpc::Status BmiGRPCService::getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response);
grpc::Status BmiGRPCService::getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response);
grpc::Status BmiGRPCService::getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response);
grpc::Status BmiGRPCService::getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response);
grpc::Status BmiGRPCService::setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response);
grpc::Status BmiGRPCService::setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response);
grpc::Status BmiGRPCService::setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response);
grpc::Status BmiGRPCService::getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response);
grpc::Status BmiGRPCService::getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response);
grpc::Status BmiGRPCService::getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response);
grpc::Status BmiGRPCService::getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response);
grpc::Status BmiGRPCService::getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response);
grpc::Status BmiGRPCService::getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response);
grpc::Status BmiGRPCService::getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response);
grpc::Status BmiGRPCService::getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response);
grpc::Status BmiGRPCService::getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response);
grpc::Status BmiGRPCService::getGridCellCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response);
grpc::Status BmiGRPCService::getGridPointCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response);
grpc::Status BmiGRPCService::getGridVertexCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response);
grpc::Status BmiGRPCService::getGridConnectivity(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridConnectivityResponse* response);
grpc::Status BmiGRPCService::getGridOffset(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOffsetResponse* response);
