#include <grpc/grpc.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/security/server_credentials.h>
#include "bmi-c/bmi/bmilib.h"
#include "bmi_grpc_server.h"
#include "bmi_c_wrapper.h"


BmiGRPCService::BmiGRPCService(Bmi* bmi_):bmi(bmi_){}

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

grpc::Status BmiGRPCService::finalize(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response)
{
    return BmiGRPCService::translate_status(this->bmi->finalize());
}

grpc::Status BmiGRPCService::getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response)
{
    char name[BMI_MAX_COMPONENT_NAME];
    int status = this->bmi->get_component_name(name);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_name(std::string(name));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response)
{
    int count;
    int status = this->bmi->get_input_var_name_count(&count);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    char** input_var_names = (char**)malloc(sizeof(char*) * count);
    char* data = (char*)malloc(sizeof(char) * count * BMI_MAX_VAR_NAME);
    for(int i = 0; i < count; i++)
    {
        input_var_names[i] = data + i * BMI_MAX_VAR_NAME;
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

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response)
{
    int count;
    int status = this->bmi->get_output_var_name_count(&count);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    char** output_var_names = (char**)malloc(sizeof(char*) * count);
    char* data = (char*)malloc(sizeof(char) * count * BMI_MAX_VAR_NAME);
    for(int i = 0; i < count; i++)
    {
        output_var_names[i] = data + i * BMI_MAX_VAR_NAME;
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

grpc::Status BmiGRPCService::getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response)
{
    char units[BMI_MAX_UNITS_NAME];
    int status = this->bmi->get_time_units(units);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_units(std::string(units));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response)
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

grpc::Status BmiGRPCService::getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response)
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

grpc::Status BmiGRPCService::getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response)
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

grpc::Status BmiGRPCService::getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response)
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

grpc::Status BmiGRPCService::getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response)
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

grpc::Status BmiGRPCService::getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response)
{
    char type[BMI_MAX_TYPE_NAME];
    int status = this->bmi->get_var_type(request->name().c_str(), type);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_type(std::string(type));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response)
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

grpc::Status BmiGRPCService::getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response)
{
    char units[BMI_MAX_UNITS_NAME];
    int status = this->bmi->get_var_units(request->name().c_str(), units);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_units(std::string(units));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response)
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

grpc::Status BmiGRPCService::getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response)
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
        response->mutable_values_int()->mutable_values()->Resize(size, (int)0);
        std::copy((int*)vals, (int*)vals + size, response->mutable_values_int()->mutable_values()->begin());
    }
    if (typechar == 'f')
    {
        int size = nbytes/sizeof(float);
        response->mutable_values_float()->mutable_values()->Resize(size, (float)0);
        std::copy((float*)vals, (float*)vals + size, response->mutable_values_float()->mutable_values()->begin());
    }
    if (typechar == 'd')
    {
        int size = nbytes/sizeof(double);
        response->mutable_values_double()->mutable_values()->Resize(size, (double)0);
        std::copy((double*)vals, (double*)vals + size, response->mutable_values_double()->mutable_values()->begin());
    }
    free(vals);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response)
{
    return grpc::Status(grpc::StatusCode::UNIMPLEMENTED, "Passing pointers is forbidden across memory space boundary");
}

