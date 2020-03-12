#include <grpc/grpc.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/security/server_credentials.h>
#include "bmi_grpc_server.h"
#include "bmi_c_wrapper.h"

BmiGRPCService::BmiGRPCService(BmiClass* bmi_) : bmi(bmi_) {}

BmiGRPCService::~BmiGRPCService() {}

grpc::Status BmiGRPCService::initialize(grpc::ServerContext *context, const bmi::InitializeRequest *request, bmi::Empty *response)
{
    try
    {
        this->bmi->Initialize(request->config_file().c_str());
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
        this->bmi->Update();
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::updateUntil(grpc::ServerContext *context, const bmi::GetTimeResponse *request, bmi::Empty *response)
{
    try
    {
        this->bmi->UpdateUntil(request->time());
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
        this->bmi->Finalize();
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
        std::string name = this->bmi->GetComponentName();
        response->set_name(name);
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputItemCount(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetCountResponse *response)
{
    try
    {
        response->set_count(this->bmi->GetInputItemCount());
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputItemCount(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetCountResponse *response)
{
    try
    {
        response->set_count(this->bmi->GetOutputItemCount());
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getInputVarNames(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetVarNamesResponse *response)
{
    try
    {
        std::vector<std::string> input_var_names = this->bmi->GetInputVarNames();
        for (int i = 0; i < input_var_names.size(); i++)
        {
            response->add_names(input_var_names[i]);
        }
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getOutputVarNames(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetVarNamesResponse *response)
{
    try
    {
        std::vector<std::string> output_var_names = this->bmi->GetOutputVarNames();
        for (int i = 0; i < output_var_names.size(); i++)
        {
            response->add_names(std::string(output_var_names[i]));
        }
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getTimeUnits(grpc::ServerContext *context, const bmi::Empty *request, bmi::GetTimeUnitsResponse *response)
{
    try
    {
        std::string units = this->bmi->GetTimeUnits();
        response->set_units(units);
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
        response->set_interval(this->bmi->GetTimeStep());
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
        response->set_time(this->bmi->GetCurrentTime());
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
        response->set_time(this->bmi->GetStartTime());
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
        response->set_time(this->bmi->GetEndTime());
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarGrid(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarGridResponse *response)
{
    try
    {
        response->set_grid_id(this->bmi->GetVarGrid(request->name().c_str()));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarType(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarTypeResponse *response)
{
    try
    {
        std::string type = this->bmi->GetVarType(request->name());
        response->set_type(type);
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
        response->set_size(this->bmi->GetVarItemsize(request->name().c_str()));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getVarLocation(grpc::ServerContext *context, const bmi::GetVarRequest *request, bmi::GetVarLocationResponse *response)
{
    try
    {
        std::string loc = this->bmi->GetVarLocation(request->name());
        bmi::GetVarLocationResponse::Location loce;
        bmi::GetVarLocationResponse::Location_Parse(loc, &loce);
        response->set_location(loce);
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
        std::string units = this->bmi->GetVarUnits(request->name());
        response->set_units(units);
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
        response->set_nbytes(this->bmi->GetVarNbytes(request->name().c_str()));
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
        int nbytes = this->bmi->GetVarNbytes(request->name().c_str());
        vals = malloc(nbytes);
        this->bmi->GetValue(request->name().c_str(), vals);
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
    std::vector<int> indices(request->indices().begin(), request->indices().end());
    try
    {
        char typechar = this->find_type(request->name());
        if (typechar == 'i')
        {
            std::vector<int> values(indices.size());
            this->bmi->GetValueAtIndices(request->name().c_str(), (void *)values.data(), indices.data(), indices.size());
            response->mutable_values_int()->mutable_values()->Resize(values.size(), 0);
            std::copy(values.begin(), values.end(), response->mutable_values_int()->mutable_values()->begin());
        }
        if (typechar == 'f')
        {
            std::vector<float> values(indices.size());
            this->bmi->GetValueAtIndices(request->name().c_str(), (void *)values.data(), indices.data(), indices.size());
            response->mutable_values_float()->mutable_values()->Resize(values.size(), 0);
            std::copy(values.begin(), values.end(), response->mutable_values_float()->mutable_values()->begin());
        }
        if (typechar == 'd')
        {
            std::vector<double> values(indices.size());
            this->bmi->GetValueAtIndices(request->name().c_str(), (void *)values.data(), indices.data(), indices.size());
            response->mutable_values_double()->mutable_values()->Resize(values.size(), 0);
            std::copy(values.begin(), values.end(), response->mutable_values_double()->mutable_values()->begin());
        }
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::setValue(grpc::ServerContext *context, const bmi::SetValueRequest *request, bmi::Empty *response)
{
    try
    {
        char typechar = this->find_type(request->name());
        if (typechar == 'i')
        {
            this->bmi->SetValue(request->name().c_str(), (void*)request->values_int().values().data());
        }
        if (typechar == 'f')
        {
            this->bmi->SetValue(request->name().c_str(), (void*)request->values_float().values().data());
        }
        if (typechar == 'd')
        {
            this->bmi->SetValue(request->name().c_str(), (void*)request->values_double().values().data());
        }
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
        void *values;
        if (typechar == 'i')
        {
            values = (void*)request->values_int().values().data();
        }
        if (typechar == 'f')
        {
            values = (void*)request->values_float().values().data();
        }
        if (typechar == 'd')
        {
            values = (void*)request->values_double().values().data();
        }
        this->bmi->SetValueAtIndices(request->name().c_str(), indices.data(), indices.size(), values);
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
        response->set_size(this->bmi->GetGridSize(request->grid_id()));
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
        std::string type = this->bmi->GetGridType(request->grid_id());
        response->set_type(type);
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
        response->set_rank(this->bmi->GetGridRank(request->grid_id()));
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
        int rank = this->bmi->GetGridRank(request->grid_id());
        shape = (int *)malloc(rank * sizeof(int));
        this->bmi->GetGridShape(request->grid_id(), shape);
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
        int rank = this->bmi->GetGridRank(request->grid_id());
        spacing = (double *)malloc(rank * sizeof(double));
        this->bmi->GetGridSpacing(request->grid_id(), spacing);
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
        int rank = this->bmi->GetGridRank(request->grid_id());
        origin = (double *)malloc(rank * sizeof(double));
        this->bmi->GetGridOrigin(request->grid_id(), origin);
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
        this->bmi->GetGridX(request->grid_id(), vals);
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
        this->bmi->GetGridY(request->grid_id(), vals);
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
        this->bmi->GetGridZ(request->grid_id(), vals);
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

grpc::Status BmiGRPCService::getGridNodeCount(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetCountResponse *response)
{
    try
    {
        response->set_count(this->bmi->GetGridNodeCount(request->grid_id()));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridEdgeCount(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetCountResponse *response)
{
    try
    {
        response->set_count(this->bmi->GetGridEdgeCount(request->grid_id()));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridFaceCount(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetCountResponse *response)
{
    try
    {
        response->set_count(this->bmi->GetGridFaceCount(request->grid_id()));
    }
    catch (const std::exception &e)
    {
        return BmiGRPCService::handle_exception(e);
    }
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridEdgeNodes(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridEdgeNodesResponse *response)
{
    int *vals;
    try
    {
        int size = 2*(this->bmi->GetGridEdgeCount(request->grid_id()));
        vals = (int *)malloc(size * sizeof(int));
        this->bmi->GetGridEdgeNodes(request->grid_id(), vals);
        response->mutable_edge_nodes()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_edge_nodes()->begin());
    }
    catch (const std::exception &e)
    {
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(vals);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridFaceNodes(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridFaceNodesResponse *response)
{
    int *vals;
    int *facenodes;
    try
    {
        int face_count = this->bmi->GetGridFaceCount(request->grid_id());
        facenodes = (int *)malloc(face_count * sizeof(int));
        this->bmi->GetGridNodesPerFace(request->grid_id(), facenodes);
        int size = 0;
        for(int i = 0; i < face_count; ++i)
        {
            size += facenodes[i];
        }
        vals = (int *)malloc(size * sizeof(int));
        this->bmi->GetGridFaceNodes(request->grid_id(), vals);
        response->mutable_face_nodes()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_face_nodes()->begin());
    }
    catch (const std::exception &e)
    {
        free(facenodes);
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(facenodes);
    free(vals);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridFaceEdges(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridFaceEdgesResponse *response)
{
    int *vals;
    int *faceedges;
    try
    {
        int face_count = this->bmi->GetGridFaceCount(request->grid_id());
        faceedges = (int *)malloc(face_count * sizeof(int));
        this->bmi->GetGridNodesPerFace(request->grid_id(), faceedges);
        int size = 0;
        for(int i = 0; i < face_count; ++i)
        {
            size += faceedges[i];
        }
        vals = (int *)malloc(size * sizeof(int));
        this->bmi->GetGridFaceEdges(request->grid_id(), vals);
        response->mutable_face_edges()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_face_edges()->begin());
    }
    catch (const std::exception &e)
    {
        free(faceedges);
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(faceedges);
    free(vals);
    return grpc::Status::OK;
}

grpc::Status BmiGRPCService::getGridNodesPerFace(grpc::ServerContext *context, const bmi::GridRequest *request, bmi::GetGridNodesPerFaceResponse *response)
{
    int *vals;
    try
    {
        int size = this->bmi->GetGridFaceCount(request->grid_id());
        vals = (int *)malloc(size * sizeof(int));
        this->bmi->GetGridNodesPerFace(request->grid_id(), vals);
        response->mutable_nodes_per_face()->Resize(size, 0);
        std::copy(vals, vals + size, response->mutable_nodes_per_face()->begin());
    }
    catch (const std::exception &e)
    {
        free(vals);
        return BmiGRPCService::handle_exception(e);
    }
    free(vals);
    return grpc::Status::OK;
}

char BmiGRPCService::find_type(const std::string &varname) const
{
    std::locale loc;
    std::string type = this->bmi->GetVarType(varname);
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
        int rank = this->bmi->GetGridRank(grid_id);
        int *shape = (int *)malloc(rank * sizeof(int));
        this->bmi->GetGridShape(grid_id, shape);
        std::string type = this->bmi->GetGridType(grid_id);
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
            int size = this->bmi->GetGridSize(grid_id);
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

grpc::Status BmiGRPCService::handle_exception(const std::exception &exception)
{
    std::cerr << "Error: " << exception.what() << std::endl;
    return grpc::Status(grpc::StatusCode::INTERNAL, exception.what());
}

void run_bmi_server(BMIModel *model, int argc, char *argv[])
{
    BmiClass *wrapper = new BmiCWrapper(model);
    run_bmi_server(wrapper, argc, argv);
    delete wrapper;
}

void run_bmi_server(BmiClass *model, int argc, char *argv[])
{
    std::string server_address("0.0.0.0:55555");
    if (argc > 1)
    {
        server_address = "0.0.0.0:" + std::string(argv[1]);
    }
    std::string bmi_port = std::getenv("BMI_PORT");
    if(!bmi_port.empty()) {
        server_address = "0.0.0.0:" + bmi_port;
    }
    std::cerr << "BMI grpc server attached to server address " << server_address << std::endl;
    BmiGRPCService service(model);
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    server->Wait();
}
