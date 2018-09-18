#include "bmi-c/bmi/bmilib.h"
#include "bmi_c_wrapper.h"

BmiCWrapper::BmiCWrapper(BMI_Model* m):model(m){}

BmiCWrapper::~BmiCWrapper()
{
    free(this->model);
}

int BmiCWrapper::initialize(const char* configfile)
{
    return BMI_Initialize(this->model, configfile);
}

int BmiCWrapper::update()
{
    return BMI_Update(this->model);
}

int BmiCWrapper::update_until(double time)
{
    return BMI_Update_until(this->model, time);
}

int BmiCWrapper::update_frac(double time)
{
    return BMI_Update_frac(this->model, time);
}

int BmiCWrapper::finalize()
{
    return BMI_Finalize(this->model);
}

int BmiCWrapper::run_model()
{
    return BMI_Run_model(this->model);
}

int BmiCWrapper::get_component_name(char* dest) const
{
    return BMI_Get_component_name(this->model, dest);
}

int BmiCWrapper::get_input_var_name_count(int* dest) const
{
    return BMI_Get_input_var_name_count(this->model, dest);
}
int BmiCWrapper::get_output_var_name_count(int* dest) const
{
    return BMI_Get_output_var_name_count(this->model, dest);
}
int BmiCWrapper::get_input_var_names(char** dest) const
{
    return BMI_Get_input_var_names(this->model, dest);
}
int BmiCWrapper::get_output_var_names(char** dest) const
{
    return BMI_Get_output_var_names(this->model, dest);
}
int BmiCWrapper::get_var_grid(const char* name, int* dest) const
{
    return BMI_Get_var_grid(this->model, name, dest);
}
int BmiCWrapper::get_var_type(const char* name, char* dest) const
{
    return BMI_Get_var_type(this->model, name, dest);
}
int BmiCWrapper::get_var_itemsize(const char* name, int* dest) const
{
    if (!this->model || !this->model->self) return BMI_FAILURE;
    return this->model->get_var_itemsize(this->model, name, dest);
}
int BmiCWrapper::get_var_units(const char* name, char* dest) const
{
    return BMI_Get_var_units(this->model, name, dest);
}
int BmiCWrapper::get_var_nbytes(const char* name, int* dest) const
{
    return BMI_Get_var_nbytes(this->model, name, dest);
}
int BmiCWrapper::get_current_time(double* dest) const
{
    return BMI_Get_current_time(this->model, dest);
}
int BmiCWrapper::get_start_time(double* dest) const
{
    return BMI_Get_start_time(this->model, dest);
}
int BmiCWrapper::get_end_time(double* dest) const
{
    return BMI_Get_end_time(this->model, dest);
}
int BmiCWrapper::get_time_units(char* dest) const
{
    return BMI_Get_time_units(this->model, dest);
}
int BmiCWrapper::get_time_step(double* dest) const
{
    return BMI_Get_time_step(this->model, dest);
}
int BmiCWrapper::get_value(const char* name, void* dest) const
{
    return BMI_Get_value(this->model, name, dest);
}
int BmiCWrapper::get_value_ptr(const char* name, void** dest)
{
    return BMI_Get_value_ptr(this->model, name, dest);
}
int BmiCWrapper::get_value_at_indices(const char* name, void* dest, const int* pts, int numpts) const
{
    return BMI_Get_value_at_indices(this->model, name, dest, (int*)pts, numpts);
}
int BmiCWrapper::set_value(const char* name, const void* src)
{
    return BMI_Set_value(this->model, name, (void*)src);
}
int BmiCWrapper::set_value_ptr(const char* name, void** src)
{
    return BMI_Set_value_ptr(this->model, name, src);
}
int BmiCWrapper::set_value_at_indices(const char* name, const int* pts, int numpts, const void* src)
{
    return BMI_Set_value_at_indices(this->model, name, (int*)pts, numpts, (void*)src);
}
int BmiCWrapper::get_grid_size(int id, int* dest) const
{
    return BMI_Get_grid_size(this->model, id, dest);
}
int BmiCWrapper::get_grid_rank(int id, int* dest) const
{
    return BMI_Get_grid_rank(this->model, id, dest);
}
int BmiCWrapper::get_grid_type(int id, char* dest) const
{
    return BMI_Get_grid_type(this->model, id, dest);
}
int BmiCWrapper::get_grid_shape(int id, int* dest) const
{
    return BMI_Get_grid_shape(this->model, id, dest);
}
int BmiCWrapper::get_grid_spacing(int id, double* dest) const
{
    return BMI_Get_grid_spacing(this->model, id, dest);
}
int BmiCWrapper::get_grid_origin(int id, double* dest) const
{
    return BMI_Get_grid_origin(this->model, id, dest);
}
int BmiCWrapper::get_grid_x(int id, double* dest) const
{
    return BMI_Get_grid_x(this->model, id, dest);
}
int BmiCWrapper::get_grid_y(int id, double* dest) const
{
    return BMI_Get_grid_y(this->model, id, dest);
}
int BmiCWrapper::get_grid_z(int id, double* dest) const
{
    return BMI_Get_grid_z(this->model, id, dest);
}
int BmiCWrapper::get_grid_cell_count(int id, int* dest) const
{
    return BMI_Get_grid_cell_count(this->model, id, dest);
}
int BmiCWrapper::get_grid_point_count(int id, int* dest) const
{
    return BMI_Get_grid_point_count(this->model, id, dest);
}
int BmiCWrapper::get_grid_vertex_count(int id, int* dest) const
{
    return BMI_Get_grid_vertex_count(this->model, id, dest);
}
int BmiCWrapper::get_grid_connectivity(int id, int* dest) const
{
    return BMI_Get_grid_connectivity(this->model, id, dest);
}
int BmiCWrapper::get_grid_offset(int id, int* dest) const
{
    return BMI_Get_grid_offset(this->model, id, dest);
}
