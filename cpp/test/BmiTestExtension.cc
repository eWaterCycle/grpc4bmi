#include <iostream>
#include <stdexcept>
#include <random>
#include "BmiTestExtension.h"

BmiTestExtension::BmiTestExtension(const std::vector<double>& x_, const std::vector<double>& y_):time_counter(0), x(x_), y(y_), size(x_.size() * y_.size()), input_var("water level"), output_var("discharge"), grid_id(121)
{
    this->ivars = std::vector<double>(size, 0.);
    this->ovars = std::vector<double>(size, 0.);
    for(std::vector<double>::size_type i = 0; i < size; ++i)
    {
        this->ovars[i] = std::rand();
    }
}

BmiTestExtension::~BmiTestExtension(){}

void BmiTestExtension::initialize(std::string configfile)
{
    std::cout<<"initializing with "<<configfile;
}

std::string BmiTestExtension::get_component_name() const
{
    return "test_model";
}

std::vector<std::string> BmiTestExtension::get_input_var_names() const
{
    return std::vector<std::string>(1, this->input_var);
}

std::vector<std::string> BmiTestExtension::get_output_var_names() const
{
    return std::vector<std::string>(1, this->output_var);
}

int BmiTestExtension::get_var_grid(std::string name) const
{
    if(name == this->input_var or name == this->output_var)
    {
        return this->grid_id;
    }
    throw std::invalid_argument("unknown variable" + name);
}

std::string BmiTestExtension::get_var_type(std::string name) const
{
    if(name == this->input_var or name == this->output_var)
    {
        return "double";
    }
    throw std::invalid_argument("unknown variable" + name);
}

int BmiTestExtension::get_var_itemsize(std::string name) const
{
    if(name == this->input_var or name == this->output_var)
    {
        return 1;
    }
    throw std::invalid_argument("unknown variable" + name);
}

std::string BmiTestExtension::get_var_units(std::string name) const
{
    if(name == this->input_var)
    {
        return "m";
    }
    if(name == this->output_var)
    {
        return "m3 s-1";
    }
    throw std::invalid_argument("unknown variable" + name);
}

int BmiTestExtension::get_var_nbytes(std::string name) const
{
    if(name == this->input_var or name == this->output_var)
    {
        return sizeof(double);
    }
    throw std::invalid_argument("unknown variable" + name);
}

double BmiTestExtension::get_current_time() const
{
    return this->time_counter;
}

double BmiTestExtension::get_start_time() const
{
    return 0;
}

double BmiTestExtension::get_end_time() const
{
    return 100;
}

std::string BmiTestExtension::get_time_units() const
{
    return "days since 1981-08-29 06:00:00";
}

double BmiTestExtension::get_time_step() const
{
    return 1;
}

int BmiTestExtension::get_grid_rank(int id) const
{
    if(id == this->grid_id)
    {
        return 2;
    }
    throw std::invalid_argument("unknown grid id argument");
}

