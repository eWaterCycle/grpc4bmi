#ifndef BMI_C_WRAPPER_H_INCLUDED
#define BMI_C_WRAPPER_H_INCLUDED

#include "bmi_class.h"
#include "bmi-c/bmi/bmi.h"

class BmiCWrapper: public Bmi
{
  public:
    BmiCWrapper(BMI_Model*);
    ~BmiCWrapper() override;

    int initialize(const char* configfile) override;
    int update() override;
    int update_until(double time) override;
    int update_frac(double time) override;
    int finalize() override;
    int run_model() override;

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

  private:
    BMI_Model* const model;
};

#endif /*BMI_C_WRAPPER_H_INCLUDED*/
