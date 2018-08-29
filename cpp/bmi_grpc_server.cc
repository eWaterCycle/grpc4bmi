#include "bmi_grpc_server.h"


BmiGRPCService::BmiGRPCService(Bmi* const bmi_):bmi(bmi_){}

BmiGRPCService::~BmiGRPCService(){}

grpc::Status BmiGRPCService::initialize(grpc::ServerContext* context, const bmi::InitializeRequest* request, bmi::Empty* response)
{
    return BmiGRPCService::translate_status(this->bmi->initialize(request->config_file().c_str()));
}

grpc::Status BmiGRPCService::update(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response)
{
    return BmiGRPCService::translate_status(this->bmi->update());
}

grpc::Status BmiGRPCService::updateUntil(grpc::ServerContext* context, const bmi::UpdateUntilRequest* request, bmi::Empty* response)
{
    return BmiGRPCService::translate_status(this->bmi->update_until(request->until()));
}

grpc::Status BmiGRPCService::updateFrac(grpc::ServerContext* context, const bmi::UpdateFracRequest* request, bmi::Empty* response)
{
    return BmiGRPCService::translate_status(this->bmi->update_frac(request->frac()));
}

grpc::Status BmiGRPCService::runModel(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response)
{
    return BmiGRPCService::translate_status(this->bmi->run_model());
}

