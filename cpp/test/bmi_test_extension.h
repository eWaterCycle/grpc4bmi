#ifndef BMI_TEST_EXTENSION_H_INCLUDED
#define BMI_TEST_EXTENSION_H_INCLUDED

#include "bmi_cpp_extension.h"

class BmiTestExtension: public BmiCppExtension
{
    public:

        BmiTestExtension(const std::vector<double>&, const std::vector<double>&);
        virtual ~BmiTestExtension();
        
        void initialize (std::string configfile) override;
        int update() override;
        int update_until(double) override;
        int update_frac(double) override;
        int finalize() override;
        int run_model() override;

        std::string get_component_name() const override;
        std::vector<std::string> get_input_var_names() const override;
        std::vector<std::string> get_output_var_names() const override;

        int get_var_grid(std::string name) const override;
        std::string get_var_type(std::string name) const override;
        int get_var_itemsize(std::string name) const override;
        std::string get_var_units(std::string name) const override;
        int get_var_nbytes(std::string name) const override;
        double get_current_time() const override;
        double get_start_time() const override;
        double get_end_time() const override;
        std::string get_time_units() const override;
        double get_time_step() const override;
        
        int get_grid_rank(int id) const override;
        int get_grid_size(int id) const override;
        std::string get_grid_type(int id) const override;
        std::vector<int> get_grid_shape(int id) const override;
        std::vector<double> get_grid_spacing(int id) const override;
        std::vector<double> get_grid_origin(int id) const override;

        std::vector<double> get_grid_x(int id) const override;
        std::vector<double> get_grid_y(int id) const override;
        std::vector<double> get_grid_z(int id) const override;

        int get_grid_cell_count(int id) const override;
        int get_grid_point_count(int id) const override;
        int get_grid_vertex_count(int id) const override;

        std::vector<int> get_grid_connectivity(int id) const override;
        std::vector<int> get_grid_offset(int id) const override;
    
    protected:

        std::vector<int> get_value_int(const std::string& name) const override;
        std::vector<float> get_value_float(const std::string& name) const override;
        std::vector<double> get_value_double(const std::string& name) const override;

        int* get_value_int_ptr(const std::string& name) override;
        float* get_value_float_ptr(const std::string& name) override;
        double* get_value_double_ptr(const std::string& name) override;

        std::vector<int> get_value_int_at_indices(std::string name, const std::vector<int>& indices) const override;
        std::vector<float> get_value_float_at_indices(std::string name, const std::vector<int>& indices) const override;
        std::vector<double> get_value_double_at_indices(std::string name, const std::vector<int>& indices) const override;

        void set_value_int(std::string name, const std::vector<int>& src) override;
        void set_value_float(std::string name, const std::vector<float>& src) override;
        void set_value_double(std::string name, const std::vector<double>& src) override;

        void set_value_int_ptr(std::string name, int* const ptr) override;
        void set_value_float_ptr(std::string name, float* const ptr) override;
        void set_value_double_ptr(std::string name, double* const ptr) override;

        void set_value_int_at_indices(std::string name, const std::vector<int>& indices, const std::vector<int>& values) override;
        void set_value_float_at_indices(std::string name, const std::vector<int>& indices, const std::vector<float>& values) override;
        void set_value_double_at_indices(std::string name, const std::vector<int>& indices, const std::vector<double>& values) override;
    
    private:

        int time_counter;
        std::vector<double> x;
        std::vector<double> y;
        std::vector<double>::size_type size;
        std::vector<std::string> input_vars;
        std::vector<std::string> output_vars;
        int grid_id;
        std::vector<double> Q;
        std::vector<double> h;

        bool has_var(std::string name) const;
};

#endif
