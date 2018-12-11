#include <iostream>
#include <algorithm>
#include <stdexcept>
#include <random>
#include "bmi_test_extension.h"

BmiTestExtension::BmiTestExtension(const std::vector<double>& x_, const std::vector<double>& y_):time_counter(0), x(x_), y(y_), size(x_.size() * y_.size()), input_vars({"water level"}), output_vars({"discharge", "water level"}), grid_id(121)
{
    this->h = std::vector<double>(size, 0.);
    this->Q = std::vector<double>(size, 0.);
    for(std::vector<double>::size_type i = 0; i < size; ++i)
    {
        this->Q[i] = 2500.*((double)std::rand())/RAND_MAX;
        this->h[i] = 2.5*((double)std::rand())/RAND_MAX;
    }
}

int BmiTestExtension::update()
{
    for(std::vector<double>::size_type i = 0; i < size; ++i)
    {
        this->Q[i] = 2500.*((double)std::rand())/RAND_MAX;
        this->h[i] = 2.5*((double)std::rand())/RAND_MAX;
    }
    this->time_counter++;
}

int BmiTestExtension::update_until(double step)
{
    while((double)(this->time_counter + 1) <= step)
    {
        this->update();
    }
}

int BmiTestExtension::update_frac(double frac)
{
    return BMI_FAILURE;
}

int BmiTestExtension::finalize()
{
    return BMI_SUCCESS;
}

int BmiTestExtension::run_model()
{
    this->update_until(1000);
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
    return this->input_vars;
}

std::vector<std::string> BmiTestExtension::get_output_var_names() const
{
    return this->output_vars;
}

bool BmiTestExtension::has_var(std::string name) const
{
    return std::find(this->input_vars.begin(), this->input_vars.end(), name) != this->input_vars.end() or std::find(this->output_vars.begin(), this->output_vars.end(), name) != this->output_vars.end();
}

int BmiTestExtension::get_var_grid(std::string name) const
{
    if(this->has_var(name))
    {
        return this->grid_id;
    }
    throw std::invalid_argument("unknown variable: " + name);
}

std::string BmiTestExtension::get_var_type(std::string name) const
{
    if(this->has_var(name))
    {
        return "double";
    }
    throw std::invalid_argument("unknown variable: " + name);
}

int BmiTestExtension::get_var_itemsize(std::string name) const
{
    if(this->has_var(name))
    {
        return sizeof(double);
    }
    throw std::invalid_argument("unknown variable: " + name);
}

std::string BmiTestExtension::get_var_units(std::string name) const
{
    if(name == "water level")
    {
        return "m";
    }
    if(name == "discharge")
    {
        return "m3 s-1";
    }
    throw std::invalid_argument("unknown variable: " + name);
}

int BmiTestExtension::get_var_nbytes(std::string name) const
{
    if(this->has_var(name))
    {
        return sizeof(double) * this->size;
    }
    throw std::invalid_argument("unknown variable: " + name);
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
        return this->size;
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
        return {static_cast<int>(this->x.size()), static_cast<int>(this->y.size())};
    }
    throw std::invalid_argument("unknown grid id argument");
}


std::vector<double> BmiTestExtension::get_grid_spacing(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<double>();
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<double> BmiTestExtension::get_grid_origin(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<double>();
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
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<float> BmiTestExtension::get_value_float(const std::string& name) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<double> BmiTestExtension::get_value_double(const std::string& name) const
{
    if(name == "discharge")
    {
        return this->Q;
    }
    if(name == "water level")
    {
        return this->h;
    }
    throw std::invalid_argument("invalid variable: " + name);
}

int* BmiTestExtension::get_value_int_ptr(const std::string& name)
{
    throw std::invalid_argument("invalid variable: " + name);
}

float* BmiTestExtension::get_value_float_ptr(const std::string& name)
{
    throw std::invalid_argument("invalid variable: " + name);
}

double* BmiTestExtension::get_value_double_ptr(const std::string& name)
{
    if(name == "discharge")
    {
        return &(this->Q.data()[0]);
    }
    if(name == "water level")
    {
        return &(this->h.data()[0]);
    }
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<int> BmiTestExtension::get_value_int_at_indices(std::string name, const std::vector<int>& indices) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<float> BmiTestExtension::get_value_float_at_indices(std::string name, const std::vector<int>& indices) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<double> BmiTestExtension::get_value_double_at_indices(std::string name, const std::vector<int>& indices) const
{
    const std::vector<double>* ref = NULL;
    if(name == "discharge")
    {
        ref = &(this->Q);
    }
    if(name == "water level")
    {
        ref = &(this->h);
    }
    if(ref == NULL)
    {
        throw std::invalid_argument("invalid variable: " + name);
    }
    std::vector<double>result(indices.size(), 0.);
    for(std::vector<double>::size_type i = 0; i < indices.size(); ++i)
    {
        result[i] = (*ref)[indices[i]];
    }
    return result;
}

void BmiTestExtension::set_value_int(std::string name, const std::vector<int>& src)
{
    throw std::invalid_argument("invalid variable: " + name);
}

void BmiTestExtension::set_value_float(std::string name, const std::vector<float>& src)
{
    throw std::invalid_argument("invalid variable: " + name);
}

void BmiTestExtension::set_value_double(std::string name, const std::vector<double>& src)
{
    if(name == "water level")
    {
        for(std::vector<double>::size_type i = 0; i < this->size; ++i)
        {
            this->h[i] = src[i];
        }
    }
    else
    {
        throw std::invalid_argument("invalid variable: " + name);
    }
}

void BmiTestExtension::set_value_int_ptr(std::string name, int* const ptr)
{
    throw std::invalid_argument("invalid variable: " + name);
}
void BmiTestExtension::set_value_float_ptr(std::string name, float* const ptr)
{
    throw std::invalid_argument("invalid variable: " + name);
}
void BmiTestExtension::set_value_double_ptr(std::string name, double* const ptr)
{
    throw std::invalid_argument("invalid variable: " + name);
}

void BmiTestExtension::set_value_int_at_indices(std::string name, const std::vector<int>& indices, const std::vector<int>& values)
{
    throw std::invalid_argument("invalid variable: " + name);
}
void BmiTestExtension::set_value_float_at_indices(std::string name, const std::vector<int>& indices, const std::vector<float>& values)
{
    throw std::invalid_argument("invalid variable: " + name);
}
void BmiTestExtension::set_value_double_at_indices(std::string name, const std::vector<int>& indices, const std::vector<double>& values)
{
    if(name == "water level")
    {
        for(std::vector<double>::size_type i = 0; i < indices.size(); ++i)
        {
            this->h[indices[i]] = values[i];
        }
    }
    else
    {
        throw std::invalid_argument("invalid variable: " + name);    
    }
}
