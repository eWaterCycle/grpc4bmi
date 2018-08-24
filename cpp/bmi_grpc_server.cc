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
    for(std::vector<std::string>::const_iterator it input_vars.begin(); it != input_vars.end(); it++)
    {
        response->add_names(*it);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const
{
    std::vector<std::string> output_vars = this->bmi->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it output_vars.begin(); it != output_vars.end(); it++)
    {
        response->add_names(*it);
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
    if (typechar == 'i')
    {
        std::vector<int> values = this->bmi->get_values<int>(request->name());
        response->mutable_values_int()->Resize(values.size());
        std::copy(values.begin(), values.end(),response->mutable_values_int()->begin());
    }
    if (typechar == 'f')
    {
        std::vector<float> values = this->bmi->get_values<float>(request->name());
        response->mutable_values_float()->Resize(values.size());
        std::copy(values.begin(), values.end(),response->mutable_values_float()->begin());
    }
    if (typechar == 'd')
    {
        std::vector<double> values = this->bmi->get_values<double>(request->name());
        response->mutable_values_double()->Resize(values.size());
        std::copy(values.begin(), values.end(),response->mutable_values_double()->begin());
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response)
{
    throw std::exception("Passing references is not supported by this protocol");
}
grpc::Status BmiGRPCService::getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response)
{
    char typechar = this->find_type(request->name());
    std::vector<int> indices(request->indices().begin(),request->indices().end());
    if (typechar == 'i')
    {
        std::vector<int> values = this->bmi->get_values_at_indices<int>(request->name(), indices);
        response->mutable_values_int()->Resize(values.size());
        std::copy(values.begin(), values.end(),response->mutable_values_int()->begin());
    }
    if (typechar == 'f')
    {
        std::vector<float> values = this->bmi->get_values<float>(request->name());
        response->mutable_values_float()->Resize(values.size());
        std::copy(values.begin(), values.end(),response->mutable_values_float()->begin());
    }
    if (typechar == 'd')
    {
        std::vector<double> values = this->bmi->get_values<double>(request->name());
        response->mutable_values_double()->Resize(values.size());
        std::copy(values.begin(), values.end(),response->mutable_values_double()->begin());
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response)
{
    char typechar = this->find_type(request->name());
    if (typechar == 'i')
    {
        std::vector<int> values(request->values_int().size());
        std::copy(request->values_int().begin(), request->values_int().end(),values.begin());
        this->bmi->setValue<int>(request->name(), values);
    }
    if (typechar == 'f')
    {
        std::vector<float> values(request->values_float().size());
        std::copy(request->values_float().begin(), request->values_float().end(),values.begin());
        this->bmi->setValue<float>(request->name(), values);
    }
    if (typechar == 'd')
    {
        std::vector<double> values(request->values_double().size());
        std::copy(request->values_double().begin(), request->values_double().end(),values.begin());
        this->bmi->setValue<double>(request->name(), values);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response)
{
    throw std::exception("Passing references is not supported by this protocol");
}
grpc::Status BmiGRPCService::setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response)
{
    char typechar = this->find_type(request->name());
    std::vector<int> indices(request->indices().begin(),request->indices().end());
    if (typechar == 'i')
    {
        std::vector<int> values(indices.size());
        std::copy(request->values_int().begin(), request->values_int().end(),values.begin());
        this->bmi->setValueAtIndices<int>(request->name(), values, indices);
    }
    if (typechar == 'f')
    {
        std::vector<float> values(indices.size());
        std::copy(request->values_float().begin(), request->values_float().end(),values.begin());
        this->bmi->setValueAtIndices<float>(request->name(), values, indices);
    }
    if (typechar == 'd')
    {
        std::vector<double> values(indices.size());
        std::copy(request->values_double().begin(), request->values_double().end(),values.begin());
        this->bmi->setValueAtIndices<double>(request->name(), values, indices);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response)
{
    response->set_size(this->bmi->GetGridSize(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response)
{
    response->set_type(this->bmi->GetGridSize(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response)
{
    response->set_rank(this->bmi->GetGridSize(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response)
{
    std::vector<int> shape = this->bmi->GetGridShape(request->grid_id());
    for(std::vector<int>::const_iterator it = shape.begin(); it != shape.end(); ++it)
    {
        response->add_shape(*it);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response)
{
    std::vector<double> spacing = this->bmi->GetGridSpacing(request->grid_id());
    for(std::vector<double>::const_iterator it = spacing.begin(); it != spacing.end(); ++it)
    {
        response->add_spacing(*it);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response)
{
    std::vector<double> spacing = this->bmi->GetGridSpacing(request->grid_id());
    for(std::vector<double>::const_iterator it = spacing.begin(); it != spacing.end(); ++it)
    {
        response->add_spacing(*it);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response)
{
    std::vector<double> x_coords = this->bmi->GetGridX(request->grid_id());
    response->mutable_coordinates().Resize(x_coords.size());
    std::copy(x_coords.begin(), x_coords.end(), response->mutable_coordinates().begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response)
{
    std::vector<double> y_coords = this->bmi->GetGridY(request->grid_id());
    response->mutable_coordinates().Resize(y_coords.size());
    std::copy(y_coords.begin(), y_coords.end(), response->mutable_coordinates().begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response)
{
    std::vector<double> z_coords = this->bmi->GetGridZ(request->grid_id());
    response->mutable_coordinates().Resize(z_coords.size());
    std::copy(z_coords.begin(), z_coords.end(), response->mutable_coordinates().begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridCellCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response)
{
    response->set_count(this->bmi->GetGridCellCount(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridPointCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response)
{
    response->set_count(this->bmi->GetGridPointCount(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridVertexCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response)
{
    response->set_count(this->bmi->GetGridVertexCount(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridConnectivity(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridConnectivityResponse* response)
{
    std::vector<int> links = this->bmi->GetGridConnectivity(request->grid_id());
    response->mutable_links().Resize(links.size());
    std::copy(links.begin(), links.end(), response->mutable_links().begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridOffset(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOffsetResponse* response)
{
    std::vector<double> origin = this->bmi->GetGridOrigin(request->grid_id());
    for(std::vector<double>::const_iterator it = origin.begin(); it != origin.end(); ++it)
    {
        response->add_origin(*it);
    }
    return grpc::Status::OK;
}

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
