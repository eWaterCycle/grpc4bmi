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

grpc::Status BmiGRPCService::getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response) const
{
    response->set_name(this->bmi->GetComponentName());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response) const
{
    response->set_count(this->bmi->GetInputVarNames().size());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response) const
{
    response->set_count(this->bmi->GetOutputVarNames().size());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const
{
    std::vector<std::string> input_vars = this->bmi->GetInputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < input_vars.size(); i++)
    {
        response->set_names(i,input_vars[i]);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const
{
    std::vector<std::string> output_vars = this->bmi->GetOutputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < output_vars.size(); i++)
    {
        response->set_names(i,output_vars[i]);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response) const
{
    response->set_units(this->bmi->GetTimeUnits());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response) const
{
    response->set_interval(this->bmi->GetTimeStep());
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const
{
    response->set_time(this->bmi->GetCurrentTime());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const
{
    response->set_time(this->bmi->GetStartTime());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const
{
    response->set_time(this->bmi->GetEndTime());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response) const
{
    response->set_grid_id(this->bmi->GetVarGrid(request->name()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response) const
{
    response->set_type(this->bmi->GetVarType(request->name()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response) const
{
    response->set_size(this->bmi->GetVarItemSize(request->name()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response) const
{
    response->set_units(this->bmi->GetVarUnits(request->name()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response) const
{
    response->set_nbytes(this->bmi->GetVarNbytes(request->name()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response) const
{
    char typechar = this->find_type(request->name());
    response->set_shape(this->bmi->GetGridShape(this->))
    if (typechar == 'i')
    {
        values = this->bmi->get_values<int>(request->name());
        for(typename std::vector<int>::size_type i = 0; i < values.size(); i++)
        {
            
        }
        response->mutable_values_int()
    }

    response->set_values();
    return grpc::Status::OK;
}
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

char BmiGRPCService::find_type(const std::string& varname) const
{
    std::locale loc;
    std::string vartype = std::tolower(this->bmi->GetVarType(varname), loc);
    std::vector<std::string>inttypes = {"int", "int16", "int32", "int64"};
    if(std::find(inttypes.begin(), inttypes.end(), vartype) != inttypes.end())
    {
        return 'i';
    }
    std::vector<std::string>flttypes = {"float", "float32"};
    if(std::find(flttypes.begin(), flttypes.end(), vartype) != flttypes.end())
    {
        return 'f';
    }
    std::vector<std::string>dbltypes = {"double", "float64"};
    if(std::find(dbltypes.begin(), dbltypes.end(), vartype) != dbltypes.end())
    {
        return 'd';
    }
    throw std::invalid_argument("Could not match the variable type " + vartype + " of variable " + varname + "to integer, float or double");
}