grpc::Status BmiGRPCService::getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response) const
{
    char name[2048];
    int status = this->bmi->get_component_name(name);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_name(std::string(name));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getInputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response) const
{
    // to be removed...
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNameCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNameCountResponse* response) const
{
    // to be removed...
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const
{
    int count;
    int status = this->bmi->get_input_var_name_count(&count);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    char** input_var_names = (char**)malloc(sizeof(char*) * count);
    char* data = (char*)malloc(sizeof(char) * count * 2048);
    for(int i = 0; i < count; i++)
    {
        input_var_names[i] = data + i * 2048;
    }
    status = this->bmi->get_input_var_names(input_var_names);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    for(int i = 0; i < count; i++)
    {
        response->add_names(std::string(input_var_names[i]));
    }
    free(data);
    free(input_var_names);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) const
{
    int count;
    int status = this->bmi->get_output_var_name_count(&count);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    char** output_var_names = (char**)malloc(sizeof(char*) * count);
    char* data = (char*)malloc(sizeof(char) * count * 2048);
    for(int i = 0; i < count; i++)
    {
        output_var_names[i] = data + i * 2048;
    }
    status = this->bmi->get_output_var_names(output_var_names);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    for(int i = 0; i < count; i++)
    {
        response->add_names(std::string(output_var_names[i]));
    }
    free(data);
    free(output_var_names);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response) const
{
    char units[2048];
    int status = this->bmi->get_time_units(units);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_units(std::string(units));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response) const
{
    double step;
    int status = this->bmi->get_time_step(&step);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_interval(step);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const
{
    double time;
    int status = this->bmi->get_current_time(&time);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_time(time);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const
{
    double time;
    int status = this->bmi->get_start_time(&time);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_time(time);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) const
{
    double time;
    int status = this->bmi->get_end_time(&time);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_time(time);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response) const
{
    int grid_id;
    int status = this->bmi->get_var_grid(request->name().c_str(), &grid_id);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_grid_id(grid_id);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response) const
{
    char type[2048];
    int status = this->bmi->get_var_type(request->name().c_str(), type);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_type(std::string(type));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response) const
{
    int size;
    int status = this->bmi->get_var_itemsize(request->name().c_str(), &size);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_size(size);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response) const
{
    char units[2048];
    int status = this->bmi->get_var_units(request->name().c_str(), units);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_units(std::string(units));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response) const
{
    int nbytes;
    int status = this->bmi->get_var_nbytes(request->name().c_str(), &nbytes);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_nbytes(nbytes);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response) const
{
    char typechar = this->find_type(request->name());
    int nbytes;
    int status = this->bmi->get_var_nbytes(request->name().c_str(), &nbytes);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    void* vals = malloc(nbytes);
    status = this->bmi->get_value(request->name().c_str(), vals);
    if(status == BMI_FAILURE)
    {
        free(vals);
        return BmiGRPCService::translate_status(status);
    }
    if (typechar == 'i')
    {
        int size = nbytes/sizeof(int);
        response->mutable_values_int()->mutable_values()->Resize(size,(int)0);
        std::copy((int*)vals, (int*)vals + size, response->mutable_values_int()->mutable_values()->begin());
    }
    if (typechar == 'f')
    {
        int size = nbytes/sizeof(float);
        response->mutable_values_float()->mutable_values()->Resize(size,(float)0);
        std::copy((float*)vals, (float*)vals + size, response->mutable_values_float()->mutable_values()->begin());
    }
    if (typechar == 'd')
    {
        int size = nbytes/sizeof(double);
        response->mutable_values_double()->mutable_values()->Resize(size,(double)0);
        std::copy((double*)vals, (double*)vals + size, response->mutable_values_double()->mutable_values()->begin());
    }
    free(vals);
    return BmiGRPCService::translate_status(status);
}
grpc::Status BmiGRPCService::getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response)
{
    return grpc::Status(grpc::StatusCode::NOTIMPLEMENTED);
}
grpc::Status BmiGRPCService::getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response) const
{
    char typechar = this->find_type(request->name());
    std::vector<int> indices(request->indices().begin(),request->indices().end());
    if (typechar == 'i')
    {
        std::vector<int> values = this->bmi->GetValueAtIndices<int>(request->name(), indices);
        response->mutable_values_int()->mutable_values()->Resize(values.size(), 0);
        std::copy(values.begin(), values.end(),response->mutable_values_int()->mutable_values()->begin());
    }
    if (typechar == 'f')
    {
        std::vector<float> values = this->bmi->GetValueAtIndices<float>(request->name(), indices);
        response->mutable_values_float()->mutable_values()->Resize(values.size(), 0);
        std::copy(values.begin(), values.end(),response->mutable_values_float()->mutable_values()->begin());
    }
    if (typechar == 'd')
    {
        std::vector<double> values = this->bmi->GetValueAtIndices<double>(request->name(), indices);
        response->mutable_values_double()->mutable_values()->Resize(values.size(), 0);
        std::copy(values.begin(), values.end(),response->mutable_values_double()->mutable_values()->begin());
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response)
{
    char typechar = this->find_type(request->name());
    if (typechar == 'i')
    {
        std::vector<int> values(request->values_int().values().size());
        std::copy(request->values_int().values().begin(),request->values_int().values().end(),values.begin());
        this->bmi->SetValue<int>(request->name(), values);
    }
    if (typechar == 'f')
    {
        std::vector<float> values(request->values_float().values().size());
        std::copy(request->values_float().values().begin(), request->values_float().values().end(),values.begin());
        this->bmi->SetValue<float>(request->name(), values);
    }
    if (typechar == 'd')
    {
        std::vector<double> values(request->values_double().values().size());
        std::copy(request->values_double().values().begin(), request->values_double().values().end(),values.begin());
        this->bmi->SetValue<double>(request->name(), values);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response)
{
    throw std::exception();
}
grpc::Status BmiGRPCService::setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response)
{
    char typechar = this->find_type(request->name());
    std::vector<int> indices(request->indices().begin(),request->indices().end());
    if (typechar == 'i')
    {
        std::vector<int> values(indices.size());
        std::copy(request->values_int().values().begin(), request->values_int().values().end(),values.begin());
        this->bmi->SetValueAtIndices<int>(request->name(), indices, values);
    }
    if (typechar == 'f')
    {
        std::vector<float> values(indices.size());
        std::copy(request->values_float().values().begin(), request->values_float().values().end(),values.begin());
        this->bmi->SetValueAtIndices<float>(request->name(), indices, values);
    }
    if (typechar == 'd')
    {
        std::vector<double> values(indices.size());
        std::copy(request->values_double().values().begin(), request->values_double().values().end(),values.begin());
        this->bmi->SetValueAtIndices<double>(request->name(), indices, values);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response) const
{
    response->set_size(this->bmi->GetGridSize(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response) const
{
    response->set_type(this->bmi->GetGridType(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response) const
{
    response->set_rank(this->bmi->GetGridRank(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response) const
{
    std::vector<int> shape = this->bmi->GetGridShape(request->grid_id());
    for(std::vector<int>::const_iterator it = shape.begin(); it != shape.end(); ++it)
    {
        response->add_shape(*it);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response) const
{
    std::vector<double> spacing = this->bmi->GetGridSpacing(request->grid_id());
    for(std::vector<double>::const_iterator it = spacing.begin(); it != spacing.end(); ++it)
    {
        response->add_spacing(*it);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response) const
{
    std::vector<double> spacing = this->bmi->GetGridSpacing(request->grid_id());
    for(std::vector<double>::const_iterator it = spacing.begin(); it != spacing.end(); ++it)
    {
        response->add_origin(*it);
    }
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) const
{
    std::vector<double> x_coords = this->bmi->GetGridX(request->grid_id());
    response->mutable_coordinates()->Resize(x_coords.size(), 0);
    std::copy(x_coords.begin(), x_coords.end(), response->mutable_coordinates()->begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) const
{
    std::vector<double> y_coords = this->bmi->GetGridY(request->grid_id());
    response->mutable_coordinates()->Resize(y_coords.size(), 0);
    std::copy(y_coords.begin(), y_coords.end(), response->mutable_coordinates()->begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) const
{
    std::vector<double> z_coords = this->bmi->GetGridZ(request->grid_id());
    response->mutable_coordinates()->Resize(z_coords.size(), 0);
    std::copy(z_coords.begin(), z_coords.end(), response->mutable_coordinates()->begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridCellCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) const
{
    response->set_count(this->bmi->GetGridCellCount(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridPointCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) const
{
    response->set_count(this->bmi->GetGridPointCount(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridVertexCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) const
{
    response->set_count(this->bmi->GetGridVertexCount(request->grid_id()));
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridConnectivity(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridConnectivityResponse* response) const
{
    std::vector<int> links = this->bmi->GetGridConnectivity(request->grid_id());
    response->mutable_links()->Resize(links.size(), 0);
    std::copy(links.begin(), links.end(), response->mutable_links()->begin());
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridOffset(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOffsetResponse* response) const
{
    std::vector<double> origin = this->bmi->GetGridOrigin(request->grid_id());
    for(std::vector<double>::const_iterator it = origin.begin(); it != origin.end(); ++it)
    {
        response->add_offsets(*it);
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

grpc::Status BmiGRPCService::translate_status(int status)
{
    if(status == BMI_SUCCESS)
    {
        return grpc::Status::OK;
    }
    if(status == BMI_FAILURE)
    {
        return grpc::Status::CANCELLED;
    }
    return grpc::Status::UNKNOWN;
}
