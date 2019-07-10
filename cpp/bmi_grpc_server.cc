#include <grpc/grpc.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/security/server_credentials.h>
#include "bmi-c/bmi/bmilib.h"
#include "bmi_grpc_server.h"
#include "bmi_c_wrapper.h"

BmiGRPCService::BmiGRPCService(Bmi *bmi_) : bmi(bmi_) {}

BmiGRPCService::~BmiGRPCService() {}

grpc::Status BmiGRPCService::initialize(grpc::ServerContext *context, const bmi::InitializeRequest *request, bmi::Empty *response)
{
    try
    {
        int status = this->bmi->initialize(request->config_file().c_str());
        BmiGRPCService::process_status("initialize", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::update(grpc::ServerContext *context, const bmi::Empty *request, bmi::Empty *response)
{
    try
    {
        int status = this->bmi->update();
        BmiGRPCService::process_status("update", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::updateUntil(grpc::ServerContext *context, const bmi::UpdateUntilRequest *request, bmi::Empty *response)
{
    try
    {
        int status = this->bmi->update_until(request->until());
        BmiGRPCService::process_status("update_until", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::updateFrac(grpc::ServerContext *context, const bmi::UpdateFracRequest *request, bmi::Empty *response)
{
    try
    {
        int status = this->bmi->update_frac(request->frac());
        BmiGRPCService::process_status("update_frac", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::runModel(grpc::ServerContext *context, const bmi::Empty *request, bmi::Empty *response)
{
    try
    {
        int status = this->bmi->run_model();
        BmiGRPCService::process_status("run_model", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::finalize(grpc::ServerContext *context, const bmi::Empty *request, bmi::Empty *response)
{
    try
    {
        int status = this->bmi->finalize();
        BmiGRPCService::process_status("finalize", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getComponentName(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetComponentNameResponse *response)
{
    try
    {
        char name[BMI_MAX_COMPONENT_NAME];
        int status = this->bmi->get_component_name(name);
        BmiGRPCService::process_status("get_component_name", status);
        response->set_name(std::string(name));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNames(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetVarNamesResponse *response)
{
    char **input_var_names;
    char *data;
    try
    {
        int count;
        int status = this->bmi->get_input_var_name_count(&count);
        BmiGRPCService::process_status("get_input_var_name_count", status);
        input_var_names = (char **)malloc(sizeof(char *) * count);
        data = (char *)malloc(sizeof(char) * count * BMI_MAX_VAR_NAME);
        for (int i = 0; i < count; i++)
        {
            input_var_names[i] = data + i * BMI_MAX_VAR_NAME;
        }
        status = this->bmi->get_input_var_names(input_var_names);
        BmiGRPCService::process_status("get_input_var_names", status);
        for (int i = 0; i < count; i++)
        {
            response->add_names(std::string(input_var_names[i]));
        }
    }
    catch (const std::exception &e)
    {
        free(data);
        free(input_var_names);
        return BmiGRPCService::handle_exception(e);
    }
    free(data);
    free(input_var_names);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetVarNamesResponse *response)
{
    char **output_var_names;
    char *data;
    try
    {
        int count;
        int status = this->bmi->get_output_var_name_count(&count);
        BmiGRPCService::process_status("get_output_var_name_count", status);
        output_var_names = (char **)malloc(sizeof(char *) * count);
        data = (char *)malloc(sizeof(char) * count * BMI_MAX_VAR_NAME);
        for (int i = 0; i < count; i++)
        {
            output_var_names[i] = data + i * BMI_MAX_VAR_NAME;
        }
        status = this->bmi->get_output_var_names(output_var_names);
        BmiGRPCService::process_status("get_output_var_names", status);
        for (int i = 0; i < count; i++)
        {
            response->add_names(std::string(output_var_names[i]));
        }
    }
    catch (const std::exception &e)
    {
        free(data);
        free(output_var_names);
        return BmiGRPCService::handle_exception(e);
    }
    free(data);
    free(output_var_names);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getTimeUnits(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetTimeUnitsResponse *response)
{
    try
    {
        char units[BMI_MAX_UNITS_NAME];
        int status = this->bmi->get_time_units(units);
        BmiGRPCService::process_status("get_time_units", status);
        response->set_units(std::string(units));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getTimeStep(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetTimeStepResponse *response)
{
    try
    {
        double step;
        int status = this->bmi->get_time_step(&step);
        BmiGRPCService::process_status("get_time_step", status);
        response->set_interval(step);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getCurrentTime(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetTimeResponse *response)
{
    try
    {
        double time;
        int status = this->bmi->get_current_time(&time);
        BmiGRPCService::process_status("get_current_time", status);
        response->set_time(time);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getStartTime(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetTimeResponse *response)
{
    try
    {
        double time;
        int status = this->bmi->get_start_time(&time);
        BmiGRPCService::process_status("get_start_time", status);
        response->set_time(time);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getEndTime(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetTimeResponse *response)
{
    try
    {
        double time;
        int status = this->bmi->get_end_time(&time);
        BmiGRPCService::process_status("get_end_time", status);
        response->set_time(time);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarGrid(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarGridResponse *response)
{
    int grid_id;
    try
    {
        int status = this->bmi->get_var_grid(request->name().c_str(), &grid_id);
        BmiGRPCService::process_status("get_var_grid", status);
        response->set_grid_id(grid_id);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarType(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarTypeResponse *response)
{
    char type[BMI_MAX_TYPE_NAME];
    try
    {
        int status = this->bmi->get_var_type(request->name().c_str(), type);
        BmiGRPCService::process_status("get_var_type", status);
        response->set_type(std::string(type));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarItemSize(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarItemSizeResponse *response)
{
    try
    {
        int size;
        int status = this->bmi->get_var_itemsize(request->name().c_str(), &size);
        BmiGRPCService::process_status("get_var_itemsize", status);
        response->set_size(size);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarUnits(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarUnitsResponse *response)
{
    try
    {
        char units[BMI_MAX_UNITS_NAME];
        int status = this->bmi->get_var_units(request->name().c_str(), units);
        BmiGRPCService::process_status("get_var_units", status);
        response->set_units(std::string(units));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarNBytes(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarNBytesResponse *response)
{
    try
    {
        int nbytes;
        int status = this->bmi->get_var_nbytes(request->name().c_str(), &nbytes);
        BmiGRPCService::process_status("get_var_nbytes", status);
        response->set_nbytes(nbytes);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getValue(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetValueResponse *response)
{
    void *vals;
    try
    {
        char typechar = this->find_type(request->name());
        int nbytes;
        int status = this->bmi->get_var_nbytes(request->name().c_str(), &nbytes);
        BmiGRPCService::process_status("get_var_nbytes", status);
        vals = malloc(nbytes);
        status = this->bmi->get_value(request->name().c_str(), vals);
        BmiGRPCService::process_status("get_value", status);
        if (typechar == 'i')
        {
            int size = nbytes / sizeof(int);
            response->mutable_values_int()->mutable_values()->Resize(size, (int)0);
            std::copy((int *)vals, (int *)vals + size, response->mutable_values_int()->mutable_values()->begin());
        }
        if (typechar == 'f')
        {
            int size = nbytes / sizeof(float);
            response->mutable_values_float()->mutable_values()->Resize(size, (float)0);
            std::copy((float *)vals, (float *)vals + size, response->mutable_values_float()->mutable_values()->begin());
        }
        if (typechar == 'd')
        {
            int size = nbytes / sizeof(double);
            response->mutable_values_double()->mutable_values()->Resize(size, (double)0);
            std::copy((double *)vals, (double *)vals + size, response->mutable_values_double()->mutable_values()->begin());
        }
    }
    catch (const std::exception &e)
    {
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(vals);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getValuePtr(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::Empty *response)
{
    return grpc::Status(grpc::StatusCode::UNIMPLEMENTED, "Passing pointers is forbidden across memory space boundary");
}

grpc::Status BmiGRPCService::getValueAtIndices(grpc::ServerContext *context, const bmi::GetValueAtIndicesRequest *request, bmi::GetValueAtIndicesResponse *response)
{
    int status = BMI_FAILURE;
    std::vector<int> indices(request->indices().begin(), request->indices().end());
    try
    {
        char typechar = this->find_type(request->name());
        if (typechar == 'i')
        {
            std::vector<int> values(indices.size());
            status = this->bmi->get_value_at_indices(request->name().c_str(), (void *)values.data(), indices.data(), indices.size());
            BmiGRPCService::process_status("get_value_at_indices", status);
            response->mutable_values_int()->mutable_values()->Resize(values.size(), 0);
            std::copy(values.begin(), values.end(), response->mutable_values_int()->mutable_values()->begin());
        }
        if (typechar == 'f')
        {
            std::vector<float> values(indices.size());
            status = this->bmi->get_value_at_indices(request->name().c_str(), (void *)values.data(), indices.data(), indices.size());
            BmiGRPCService::process_status("get_value_at_indices", status);
            response->mutable_values_float()->mutable_values()->Resize(values.size(), 0);
            std::copy(values.begin(), values.end(), response->mutable_values_float()->mutable_values()->begin());
        }
        if (typechar == 'd')
        {
            std::vector<double> values(indices.size());
            status = this->bmi->get_value_at_indices(request->name().c_str(), (void *)values.data(), indices.data(), indices.size());
            BmiGRPCService::process_status("get_value_at_indices", status);
            response->mutable_values_double()->mutable_values()->Resize(values.size(), 0);
            std::copy(values.begin(), values.end(), response->mutable_values_double()->mutable_values()->begin());
        }
        BmiGRPCService::process_status("get_value_at_indices", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::setValue(grpc::ServerContext *context, const bmi::SetValueRequest *request, bmi::Empty *response)
{
    int status = BMI_FAILURE;
    try
    {
        char typechar = this->find_type(request->name());
        if (typechar == 'i')
        {
            status = this->bmi->set_value(request->name().c_str(), (const void *)request->values_int().values().data());
        }
        if (typechar == 'f')
        {
            status = this->bmi->set_value(request->name().c_str(), (const void *)request->values_float().values().data());
        }
        if (typechar == 'd')
        {
            status = this->bmi->set_value(request->name().c_str(), (const void *)request->values_double().values().data());
        }
        BmiGRPCService::process_status("set_value", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::setValuePtr(grpc::ServerContext *context, const bmi::SetValuePtrRequest *request, bmi::Empty *response)
{
    return grpc::Status(grpc::StatusCode::UNIMPLEMENTED, "Passing pointers is forbidden across memory space boundary");
}

grpc::Status BmiGRPCService::setValueAtIndices(grpc::ServerContext *context, const bmi::SetValueAtIndicesRequest *request, bmi::Empty *response)
{
    try
    {
        char typechar = this->find_type(request->name());
        std::vector<int> indices(request->indices().begin(), request->indices().end());
        const void *values;
        if (typechar == 'i')
        {
            values = (const void *)request->values_int().values().data();
        }
        if (typechar == 'f')
        {
            values = (const void *)request->values_float().values().data();
        }
        if (typechar == 'd')
        {
            values = (const void *)request->values_double().values().data();
        }
        int status = this->bmi->set_value_at_indices(request->name().c_str(), indices.data(), indices.size(), values);
        BmiGRPCService::process_status("set_value_at_indices", status);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridSize(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridSizeResponse *response)
{
    try
    {
        int size;
        int status = this->bmi->get_grid_size(request->grid_id(), &size);
        BmiGRPCService::process_status("get_grid_size", status);
        response->set_size(size);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridType(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridTypeResponse *response)
{
    try
    {
        char type[BMI_MAX_TYPE_NAME];
        int status = this->bmi->get_grid_type(request->grid_id(), type);
        BmiGRPCService::process_status("get_grid_type", status);
        response->set_type(std::string(type));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridRank(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridRankResponse *response)
{
    try
    {
        int rank;
        int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
        BmiGRPCService::process_status("get_grid_rank", status);
        response->set_rank(rank);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridShape(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridShapeResponse *response)
{
    int *shape;
    try
    {
        int rank;
        int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
        BmiGRPCService::process_status("get_grid_rank", status);
        shape = (int *)malloc(rank * sizeof(int));
        status = this->bmi->get_grid_shape(request->grid_id(), shape);
        BmiGRPCService::process_status("get_grid_shape", status);
        response->clear_shape();
        for (int i = 0; i < rank; i++)
        {
            response->add_shape(shape[i]);
        }
    }
    catch (const std::exception &e)
    {
        free(shape);
        return BmiGRPCService::handle_exception(e);
    }
    free(shape);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridSpacing(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridSpacingResponse *response)
{
    double *spacing;
    try
    {
        int rank;
        int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
        BmiGRPCService::process_status("get_grid_rank", status);
        spacing = (double *)malloc(rank * sizeof(double));
        status = this->bmi->get_grid_spacing(request->grid_id(), spacing);
        BmiGRPCService::process_status("get_grid_spacing", status);
        for (int i = 0; i < rank; i++)
        {
            response->add_spacing(spacing[i]);
        }
    }
    catch (const std::exception &e)
    {
        free(spacing);
        return BmiGRPCService::handle_exception(e);
    }
    free(spacing);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridOrigin(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridOriginResponse *response)
{
    double *origin;
    try
    {
        int rank;
        int status = this->bmi->get_grid_rank(request->grid_id(), &rank);
        BmiGRPCService::process_status("get_grid_rank", status);
        origin = (double *)malloc(rank * sizeof(double));
        status = this->bmi->get_grid_origin(request->grid_id(), origin);
        BmiGRPCService::process_status("get_grid_origin", status);
        for (int i = 0; i < rank; i++)
        {
            response->add_origin(origin[i]);
        }
    }
    catch (const std::exception &e)
    {
        free(origin);
        return BmiGRPCService::handle_exception(e);
    }
    free(origin);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridX(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridPointsResponse *response)
{
    double *vals;
    try
    {
        int d[3];
        this->get_grid_dimensions(request->grid_id(), d);
        int size = d[0];
        vals = (double *)malloc(size * sizeof(double));
        int status = this->bmi->get_grid_x(request->grid_id(), vals);
        BmiGRPCService::process_status("get_grid_x", status);
        response->mutable_coordinates()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_coordinates()->begin());
    }
    catch (const std::exception &e)
    {
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(vals);
    return grpc::Status::OK;
}
grpc::Status BmiGRPCService::getGridY(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridPointsResponse *response)
{
    double *vals;
    try
    {
        int d[3];
        this->get_grid_dimensions(request->grid_id(), d);
        int size = d[1];
        double *vals = (double *)malloc(size * sizeof(double));
        int status = this->bmi->get_grid_y(request->grid_id(), vals);
        BmiGRPCService::process_status("get_grid_y", status);
        response->mutable_coordinates()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_coordinates()->begin());
    }
    catch (const std::exception &e)
    {
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(vals);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridZ(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridPointsResponse *response)
{
    double *vals;
    try
    {
        int d[3];
        this->get_grid_dimensions(request->grid_id(), d);
        int size = d[2];
        double *vals = (double *)malloc(size * sizeof(double));
        int status = this->bmi->get_grid_z(request->grid_id(), vals);
        BmiGRPCService::process_status("get_grid_z", status);
        response->mutable_coordinates()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_coordinates()->begin());
    }
    catch (const std::exception &e)
    {
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(vals);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridConnectivity(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridConnectivityResponse *response)
{
    int *links;
    try
    {
        int size;
        int status = this->bmi->get_grid_cell_count(request->grid_id(), &size);
        size *= 3; // TODO: Figure out how to retrieve cell types to get the total storage size, this is only for triangles...
        BmiGRPCService::process_status("get_grid_cell_count", status);
        links = (int *)malloc(size * sizeof(int));
        status = this->bmi->get_grid_connectivity(request->grid_id(), links);
        BmiGRPCService::process_status("get_grid_connectivity", status);
        response->mutable_links()->Resize(size, 0);
        std::copy(links, links + size, response->mutable_links()->begin());
    }
    catch (const std::exception &e)
    {
        free(links);
        return BmiGRPCService::handle_exception(e);
    }
    free(links);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridOffset(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridOffsetResponse *response)
{
    int *offsets;
    try
    {
        int size;
        int status = this->bmi->get_grid_size(request->grid_id(), &size);
        BmiGRPCService::process_status("get_grid_connectivity", status);
        offsets = (int *)malloc(size * sizeof(int));
        status = this->bmi->get_grid_offset(request->grid_id(), offsets);
        BmiGRPCService::process_status("get_grid_connectivity", status);
        response->mutable_offsets()->Resize(size, 0);
        std::copy(offsets, offsets + size, response->mutable_offsets()->begin());
    }
    catch (const std::exception &e)
    {
        free(offsets);
        return BmiGRPCService::handle_exception(e);
    }
    free(offsets);
    return grpc::Status::OK;
}

char BmiGRPCService::find_type(const std::string &varname) const
{
    std::locale loc;
    char type[BMI_MAX_TYPE_NAME];
    int status = this->bmi->get_var_type(varname.c_str(), type);
    BmiGRPCService::process_status("get_var_type", status);
    std::string vartype(type);
    std::transform(vartype.begin(), vartype.end(), vartype.begin(), ::tolower);
    std::vector<std::string> inttypes = {"int", "int16", "int32", "int64"};
    if (std::find(inttypes.begin(), inttypes.end(), vartype) != inttypes.end())
    {
        return 'i';
    }
    std::vector<std::string> flttypes = {"float", "float32"};
    if (std::find(flttypes.begin(), flttypes.end(), vartype) != flttypes.end())
    {
        return 'f';
    }
    std::vector<std::string> dbltypes = {"double", "float64"};
    if (std::find(dbltypes.begin(), dbltypes.end(), vartype) != dbltypes.end())
    {
        return 'd';
    }
    throw std::invalid_argument("Could not match the variable type " + vartype + " of variable " + varname + "to integer, float or double");
}

void BmiGRPCService::get_grid_dimensions(int grid_id, int *vec3d) const
{
    int *shape;
    try
    {
        int rank;
        int status = this->bmi->get_grid_rank(grid_id, &rank);
        BmiGRPCService::process_status("get_grid_rank", status);
        int *shape = (int *)malloc(rank * sizeof(int));
        status = this->bmi->get_grid_shape(grid_id, shape);
        BmiGRPCService::process_status("get_grid_shape", status);
        char type[BMI_MAX_TYPE_NAME];
        status = this->bmi->get_grid_type(grid_id, type);
        BmiGRPCService::process_status("get_grid_type", status);
        std::string typestr(type);
        if (typestr == "uniform_rectilinear" or typestr == "rectilinear")
        {
            vec3d[0] = shape[0];
            vec3d[1] = shape[1];
            if (rank > 2)
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
            BmiGRPCService::process_status("get_grid_size", status);
            vec3d[0] = size;
            vec3d[1] = size;
            vec3d[2] = size;
        }
    }
    catch (const std::exception &e)
    {
        free(shape);
        throw;
    }
    free(shape);
}

void BmiGRPCService::process_status(const std::string func, int status)
{
    if (status == BMI_FAILURE)
    {
        throw std::logic_error("BMI model function " + func + " failed");
    }
}

grpc::Status BmiGRPCService::handle_exception(const std::exception &exception)
{
    std::cerr << "Error: " << exception.what() << std::endl;
    return grpc::Status(grpc::StatusCode::INTERNAL, exception.what());
}

void run_bmi_server(BMI_Model *model, int argc, char *argv[])
{
    Bmi *wrapper = new BmiCWrapper(model);
    run_bmi_server(wrapper, argc, argv);
    delete wrapper;
}

void run_bmi_server(Bmi *model, int argc, char *argv[])
{
    std::string server_address("0.0.0.0:50051");
    if (argc > 1)
    {
        server_address = "0.0.0.0:" + std::string(argv[1]);
    }
    std::cerr << "BMI grpc server attached to server address " << server_address << std::endl;
    BmiGRPCService service(model);
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    server->Wait();
}
