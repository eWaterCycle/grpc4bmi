#ifndef BMI_CLASS_H_INCLUDED
#define BMI_CLASS_H_INCLUDED

#include <string>

#define BMI_SUCCESS (0)
#define BMI_FAILURE (1) 
#define BMI_MAX_UNITS_NAME (2048)
#define BMI_MAX_TYPE_NAME (2048)
#define BMI_MAX_COMPONENT_NAME (2048)
#define BMI_MAX_VAR_NAME (2048)

class Bmi 
{
  public:

    Bmi(){};
    virtual ~Bmi(){};

    virtual int initialize(const char* configfile) = 0;
    virtual int update() = 0;
    virtual int update_until(double time) = 0;
    virtual int update_frac(double time) = 0;
    virtual int finalize() = 0;
    virtual int run_model() = 0;

    virtual int get_component_name(char* dest) const = 0;
    virtual int get_input_var_name_count(int* dest) const = 0;
    virtual int get_output_var_name_count(int* dest) const = 0;
    virtual int get_input_var_names(char** dest) const = 0;
    virtual int get_output_var_names(char** dest) const = 0;
    
    virtual int get_var_grid(const char* name, int* dest) const = 0;
    virtual int get_var_type(const char* name, char* dest) const = 0;
    virtual int get_var_itemsize(const char* name, int* dest) const = 0;
    virtual int get_var_units(const char* name, char* dest) const = 0;
    virtual int get_var_nbytes(const char* name, int* dest) const = 0;
    virtual int get_current_time(double* dest) const = 0;
    virtual int get_start_time(double* dest) const = 0;
    virtual int get_end_time(double* dest) const = 0;
    virtual int get_time_units(char* dest) const = 0;
    virtual int get_time_step(double* dest) const = 0;
    
    
    virtual int get_value(const char* name, void* dest) const = 0;
    virtual int get_value_ptr(const char* name, void** dest) = 0;
    virtual int get_value_at_indices(const char* name, void* dest, const int* pts, int numpts) const = 0;

    virtual int set_value(const char* name, const void* src) = 0;
    virtual int set_value_ptr(const char* name, void** src) = 0;
    virtual int set_value_at_indices(const char* name, const int* pts, int numpts, const void* src) = 0;

    virtual int get_grid_size(int id, int* dest) const = 0;
    virtual int get_grid_rank(int id, int* dest) const = 0;
    virtual int get_grid_type(int id, char* dest) const = 0;
    virtual int get_grid_shape(int id, int* dest) const = 0;
    virtual int get_grid_spacing(int id, double* dest) const = 0;
    virtual int get_grid_origin(int id, double* dest) const = 0;
    virtual int get_grid_x(int id, double* dest) const = 0;
    virtual int get_grid_y(int id, double* dest) const = 0;
    virtual int get_grid_z(int id, double* dest) const = 0;
    virtual int get_grid_cell_count(int id, int* dest) const = 0;
    virtual int get_grid_point_count(int id, int* dest) const = 0;
    virtual int get_grid_vertex_count(int id, int* dest) const = 0;
    virtual int get_grid_connectivity(int id, int* dest) const = 0;
    virtual int get_grid_offset(int id, int* dest) const = 0;
};

// TODO: converter to C-BMI struct
// BMI_Model* register_bmi_class(Bmi* instance);

#endif