grpc::Status BmiGRPCService::getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response)
{
    char typechar = this->find_type(request->name());
    std::vector<int> indices(request->indices().begin(),request->indices().end());
    if (typechar == 'i')
    {
        std::vector<int> values(indices.size());
        this->bmi->get_value_at_indices(request->name().c_str(), (void*)values.data(), indices.data(), indices.size());
        response->mutable_values_int()->mutable_values()->Resize(values.size(), 0);
        std::copy(values.begin(), values.end(),response->mutable_values_int()->mutable_values()->begin());
    }
    if (typechar == 'f')
    {
        std::vector<float> values(indices.size());
        this->bmi->get_value_at_indices(request->name().c_str(), (void*)values.data(), indices.data(), indices.size());
        response->mutable_values_float()->mutable_values()->Resize(values.size(), 0);
        std::copy(values.begin(), values.end(),response->mutable_values_float()->mutable_values()->begin());
    }
    if (typechar == 'd')
    {
        std::vector<double> values(indices.size());
        this->bmi->get_value_at_indices(request->name().c_str(), (void*)values.data(), indices.data(), indices.size());
        response->mutable_values_double()->mutable_values()->Resize(values.size(), 0);
        std::copy(values.begin(), values.end(),response->mutable_values_double()->mutable_values()->begin());
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response)
{
    char typechar = this->find_type(request->name());
    int status = BMI_FAILURE;
    if (typechar == 'i')
    {
        status = this->bmi->set_value(request->name().c_str(), (const void*)request->values_int().values().data());
    }
    if (typechar == 'f')
    {
        status = this->bmi->set_value(request->name().c_str(), (const void*)request->values_float().values().data());
    }
    if (typechar == 'd')
    {
        status = this->bmi->set_value(request->name().c_str(), (const void*)request->values_double().values().data());
    }
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response)
{
    return grpc::Status(grpc::StatusCode::UNIMPLEMENTED, "Passing pointers is forbidden across memory space boundary");
}

grpc::Status BmiGRPCService::setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response)
{
    char typechar = this->find_type(request->name());
    std::vector<int> indices(request->indices().begin(),request->indices().end());
    const void* values;
    if (typechar == 'i')
    {
        values = (const void*)request->values_int().values().data();
    }
    if (typechar == 'f')
    {
        values = (const void*)request->values_float().values().data();
    }
    if (typechar == 'd')
    {
        values = (const void*)request->values_double().values().data();
    }
    return translate_status(this->bmi->set_value_at_indices(request->name().c_str(), indices.data(), indices.size(), values));
}

