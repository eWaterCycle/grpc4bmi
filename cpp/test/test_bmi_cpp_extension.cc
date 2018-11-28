#include <assert.h>
#include <stdexcept>
#include <cstring>
#include "bmi_cpp_extension.h"
#include "test/bmi_test_extension.h"

void test_initialize(Bmi* b)
{
    const char* s = "somestring";
    b->initialize(s);
    assert(true);
}

void test_component_name(Bmi* b)
{
    char component_name_char[BMI_MAX_COMPONENT_NAME];
    b->get_component_name(component_name_char);
    std::string check_string(component_name_char, strlen(component_name_char));
    std::string component_name_string = static_cast<const BmiCppExtension*>(b)->get_component_name();
    assert(check_string == component_name_string);
}

void test_input_var_count(Bmi* b)
{
    int count = 0;
    b->get_input_var_name_count(&count);
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    assert(input_vars.size() == count);
}

void test_input_vars(Bmi* b)
{
    int count = 0;
    b->get_input_var_name_count(&count);
    char** names = (char**) malloc(sizeof(char*)*count);
    for(int i = 0; i < count; i++)
    {
        names[i] = (char*) malloc(sizeof(char)*BMI_MAX_VAR_NAME);
    }
    b->get_input_var_names(names);
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    for(std::vector<std::string>::size_type i = 0; i < input_vars.size(); i++)
    {
        std::string check_string(names[i], strlen(names[i]));
        assert(input_vars[i] == check_string);
    }
    for(int i = 0; i < count; i++)
    {
        free(names[i]);
    }
    free(names);
}

void test_output_var_count(Bmi* b)
{
    int count = 0;
    b->get_output_var_name_count(&count);
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    assert(output_vars.size() == count);
}

void test_output_vars(Bmi* b)
{
    int count = 0;
    b->get_output_var_name_count(&count);
    char** names = (char**) malloc(sizeof(char*)*count);
    for(int i = 0; i < count; i++)
    {
        names[i] = (char*) malloc(sizeof(char)*BMI_MAX_VAR_NAME);
    }
    b->get_output_var_names(names);
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::size_type i = 0; i < output_vars.size(); i++)
    {
        std::string check_string(names[i], strlen(names[i]));
        assert(output_vars[i] == check_string);
    }
    for(int i = 0; i < count; i++)
    {
        free(names[i]);
    }
    free(names);
}

void test_var_grid(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        int id = -999;
        b->get_var_grid(it->c_str(), &id);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_grid(*it) == id);
    }
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        int id = -999;
        b->get_var_grid(it->c_str(), &id);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_grid(*it) == id);
    }
}

void test_var_type(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        char type[BMI_MAX_VAR_NAME];
        b->get_var_type(it->c_str(), type);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_type(*it) == std::string(type, strlen(type)));
    }
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        char type[BMI_MAX_VAR_NAME];
        b->get_var_type(it->c_str(), type);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_type(*it) == std::string(type, strlen(type)));
    }
}

void test_var_itemsize(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        int size = -999;
        b->get_var_itemsize(it->c_str(), &size);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_itemsize(*it) == size);
    }
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        int size = -999;
        b->get_var_itemsize(it->c_str(), &size);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_itemsize(*it) == size);
    }
}

void test_var_nbytes(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        int size = -999;
        b->get_var_nbytes(it->c_str(), &size);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_nbytes(*it) == size);
    }
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        int size = -999;
        b->get_var_nbytes(it->c_str(), &size);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_nbytes(*it) == size);
    }
}

void test_var_units(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        char units[BMI_MAX_UNITS_NAME];
        b->get_var_units(it->c_str(), units);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_units(*it) == std::string(units, strlen(units)));
    }
    std::vector<std::string> input_vars = static_cast<const BmiCppExtension*>(b)->get_input_var_names();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        char units[BMI_MAX_UNITS_NAME];
        b->get_var_units(it->c_str(), units);
        assert(static_cast<const BmiCppExtension*>(b)->get_var_units(*it) == std::string(units, strlen(units)));
    }
}

void test_start_time(Bmi* b)
{
    double t = -999.;
    b->get_start_time(&t);
    assert(t == static_cast<const BmiCppExtension*>(b)->get_start_time());
}

void test_end_time(Bmi* b)
{
    double t = -999.;
    b->get_end_time(&t);
    assert(t == static_cast<const BmiCppExtension*>(b)->get_end_time());
}

void test_current_time(Bmi* b)
{
    double t = -999.;
    b->update();
    b->get_current_time(&t);
    assert(t == static_cast<const BmiCppExtension*>(b)->get_current_time());
}

