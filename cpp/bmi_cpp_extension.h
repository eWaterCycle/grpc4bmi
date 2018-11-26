#ifndef BMI_CPP_EXTENSION_H_INCLUDED
#define BMI_CPP_EXTENSION_H_INCLUDED

#include <string>
#include <vector>
#include <stdexcept>
#include "bmi_class.h"


class BmiCppExtension: public Bmi 
{
  public:
      
    BmiCppExtension();
    virtual ~BmiCppExtension();
    virtual void initialize (std::string configfile) = 0;

    virtual std::string get_component_name() const = 0;
    virtual std::vector<std::string> get_input_var_names() const = 0;
    virtual std::vector<std::string> get_output_var_names() const = 0;

    virtual int get_var_grid(std::string name) const = 0;
    virtual std::string get_var_type(std::string name) const = 0;
    virtual int get_var_itemsize(std::string name) const = 0;
    virtual std::string get_var_units(std::string name) const = 0;
    virtual int get_var_nbytes(std::string name) const = 0;
    virtual double get_current_time() const = 0;
    virtual double get_start_time() const = 0;
    virtual double get_end_time() const = 0;
    virtual std::string get_time_units() const = 0;
    virtual double get_time_step() const = 0;

    template<typename T> std::vector<T> get_value(std::string name) const
    {
        std::vector<T> result(this->get_var_nbytes(name.c_str())/sizeof(T));
        this->get_value(name.c_str(), (void*)result.data());
        return result;
    }
    template<typename T> T* get_value_ptr(std::string name)
    {
        T* ptr;
        this->get_value_ptr(name.c_str(), (void**)&ptr);
        return ptr;
    }
    template<typename T> std::vector<T> get_value_at_indices(std::string name, const std::vector<int>& indices) const
    {
        std::vector<T> result(indices.size());
        this->get_value_at_indices(name.c_str(), (void*)result.data(), indices.data(), indices.size());
        return result;
    }

    template<typename T> void set_value(std::string name, const std::vector<T>& src)
    {
        this->set_value(name.c_str(), static_cast<const void*>(src.data()));
    }
    template<typename T> void set_value_ptr(std::string name, T* const ptr)
    {
        this->set_value_ptr(name.c_str(), (void**)(&ptr));
    }
    template<typename T> void set_value_at_indices(std::string name, const std::vector<int>& indices, const std::vector<T>& values)
    {
        this->set_value_at_indices(name.c_str(), indices.data(), indices.size(), static_cast<const void*>(values.data()));
    }

    virtual int get_grid_rank(int id) const = 0;
    virtual int get_grid_size(int id) const = 0;
    virtual std::string get_grid_type(int id) const = 0;
    virtual std::vector<int> get_grid_shape(int id) const = 0;
    virtual std::vector<double> get_grid_spacing(int id) const = 0;
    virtual std::vector<double> get_grid_origin(int id) const = 0;

    virtual std::vector<double> get_grid_x(int id) const = 0;
    virtual std::vector<double> get_grid_y(int id) const = 0;
    virtual std::vector<double> get_grid_z(int id) const = 0;

    virtual int get_grid_cell_count(int id) const = 0;
    virtual int get_grid_point_count(int id) const = 0;
    virtual int get_grid_vertex_count(int id) const = 0;

    virtual std::vector<int> get_grid_connectivity(int id) const = 0;
    virtual std::vector<int> get_grid_offset(int id) const = 0;

    int initialize(const char* configfile) override;

    int get_component_name(char* dest) const override;
    int get_input_var_name_count(int* dest) const override;
    int get_output_var_name_count(int* dest) const override;
    int get_input_var_names(char** dest) const override;
    int get_output_var_names(char** dest) const override;
    
    int get_var_grid(const char* name, int* dest) const override;
    int get_var_type(const char* name, char* dest) const override;
    int get_var_itemsize(const char* name, int* dest) const override;
    int get_var_units(const char* name, char* dest) const override;
    int get_var_nbytes(const char* name, int* dest) const override;
    int get_current_time(double* dest) const override;
    int get_start_time(double* dest) const override;
    int get_end_time(double* dest) const override;
    int get_time_units(char* dest) const override;
    int get_time_step(double* dest) const override;
    
    int get_value(const char* name, void* dest) const override;
    int get_value_ptr(const char* name, void** dest) override;
    int get_value_at_indices(const char* name, void* dest, const int* pts, int numpts) const override;

    int set_value(const char* name, const void* src) override;
    int set_value_ptr(const char* name, void** src) override;
    int set_value_at_indices(const char* name, const int* pts, int numpts, const void* src) override;

    int get_grid_size(int id, int* dest) const override;
    int get_grid_rank(int id, int* dest) const override;
    int get_grid_type(int id, char* dest) const override;
    int get_grid_shape(int id, int* dest) const override;
    int get_grid_spacing(int id, double* dest) const override;
    int get_grid_origin(int id, double* dest) const override;
    int get_grid_x(int id, double* dest) const override;
    int get_grid_y(int id, double* dest) const override;
    int get_grid_z(int id, double* dest) const override;
    int get_grid_cell_count(int id, int* dest) const override;
    int get_grid_point_count(int id, int* dest) const override;
    int get_grid_vertex_count(int id, int* dest) const override;
    int get_grid_connectivity(int id, int* dest) const override;
    int get_grid_offset(int id, int* dest) const override;

  protected:

    virtual std::vector<int> get_value_int(const std::string& name) const = 0;
    virtual std::vector<float> get_value_float(const std::string& name) const = 0;
    virtual std::vector<double> get_value_double(const std::string& name) const = 0;

    virtual int* get_value_int_ptr(const std::string& name) = 0;
    virtual float* get_value_float_ptr(const std::string& name) = 0;
    virtual double* get_value_double_ptr(const std::string& name) = 0;

    virtual std::vector<int> get_value_int_at_indices(std::string name, const std::vector<int>& indices) const = 0;
    virtual std::vector<float> get_value_float_at_indices(std::string name, const std::vector<int>& indices) const = 0;
    virtual std::vector<double> get_value_double_at_indices(std::string name, const std::vector<int>& indices) const = 0;

    virtual void set_value_int(std::string name, const std::vector<int>& src) = 0;
    virtual void set_value_float(std::string name, const std::vector<float>& src) = 0;
    virtual void set_value_double(std::string name, const std::vector<double>& src) = 0;

    virtual void set_value_int_ptr(std::string name, int* const ptr) = 0;
    virtual void set_value_float_ptr(std::string name, float* const ptr) = 0;
    virtual void set_value_double_ptr(std::string name, double* const ptr) = 0;

    virtual void set_value_int_at_indices(std::string name, const std::vector<int>& indices, const std::vector<int>& values) = 0;
    virtual void set_value_float_at_indices(std::string name, const std::vector<int>& indices, const std::vector<float>& values) = 0;
    virtual void set_value_double_at_indices(std::string name, const std::vector<int>& indices, const std::vector<double>& values) = 0;

  private:

    char find_type(const std::string& name) const;
};

#endif /*BMI_CPP_EXTENSION_H_INCLUDED*/