int BmiTestExtension::get_grid_size(int id) const
{
    if(id == this->grid_id)
    {
        return 1;
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::string BmiTestExtension::get_grid_type(int id) const
{
    if(id == this->grid_id)
    {
        return "rectilinear";
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::get_grid_shape(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<int>(1, 1);
    }
    throw std::invalid_argument("unknown grid id argument");
}


std::vector<double> BmiTestExtension::get_grid_spacing(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<double>(1, 0.);
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<double> BmiTestExtension::get_grid_origin(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<double>(1, 0.);
    }
    throw std::invalid_argument("unknown grid id argument");

}

std::vector<double> BmiTestExtension::get_grid_x(int id) const
{
    if(id == this->grid_id)
    {
        return this->x;
    }
    throw std::invalid_argument("unknown grid id argument");

}

std::vector<double> BmiTestExtension::get_grid_y(int id) const
{
    if(id == this->grid_id)
    {
        return this->y;
    }
    throw std::invalid_argument("unknown grid id argument");
        
}
std::vector<double> BmiTestExtension::get_grid_z(int id) const
{
    if(id == 1)
    {
        return std::vector<double>(1, 0.);
    }
    throw std::invalid_argument("unknown grid id argument");
    
}

int BmiTestExtension::get_grid_cell_count(int id) const
{
    if(id == this->grid_id)
    {
        return this->size;
    }
    throw std::invalid_argument("unknown grid id argument");
    
}
int BmiTestExtension::get_grid_point_count(int id) const
{
    if(id == this->grid_id)
    {
        return this->size;
    }
    throw std::invalid_argument("unknown grid id argument");
}
int BmiTestExtension::get_grid_vertex_count(int id) const
{
    if(id == this->grid_id)
    {
        return this->size;
    }
    throw std::invalid_argument("unknown grid id argument");
    
}

std::vector<int> BmiTestExtension::get_grid_connectivity(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<int>();
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::get_grid_offset(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<int>();
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::get_value_int(const std::string& name) const
{
    throw std::invalid_argument("invalid variable" + name);
}

std::vector<float> BmiTestExtension::get_value_float(const std::string& name) const
{
    throw std::invalid_argument("invalid variable" + name);
}

std::vector<double> BmiTestExtension::get_value_double(const std::string& name) const
{
    if(name == this->output_var)
    {
        return this->ovars;
    }
    throw std::invalid_argument("invalid variable" + name);
}

int* BmiTestExtension::get_value_int_ptr(const std::string& name)
{
    throw std::invalid_argument("invalid variable" + name);
}

float* BmiTestExtension::get_value_float_ptr(const std::string& name)
{
    throw std::invalid_argument("invalid variable" + name);
}

double* BmiTestExtension::get_value_double_ptr(const std::string& name)
{
    throw std::invalid_argument("invalid variable" + name);
}

std::vector<int> BmiTestExtension::get_value_int_at_indices(std::string name, const std::vector<int>& indices) const
{
    throw std::invalid_argument("invalid variable" + name);
}

std::vector<float> BmiTestExtension::get_value_float_at_indices(std::string name, const std::vector<int>& indices) const
{
    throw std::invalid_argument("invalid variable" + name);
}

std::vector<double> BmiTestExtension::get_value_double_at_indices(std::string name, const std::vector<int>& indices) const
{
    if(name == this->output_var)
    {
        std::vector<double>result(indices.size(), 0.);
        for(std::vector<double>::size_type i = 0; i < indices.size(); ++i)
        {
            result[i] = this->ovars[indices[i]];
        }
        return result;
    }
    throw std::invalid_argument("invalid variable" + name);
}

void BmiTestExtension::set_value_int(std::string name, const std::vector<int>& src)
{
    throw std::invalid_argument("invalid variable" + name);
}

void BmiTestExtension::set_value_float(std::string name, const std::vector<float>& src)
{
    throw std::invalid_argument("invalid variable" + name);
}

void BmiTestExtension::set_value_double(std::string name, const std::vector<double>& src)
{
    std::vector<double>::size_type n = std::min(src.size(), this->size);
    for(std::vector<double>::size_type i = 0; i < n; ++i)
    {
        this->ivars[i] = src[i];
    }
}

void BmiTestExtension::set_value_int_ptr(std::string name, int* const ptr)
{
    throw std::invalid_argument("invalid variable" + name);
}
void BmiTestExtension::set_value_float_ptr(std::string name, float* const ptr)
{
    throw std::invalid_argument("invalid variable" + name);
}
void BmiTestExtension::set_value_double_ptr(std::string name, double* const ptr)
{
    throw std::invalid_argument("invalid variable" + name);
}

void BmiTestExtension::set_value_int_at_indices(std::string name, const std::vector<int>& indices, const std::vector<int>& values)
{
    throw std::invalid_argument("invalid variable" + name);
}
void BmiTestExtension::set_value_float_at_indices(std::string name, const std::vector<int>& indices, const std::vector<float>& values)
{
    throw std::invalid_argument("invalid variable" + name);
}
void BmiTestExtension::set_value_double_at_indices(std::string name, const std::vector<int>& indices, const std::vector<double>& values)
{
    if(name == this->input_var)
    {
        for(std::vector<double>::size_type i = 0; i < indices.size(); ++i)
        {
            this->ivars[i] = values[indices[i]];
        }
    }
    throw std::invalid_argument("invalid variable" + name);
}