void test_time_step(Bmi* b)
{
    double t = -999.;
    b->get_time_step(&t);
    assert(t == static_cast<const BmiCppExtension*>(b)->get_time_step());
}

void test_time_units(Bmi* b)
{
    char unit[BMI_MAX_UNITS_NAME];
    b->get_time_units(unit);
    assert(std::string(unit, strlen(unit)) == static_cast<const BmiCppExtension*>(b)->get_time_units());
}

void test_get_values(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        if(static_cast<const BmiCppExtension*>(b)->get_var_type(*it) != "double")
        {
            continue;
        }
        int nbytes = 0;
        b->get_var_nbytes(it->c_str(), &nbytes);
        void* vals = (void*) malloc(nbytes);
        b->get_value(it->c_str(), vals);
        std::vector<double> vals_vec((double*)vals, (double*)vals + nbytes/sizeof(double));
        std::vector<double> vals_check = static_cast<const BmiCppExtension*>(b)->get_value<double>(*it);
        assert(vals_vec == vals_check);
        free(vals);
    }
}

void test_get_values_at_indices(Bmi* b)
{
    std::vector<int>indices = {1, 3, 5, 7};
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        if(static_cast<const BmiCppExtension*>(b)->get_var_type(*it) != "double")
        {
            continue;
        }
        int nbytes = 0;
        b->get_var_itemsize(it->c_str(), &nbytes);
        nbytes *= indices.size();
        void* vals = (void*) malloc(nbytes);
        b->get_value_at_indices(it->c_str(), vals, indices.data(), indices.size());
        std::vector<double> vals_vec((double*)vals, (double*)vals + nbytes/sizeof(double));
        assert(vals_vec == static_cast<const BmiCppExtension*>(b)->get_value_at_indices<double>(*it, indices));
        free(vals);
    }
}

void test_get_value_ptr(Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<const BmiCppExtension*>(b)->get_output_var_names();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        if(static_cast<const BmiCppExtension*>(b)->get_var_type(*it) != "double")
        {
            continue;
        }
        void* p;
        b->get_value_ptr(it->c_str(), &p);
        assert(p == static_cast<BmiCppExtension*>(b)->get_value_ptr<double>(*it));
    }
    
}

void test_finalize(Bmi* b)
{
    b->finalize();
    assert(true);
}

int main(int argc, char* argv[])
{
    std::vector<double> u = {0.1, 0.2, 0.4, 0.8};
    std::vector<double> v = {-0.6, -0.4, -0.2, 0.};
    Bmi* bmi = new BmiTestExtension(u, v);
    std::string testfunc(argv[1]);
    if(testfunc == "initialize")
    {
        test_initialize(bmi);
    }
    else if(testfunc == "component_name")
    {
        test_component_name(bmi);
    }
    else if(testfunc == "input_var_count")
    {
        test_input_var_count(bmi);
    }
    else if(testfunc == "input_vars")
    {
        test_input_vars(bmi);
    }
    else if(testfunc == "output_var_count")
    {
        test_output_var_count(bmi);
    }
    else if(testfunc == "output_vars")
    {
        test_output_vars(bmi);
    }
    else if(testfunc == "var_grid")
    {
        test_var_grid(bmi);
    }
    else if(testfunc == "var_type")
    {
        test_var_type(bmi);
    }
    else if(testfunc == "var_itemsize")
    {
        test_var_itemsize(bmi);
    }
    else if(testfunc == "var_nbytes")
    {
        test_var_nbytes(bmi);
    }
    else if(testfunc == "var_units")
    {
        test_var_units(bmi);
    }
    else if(testfunc == "start_time")
    {
        test_start_time(bmi);
    }
    else if(testfunc == "current_time")
    {
        test_current_time(bmi);
    }
    else if(testfunc == "end_time")
    {
        test_end_time(bmi);
    }
    else if(testfunc == "time_step")
    {
        test_time_step(bmi);
    }
    else if(testfunc == "time_units")
    {
        test_time_units(bmi);
    }
    else if(testfunc == "get_values")
    {
        test_get_values(bmi);
    }
    else if(testfunc == "get_values_at_indices")
    {
        test_get_values_at_indices(bmi);
    }
    else if(testfunc == "get_value_ptr")
    {
        test_get_value_ptr(bmi);
    }
    else if(testfunc == "finalize")
    {
        test_finalize(bmi);
    }
    else
    {
        throw std::invalid_argument("Unknown test function selection " + testfunc);
        return 1;
    }
    delete bmi;
    return 0;
}
