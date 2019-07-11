#include "bmi_c_wrapper.h"
#include <stdexcept>

BmiCWrapper::BmiCWrapper(BMIModel* m):model(m){}

BmiCWrapper::~BmiCWrapper(){}

void checkStatus(int status)
{
    if(status == BMI_FAILURE)
    {
        throw std::runtime_error("BMI failure from C intercepted");
    }
}

void BmiCWrapper::Initialize(const char* configfile)
{
    checkStatus(this->model->initialize(this->model->self, const_cast<char*>(configfile)));
}

void BmiCWrapper::Update()
{
    double curtime, timestep;
    checkStatus(this->model->get_current_time(this->model->self, &curtime));
    checkStatus(this->model->get_time_step(this->model->self, &timestep));
    checkStatus(this->model->update(this->model->self, curtime + timestep));
}

void BmiCWrapper::UpdateUntil(double time)
{
    checkStatus(this->model->update(this->model->self, time));
}

void BmiCWrapper::Finalize()
{
    checkStatus(this->model->finalize(this->model->self));
}

void BmiCWrapper::GetComponentName(char* const dest)
{
    checkStatus(this->model->get_component_name(this->model->self, dest));
}

int BmiCWrapper::GetInputVarNameCount()
{
    int dest;
    checkStatus(this->model->get_input_item_count(this->model->self, &dest));
    return dest;
}

int BmiCWrapper::GetOutputVarNameCount()
{
    int dest;
    checkStatus(this->model->get_output_item_count(this->model->self, &dest));
    return dest;
}

void BmiCWrapper::GetInputVarNames(char** dest)
{
    checkStatus(this->model->get_input_var_names(this->model->self, dest));
}

void BmiCWrapper::GetOutputVarNames(char** dest)
{
    checkStatus(this->model->get_output_var_names(this->model->self, dest));
}

int BmiCWrapper::GetVarGrid(const char* name)
{
    int dest;
    checkStatus(this->model->get_var_grid(this->model->self, const_cast<char*>(name), &dest));
    return dest;
}

void BmiCWrapper::GetVarType(const char* name, char* vtype)
{
    checkStatus(this->model->get_var_type(this->model->self, const_cast<char*>(name), vtype));
}

int BmiCWrapper::GetVarItemsize(const char* name)
{
    int dest;
    checkStatus(this->model->get_var_itemsize(this->model->self, const_cast<char*>(name), &dest));
    return dest;
}

void BmiCWrapper::GetVarUnits(const char* name, char* const dest)
{
    checkStatus(this->model->get_var_units(this->model->self, const_cast<char*>(name), dest));
}

int BmiCWrapper::GetVarNbytes(const char* name)
{
    int dest;
    checkStatus(this->model->get_var_nbytes(this->model->self, const_cast<char*>(name), &dest));
    return dest;
}

void BmiCWrapper::GetVarLocation(const char* name, char* location)
{
    checkStatus(this->model->get_var_location(this->model->self, const_cast<char*>(name), location));
}

double BmiCWrapper::GetCurrentTime()
{
    double dest;
    checkStatus(this->model->get_current_time(this->model->self, &dest));
    return dest;
}

double BmiCWrapper::GetStartTime()
{
    double dest;
    checkStatus(this->model->get_start_time(this->model->self, &dest));
    return dest;
}

double BmiCWrapper::GetEndTime()
{
    double dest;
    checkStatus(this->model->get_end_time(this->model->self, &dest));
    return dest;
}

void BmiCWrapper::GetTimeUnits(char* dest)
{
    checkStatus(this->model->get_time_units(this->model->self, dest));
}

double BmiCWrapper::GetTimeStep()
{
    double dest;
    checkStatus(this->model->get_time_step(this->model->self, &dest));
    return dest;
}

void BmiCWrapper::GetValue(const char* name, void* dest)
{
    checkStatus(this->model->get_value(this->model->self, const_cast<char*>(name), dest));
}

void* BmiCWrapper::GetValuePtr(const char* name)
{
    void* dest;
    checkStatus(this->model->get_value_ptr(this->model->self, const_cast<char*>(name), &dest));
    return dest;
}

void* BmiCWrapper::GetValueAtIndices(const char* name, void* dest, int* pts, int numpts)
{
    checkStatus(this->model->get_value_at_indices(this->model->self, const_cast<char*>(name), dest, const_cast<int*>(pts), numpts));
    return dest; // Is this the idea?
}

void BmiCWrapper::SetValue(const char* name, void* src)
{
    checkStatus(this->model->set_value(this->model->self, const_cast<char*>(name), src));
}

void BmiCWrapper::SetValueAtIndices(const char* name, void* values, int* pts, int numpts)
{
    checkStatus(this->model->set_value_at_indices(this->model->self, const_cast<char*>(name), values, pts, numpts));
}

int BmiCWrapper::GetGridSize(int id)
{
    int dest;
    checkStatus(this->model->get_grid_size(this->model->self, id, &dest));
    return dest;
}

int BmiCWrapper::GetGridRank(int id)
{
    int dest;
    checkStatus(this->model->get_grid_size(this->model->self, id, &dest));
    return dest;
}

void BmiCWrapper::GetGridType(int id, char* dest)
{
    checkStatus(this->model->get_grid_type(this->model->self, id, dest));
}

void BmiCWrapper::GetGridShape(int id, int* dest)
{
    checkStatus(this->model->get_grid_shape(this->model->self, id, dest));
}

void BmiCWrapper::GetGridSpacing(int id, double* dest)
{
    checkStatus(this->model->get_grid_spacing(this->model->self, id, dest));
}

void BmiCWrapper::GetGridOrigin(int id, double* dest)
{
    checkStatus(this->model->get_grid_origin(this->model->self, id, dest));
}

void BmiCWrapper::GetGridX(int id, double* dest)
{
    checkStatus(this->model->get_grid_x(this->model->self, id, dest));
}

void BmiCWrapper::GetGridY(int id, double* dest)
{
    checkStatus(this->model->get_grid_y(this->model->self, id, dest));
}

void BmiCWrapper::GetGridZ(int id, double* dest)
{
    checkStatus(this->model->get_grid_z(this->model->self, id, dest));
}

int BmiCWrapper::GetGridNodeCount(int grid)
{
    int dest;
    checkStatus(this->model->get_grid_node_count(this->model->self, grid, &dest));
    return dest;
}

int BmiCWrapper::GetGridEdgeCount(int grid)
{
    int dest;
    checkStatus(this->model->get_grid_edge_count(this->model->self, grid, &dest));
    return dest;
}

int BmiCWrapper::GetGridFaceCount(int grid)
{
    int dest;
    checkStatus(this->model->get_grid_face_count(this->model->self, grid, &dest));
    return dest;
}

void BmiCWrapper::GetGridEdgeNodes(int grid, int *edge_nodes)
{
    checkStatus(this->model->get_grid_edge_nodes(this->model->self, grid, edge_nodes));
}

void BmiCWrapper::GetGridFaceEdges(int grid, int *face_edges)
{
    checkStatus(this->model->get_grid_edge_nodes(this->model->self, grid, face_edges));
}

void BmiCWrapper::GetGridFaceNodes(int grid, int *face_nodes)
{
    checkStatus(this->model->get_grid_face_nodes(this->model->self, grid, face_nodes));
}

void BmiCWrapper::GetGridNodesPerFace(int grid, int *nodes_per_face)
{
    checkStatus(this->model->get_grid_nodes_per_face(this->model->self, grid, nodes_per_face));
}