grpc::Status BmiGRPCService::getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response)
{
    int size;
    int status = this->bmi->get_grid_size(request->grid_id(), &size);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_size(size);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response)
{
    char type[BMI_MAX_TYPE_NAME];
    int status = this->bmi->get_grid_type(request->grid_id(), type);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_type(std::string(type));
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response)
{
    int rank;
    int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    response->set_rank(rank);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response)
{
    int rank;
    int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    int* shape = (int*)malloc(rank * sizeof(int));
    status = this->bmi->get_grid_shape(request->grid_id(), shape);
    if(status == BMI_FAILURE)
    {
        free(shape);
        return BmiGRPCService::translate_status(status);
    }
    response->clear_shape();
    for(int i = 0; i < rank; i++)
    {
        response->add_shape(shape[i]);
    }
    free(shape);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response)
{
    int rank;
    int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    double* spacing = (double*)malloc(rank * sizeof(double));
    status = this->bmi->get_grid_spacing(request->grid_id(), spacing);
    if(status == BMI_FAILURE)
    {
        free(spacing);
        return BmiGRPCService::translate_status(status);
    }
    for(int i = 0; i < rank; i++)
    {
        response->add_spacing(spacing[i]);
    }
    free(spacing);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response)
{
    int rank;
    int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    double* origin = (double*)malloc(rank * sizeof(double));
    status = this->bmi->get_grid_origin(request->grid_id(), origin);
    if(status == BMI_FAILURE)
    {
        free(origin);
        return BmiGRPCService::translate_status(status);
    }
    for(int i = 0; i < rank; i++)
    {
        response->add_origin(origin[i]);
    }
    free(origin);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response)
{
    int d[3];
    int status = this->get_grid_dimensions(request->grid_id(), d);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    int size = d[0];
    double* vals = (double*)malloc(size*sizeof(double));
    status = this->bmi->get_grid_x(request->grid_id(), vals);
    if(status == BMI_FAILURE)
    {
        free(vals);
        return BmiGRPCService::translate_status(status);
    }
    response->mutable_coordinates()->Resize(size, 0);
    std::copy(vals, vals + size, response->mutable_coordinates()->begin());
    free(vals);
    return BmiGRPCService::translate_status(status);
}
grpc::Status BmiGRPCService::getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response)
{
    int d[3];
    int status = this->get_grid_dimensions(request->grid_id(), d);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    int size = d[1];
    double* vals = (double*)malloc(size*sizeof(double));
    status = this->bmi->get_grid_y(request->grid_id(), vals);
    if(status == BMI_FAILURE)
    {
        free(vals);
        return BmiGRPCService::translate_status(status);
    }
    response->mutable_coordinates()->Resize(size, 0);
    std::copy(vals, vals + size, response->mutable_coordinates()->begin());
    free(vals);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response)
{
    int d[3];
    int status = this->get_grid_dimensions(request->grid_id(), d);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    int size = d[2];
    double* vals = (double*)malloc(size*sizeof(double));
    status = this->bmi->get_grid_z(request->grid_id(), vals);
    if(status == BMI_FAILURE)
    {
        free(vals);
        return BmiGRPCService::translate_status(status);
    }
    response->mutable_coordinates()->Resize(size, 0);
    std::copy(vals, vals + size, response->mutable_coordinates()->begin());
    free(vals);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridConnectivity(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridConnectivityResponse* response)
{
    int size;
    int status = this->bmi->get_grid_cell_count(request->grid_id(), &size);
    size *= 3; // TODO: Figure out how to retrieve cell types to get the total storage size, this is only for triangles...
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    int* links = (int*)malloc(size * sizeof(int));
    status = this->bmi->get_grid_connectivity(request->grid_id(), links);
    if(status == BMI_FAILURE)
    {
        free(links);
        return BmiGRPCService::translate_status(status);
    }
    response->mutable_links()->Resize(size, 0);
    std::copy(links, links + size, response->mutable_links()->begin());
    free(links);
    return BmiGRPCService::translate_status(status);
}

grpc::Status BmiGRPCService::getGridOffset(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOffsetResponse* response)
{
    int size;
    int status = this->bmi->get_grid_size(request->grid_id(), &size);
    if(status == BMI_FAILURE)
    {
        return BmiGRPCService::translate_status(status);
    }
    int* offsets = (int*)malloc(size * sizeof(int));
    status = this->bmi->get_grid_offset(request->grid_id(), offsets);
    if(status == BMI_FAILURE)
    {
        free(offsets);
        return BmiGRPCService::translate_status(status);
    }
    response->mutable_offsets()->Resize(size, 0);
    std::copy(offsets, offsets + size, response->mutable_offsets()->begin());
    free(offsets);
    return BmiGRPCService::translate_status(status);
}

char BmiGRPCService::find_type(const std::string& varname) const
{
    std::locale loc;
    char type[BMI_MAX_TYPE_NAME];
    this->bmi->get_var_type(varname.c_str(), type);
    std::string vartype(type);
    std::transform(vartype.begin(), vartype.end(), vartype.begin(), ::tolower);
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

int BmiGRPCService::get_grid_dimensions(int grid_id, int* vec3d) const
{
    int rank;
    int status = this->bmi->get_grid_rank(grid_id, &rank);
    if(status == BMI_FAILURE)
    {
        return status;
    }
    int* shape = (int*)malloc(rank * sizeof(int));
    status = this->bmi->get_grid_shape(grid_id, shape);
    if(status == BMI_FAILURE)
    {
        free(shape);
        return status;
    }
    char type[BMI_MAX_TYPE_NAME];
    status = this->bmi->get_grid_type(grid_id, type);
    if(status == BMI_FAILURE)
    {
        free(shape);
        return status;
    }
    std::string typestr(type);
    if(typestr == "uniform_rectilinear" or typestr == "rectilinear")
    {
        vec3d[0] = shape[0];
        vec3d[1] = shape[1];
        if(rank > 2)
        {
            vec3d[2] = shape[2];
        }
        else
        {
            vec3d[3] = 1;
        }
    }
    else
    {
        int size;
        status = this->bmi->get_grid_size(grid_id, &size);
        vec3d[0] = size;
        vec3d[1] = size;
        vec3d[2] = size;
    }
    return status;
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
    return grpc::Status(grpc::StatusCode::UNKNOWN, "Unknown BMI status code encountered");
}

void run_bmi_server(BMI_Model* model, int argc, char* argv[])
{
    Bmi* wrapper = new BmiCWrapper(model);
    run_bmi_server(wrapper, argc, argv);
    delete wrapper;
}

void run_bmi_server(Bmi* model, int argc, char* argv[])
{
    std::string server_address("0.0.0.0:50051");
    if(argc > 1)
    {
        server_address = "0.0.0.0:" + std::string(argv[1]);
    }
    std::cerr<<"BMI grpc server attached to server address "<<server_address<<std::endl;
    BmiGRPCService service(model); 
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    server->Wait();
}
