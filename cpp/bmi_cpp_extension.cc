#include <algorithm>
#include <cstring>
#include "bmi_cpp_extension.h"

BmiCppExtension::BmiCppExtension(){}

BmiCppExtension::~BmiCppExtension(){}

int BmiCppExtension::initialize(const char* configfile)
{
    this->initialize(std::string(configfile));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_component_name(char* dest) const
{
    std::string s = this->get_component_name();
    strncpy(dest, s.c_str(), s.size());
    dest[s.size()] = '\0';
    return BMI_SUCCESS;
}

int BmiCppExtension::get_input_var_name_count(int* dest) const
{
    *dest = this->get_input_var_names().size();
    return BMI_SUCCESS;
}

int BmiCppExtension::get_output_var_name_count(int* dest) const
{
    *dest = this->get_output_var_names().size();
    return BMI_SUCCESS;
}
    
int BmiCppExtension::get_input_var_names(char** dest) const
{
    std::vector<std::string> src = this->get_input_var_names();
    for(std::vector<std::string>::size_type i = 0; i < src.size(); i++)
    {
        strncpy(dest[i], src[i].c_str(), src[i].size());
        dest[i][src[i].size()] = '\0';
    }
    return BMI_SUCCESS;
}
    
int BmiCppExtension::get_output_var_names(char** dest) const
{
    std::vector<std::string> src = this->get_output_var_names();
    for(std::vector<std::string>::size_type i = 0; i < src.size(); i++)
    {
        strncpy(dest[i], src[i].c_str(), src[i].size());
        dest[i][src[i].size()] = '\0';
    }
    return BMI_SUCCESS;
}

int BmiCppExtension::get_var_grid(const char* name, int* dest) const
{
    *dest = this->get_var_grid(std::string(name));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_var_type(const char* name, char* dest) const
{
    std::string type = this->get_var_type(std::string(name));
    strncpy(dest, type.c_str(), type.size());
    dest[type.size()] = '\0';
    return BMI_SUCCESS;
}

int BmiCppExtension::get_var_itemsize(const char* name, int* dest) const
{
    *dest = this->get_var_itemsize(std::string(name));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_var_units(const char* name, char* dest) const
{
    std::string units = this->get_var_units(std::string(name));
    strncpy(dest, units.c_str(), units.size());
    dest[units.size()] = '\0';
    return BMI_SUCCESS;
}

int BmiCppExtension::get_var_nbytes(const char* name, int* dest) const
{
    *dest = this->get_var_nbytes(std::string(name));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_current_time(double* dest) const
{
    *dest = this->get_current_time();
    return BMI_SUCCESS;
}

int BmiCppExtension::get_start_time(double* dest) const
{
    *dest = this->get_start_time();
    return BMI_SUCCESS;
}

int BmiCppExtension::get_end_time(double* dest) const
{
    *dest = this->get_end_time();
    return BMI_SUCCESS;
}

int BmiCppExtension::get_time_units(char* dest) const
{
    std::string units = this->get_time_units();
    strncpy(dest, units.c_str(), units.size());
    dest[units.size()] = '\0';
    return BMI_SUCCESS;
}

int BmiCppExtension::get_time_step(double* dest) const
{
    *dest = this->get_time_step();
    return BMI_SUCCESS;
}
int BmiCppExtension::get_value(const char* name, void* dest) const
{
    char type = this->find_type(std::string(name));
    if(type == 'i')
    {
        std::vector<int> vals = this->get_value_int(std::string(name));
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(int));
        return BMI_SUCCESS;
    }
    if(type == 'f')
    {
        std::vector<float> vals = this->get_value_float(std::string(name));
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(float));
        return BMI_SUCCESS;
    }
    if(type == 'd')
    {
        std::vector<double> vals = this->get_value_double(std::string(name));
        memcpy(dest, vals.data(), vals.size()*sizeof(double));
        return BMI_SUCCESS;
    }
    return BMI_FAILURE;
}

int BmiCppExtension::get_value_ptr(const char* name, void** dest)
{
    char type = this->find_type(std::string(name));
    if(type == 'i')
    {
        *dest = static_cast<void*>(this->get_value_int_ptr(std::string(name)));
        return BMI_SUCCESS;
    }
    if(type == 'f')
    {
        *dest = static_cast<void*>(this->get_value_float_ptr(std::string(name)));
        return BMI_SUCCESS;
    }
    if(type == 'd')
    {
        *dest = static_cast<void*>(this->get_value_double_ptr(std::string(name)));
        return BMI_SUCCESS;
    }
    return BMI_FAILURE;

}

int BmiCppExtension::get_value_at_indices(const char* name, void* dest, const int* pts, int numpts) const
{
    char type = this->find_type(std::string(name));
    std::vector<int> indices;
    indices.assign(pts, pts + numpts);
    if(type == 'i')
    {
        std::vector<int> vals = this->get_value_int_at_indices(std::string(name), indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(int));
        return BMI_SUCCESS;
    }
    if(type == 'f')
    {
        std::vector<float> vals = this->get_value_float_at_indices(std::string(name), indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(float));
        return BMI_SUCCESS;
    }
    if(type == 'd')
    {
        std::vector<double> vals = this->get_value_double_at_indices(std::string(name), indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(double));
        return BMI_SUCCESS;
    }
    return BMI_FAILURE;
}

int BmiCppExtension::set_value(const char* name, const void* src)
{
    char type = this->find_type(std::string(name));
    int nbytes;
    this->get_var_nbytes(name, &nbytes);
    if(type == 'i')
    {
        std::vector<int> vals;
        vals.assign(static_cast<const int*>(src), static_cast<const int*>(src) + nbytes / sizeof(int));
        this->set_value_int(std::string(name), vals);
        return BMI_SUCCESS;
    }
    if(type == 'f')
    {
        std::vector<float> vals;
        vals.assign(static_cast<const float*>(src), static_cast<const float*>(src) + nbytes / sizeof(float));
        this->set_value_float(std::string(name), vals);
        return BMI_SUCCESS;
    }
    if(type == 'd')
    {
        std::vector<double> vals;
        vals.assign(static_cast<const double*>(src), static_cast<const double*>(src) + nbytes / sizeof(double));
        this->set_value_double(std::string(name), vals);
        return BMI_SUCCESS;
    }
    return BMI_FAILURE;
}

int BmiCppExtension::set_value_ptr(const char* name, void** src)
{
    char type = this->find_type(std::string(name));
    if(type == 'i')
    {
        this->set_value_int_ptr(std::string(name), static_cast<int*>(*src));
        return BMI_SUCCESS;
    }
    if(type == 'f')
    {
        this->set_value_float_ptr(std::string(name), static_cast<float*>(*src));
        return BMI_SUCCESS;
    }
    if(type == 'd')
    {
        this->set_value_double_ptr(std::string(name), static_cast<double*>(*src));
        return BMI_SUCCESS;
    }
    return BMI_FAILURE;
}

int BmiCppExtension::set_value_at_indices(const char* name, const int* pts, int numpts, const void* src)
{
    char type = this->find_type(std::string(name));
    std::vector<int> indices(pts, pts + numpts);
    if(type == 'i')
    {
        std::vector<int> vals;
        vals.assign(static_cast<const int*>(src), static_cast<const int*>(src) + numpts);
        this->set_value_int_at_indices(std::string(name), indices, vals);
        return BMI_SUCCESS;
    }
    if(type == 'f')
    {
        std::vector<float> vals;
        vals.assign(static_cast<const float*>(src), static_cast<const float*>(src) + numpts);
        this->set_value_float_at_indices(std::string(name), indices, vals);
        return BMI_SUCCESS;
    }
    if(type == 'd')
    {
        std::vector<double> vals;
        vals.assign(static_cast<const double*>(src), static_cast<const double*>(src) + numpts);
        this->set_value_double_at_indices(std::string(name), indices, vals);
        return BMI_SUCCESS;
    }
    return BMI_FAILURE;

}

int BmiCppExtension::get_grid_size(int id, int* dest) const
{
    *dest = this->get_grid_size(id);
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_rank(int id, int* dest) const
{
    *dest = this->get_grid_rank(id);
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_type(int id, char* dest) const
{
    std::string type = this->get_grid_type(id);
    strncpy(dest, type.c_str(), type.size());
    dest[type.size()] = '\0';
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_shape(int id, int* dest) const
{
    std::vector<int> shape = this->get_grid_shape(id);
    memcpy(dest, shape.data(), shape.size()*sizeof(int));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_spacing(int id, double* dest) const
{
    std::vector<double> s = this->get_grid_spacing(id);
    memcpy(dest, s.data(), s.size()*sizeof(double));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_origin(int id, double* dest) const
{
    std::vector<double> o = this->get_grid_spacing(id);
    memcpy(dest, o.data(), o.size()*sizeof(double));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_x(int id, double* dest) const
{
    std::vector<double> x = this->get_grid_x(id);
    memcpy(dest, x.data(), x.size()*sizeof(double));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_y(int id, double* dest) const
{
    std::vector<double> y = this->get_grid_y(id);
    memcpy(dest, y.data(), y.size()*sizeof(double));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_z(int id, double* dest) const
{
    std::vector<double> z = this->get_grid_z(id);
    memcpy(dest, z.data(), z.size()*sizeof(double));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_cell_count(int id, int* dest) const
{
    *dest = this->get_grid_cell_count(id);
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_point_count(int id, int* dest) const
{
    *dest = this->get_grid_point_count(id);
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_vertex_count(int id, int* dest) const
{
    *dest = this->get_grid_vertex_count(id);
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_connectivity(int id, int* dest) const
{
    std::vector<int> c = this->get_grid_connectivity(id);
    memcpy(dest, c.data(), c.size()*sizeof(int));
    return BMI_SUCCESS;
}

int BmiCppExtension::get_grid_offset(int id, int* dest) const
{
    std::vector<int> o = this->get_grid_offset(id);
    memcpy(dest, o.data(), o.size()*sizeof(int));
    return BMI_SUCCESS;
}

char BmiCppExtension::find_type(const std::string& varname) const
{
    std::string vartype = this->get_var_type(varname);
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
