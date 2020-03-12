#include <assert.h>
#include <stdexcept>
#include <cstring>
#include "bmi_cpp_extension.h"
#include "test/bmi_test_extension.h"

void test_initialize(bmi::Bmi* b)
{
    const char* s = "somestring";
    b->Initialize(s);
    assert(true);
}

void test_component_name(bmi::Bmi* b)
{
    std::string check_string = b->GetComponentName();
    std::string component_name_string = static_cast<BmiCppExtension*>(b)->GetComponentName();
    assert(check_string == component_name_string);
}

void test_input_item_count(bmi::Bmi* b)
{
    int count = b->GetInputItemCount();
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    assert(input_vars.size() == count);
}

void test_input_vars(bmi::Bmi* b)
{
    std::vector<std::string> names = b->GetInputVarNames();
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < input_vars.size(); i++)
    {
        assert(input_vars[i] == names[i]);
    }
}

void test_output_item_count(bmi::Bmi* b)
{
    int count = b->GetOutputItemCount();
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    assert(output_vars.size() == count);
}

void test_output_vars(bmi::Bmi* b)
{
    std::vector<std::string> names = b->GetOutputVarNames();
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < output_vars.size(); i++)
    {
        assert(output_vars[i] == names[i]);
    }
}

void test_var_grid(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        int id = b->GetVarGrid(it->c_str());
        assert(static_cast<BmiCppExtension*>(b)->GetVarGrid(*it) == id);
    }
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        int id = b->GetVarGrid(it->c_str());
        assert(static_cast<BmiCppExtension*>(b)->GetVarGrid(*it) == id);
    }
}

void test_var_type(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        std::string type = b->GetVarType(it->c_str());
        assert(static_cast<BmiCppExtension*>(b)->GetVarType(*it) == type);
    }
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        std::string type = b->GetVarType(it->c_str());
        assert(static_cast<BmiCppExtension*>(b)->GetVarType(*it) == type);
    }
}

void test_var_itemsize(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        int size = b->GetVarItemsize(it->c_str());
        assert(static_cast<BmiCppExtension*>(b)->GetVarItemsize(*it) == size);
    }
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        int size = b->GetVarItemsize(it->c_str());
        assert(static_cast<BmiCppExtension*>(b)->GetVarItemsize(*it) == size);
    }
}

void test_var_nbytes(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        int size = b->GetVarNbytes(*it);
        assert(static_cast<BmiCppExtension*>(b)->GetVarNbytes(*it) == size);
    }
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        int size = b->GetVarNbytes(*it);
        assert(static_cast<BmiCppExtension*>(b)->GetVarNbytes(*it) == size);
    }
}

void test_var_units(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        std::string units = b->GetVarUnits(*it);
        assert(static_cast<BmiCppExtension*>(b)->GetVarUnits(*it) == units);
    }
    std::vector<std::string> input_vars = static_cast<BmiCppExtension*>(b)->GetInputVarNames();
    for(std::vector<std::string>::const_iterator it = input_vars.begin(); it != input_vars.end(); ++it)
    {
        std::string units = b->GetVarUnits(*it);
        assert(static_cast<BmiCppExtension*>(b)->GetVarUnits(*it) == units);
    }
}

void test_start_time(bmi::Bmi* b)
{
    double t = b->GetStartTime();
    assert(t == static_cast<BmiCppExtension*>(b)->GetStartTime());
}

void test_end_time(bmi::Bmi* b)
{
    double t = b->GetEndTime();
    assert(t == static_cast<BmiCppExtension*>(b)->GetEndTime());
}

void test_current_time(bmi::Bmi* b)
{
    double t = -999.;
    b->Update();
    t = b->GetCurrentTime();
    assert(t == static_cast<BmiCppExtension*>(b)->GetCurrentTime());
}

void test_time_step(bmi::Bmi* b)
{
    double t = b->GetTimeStep();
    assert(t == static_cast<BmiCppExtension*>(b)->GetTimeStep());
}

void test_time_units(bmi::Bmi* b)
{
    std::string unit = b->GetTimeUnits();
    assert(unit == static_cast<BmiCppExtension*>(b)->GetTimeUnits());
}

void test_get_values(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        if(static_cast<BmiCppExtension*>(b)->GetVarType(*it) != "double")
        {
            continue;
        }
        int nbytes = b->GetVarNbytes(*it);
        void* vals = (void*) malloc(nbytes);
        b->GetValue(*it, vals);
        std::vector<double> vals_vec((double*)vals, (double*)vals + nbytes/sizeof(double));
        std::vector<double> vals_check = static_cast<BmiCppExtension*>(b)->GetValue<double>(*it);
        assert(vals_vec == vals_check);
        free(vals);
    }
}

void test_get_values_at_indices(bmi::Bmi* b)
{
    std::vector<int>indices = {1, 3, 5, 7};
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        if(static_cast<BmiCppExtension*>(b)->GetVarType(*it) != "double")
        {
            continue;
        }
        int nbytes = b->GetVarItemsize(*it);
        nbytes *= indices.size();
        void* vals = (void*) malloc(nbytes);
        b->GetValueAtIndices(*it, vals, indices.data(), indices.size());
        std::vector<double> vals_vec((double*)vals, (double*)vals + nbytes/sizeof(double));
        assert(vals_vec == static_cast<BmiCppExtension*>(b)->GetValueAtIndices<double>(*it, indices));
        free(vals);
    }
}

void test_get_value_ptr(bmi::Bmi* b)
{
    std::vector<std::string> output_vars = static_cast<BmiCppExtension*>(b)->GetOutputVarNames();
    for(std::vector<std::string>::const_iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        if(static_cast<BmiCppExtension*>(b)->GetVarType(*it) != "double")
        {
            continue;
        }
        void* p = b->GetValuePtr(*it);
        assert(p == static_cast<BmiCppExtension*>(b)->GetValuePtr<double>(*it));
    }
    
}

void test_finalize(bmi::Bmi* b)
{
    b->Finalize();
    assert(true);
}

int main(int argc, char* argv[])
{
    std::vector<double> u = {0.1, 0.2, 0.4, 0.8};
    std::vector<double> v = {-0.6, -0.4, -0.2, 0.};
    bmi::Bmi* bmi = new BmiTestExtension(u, v);
    std::string testfunc(argv[1]);
    if(testfunc == "initialize")
    {
        test_initialize(bmi);
    }
    else if(testfunc == "component_name")
    {
        test_component_name(bmi);
    }
    else if(testfunc == "input_item_count")
    {
        test_input_item_count(bmi);
    }
    else if(testfunc == "input_vars")
    {
        test_input_vars(bmi);
    }
    else if(testfunc == "output_item_count")
    {
        test_output_item_count(bmi);
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
