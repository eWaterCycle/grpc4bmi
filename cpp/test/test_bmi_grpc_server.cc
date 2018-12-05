#include <assert.h>
#include <stdexcept>
#include <cstring>
#include "bmi_cpp_extension.h"
#include "test/bmi_test_extension.h"
#include "bmi_grpc_server.h"

#define SELECT_NONE 0
#define SELECT_OUTPUT 1
#define SELECT_INPUT 2
#define SELECT_ALL 3

std::vector<std::string> get_bmi_varnames(Bmi* b, int selector=SELECT_ALL)
{
    int count = 0;
    int input_count = 0;
    int output_count = 0;
    if((selector & SELECT_INPUT) > 0)
    {
        b->get_input_var_name_count(&input_count);
        count += input_count;
    }
    if((selector & SELECT_OUTPUT) > 0)
    {
        b->get_output_var_name_count(&output_count);
        count += output_count;
    }
    if(count == 0)
    {
        return std::vector<std::string>();
    }
    char** names = (char**) malloc(sizeof(char*)*count);
    for(int i = 0; i < count; i++)
    {
        names[i] = (char*) malloc(sizeof(char)*BMI_MAX_VAR_NAME);
    }
    if(selector & SELECT_INPUT > 0)
    {
        b->get_input_var_names(names);
    }
    if(selector & SELECT_OUTPUT > 0)
    {
        b->get_output_var_names(names + input_count);
    }
    std::vector<std::string> result(count);
    for(std::vector<std::string>::size_type i = 0; i < result.size(); ++i)
    {
        result[i] = std::string(names[i]);
        free(names[i]);
    }
    free(names);
    return result;
}

void test_initialize(BmiGRPCService* s, Bmi* b)
{
    const char* inifile = "somestring";
    bmi::InitializeRequest* request = new bmi::InitializeRequest();
    bmi::Empty* response = new bmi::Empty();
    request->set_config_file(std::string(inifile));
    s->initialize(NULL, request, response);
    b->initialize(inifile);
    assert(true);
    delete request;
    delete response;
}

void test_component_name(BmiGRPCService* s, Bmi* b)
{
    char component_name_char[BMI_MAX_COMPONENT_NAME];
    b->get_component_name(component_name_char);
    std::string check_string(component_name_char, strlen(component_name_char));
    bmi::Empty* request = new bmi::Empty();
    bmi::GetComponentNameResponse* response = new bmi::GetComponentNameResponse();
    s->getComponentName(NULL, request, response);
    assert(response->name() == check_string);
    delete request;
    delete response;
}

void test_input_var_count(BmiGRPCService* s, Bmi* b)
{
    int count = 0;
    b->get_input_var_name_count(&count);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetVarNamesResponse* response = new bmi::GetVarNamesResponse();
    s->getInputVarNames(NULL, request, response);
    assert(response->names().size() == count);
    delete request;
    delete response;
}

void test_input_vars(BmiGRPCService* s, Bmi* b)
{
    int count = 0;
    b->get_input_var_name_count(&count);
    char** names = (char**) malloc(sizeof(char*)*count);
    for(int i = 0; i < count; i++)
    {
        names[i] = (char*) malloc(sizeof(char)*BMI_MAX_VAR_NAME);
    }
    b->get_input_var_names(names);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetVarNamesResponse* response = new bmi::GetVarNamesResponse();
    s->getInputVarNames(NULL, request, response);
    for(int i = 0; i < count; i++)
    {
        assert(std::string(names[i]) == response->names()[i]);
    }
    for(int i = 0; i < count; i++)
    {
        free(names[i]);
    }
    free(names);
    delete request;
    delete response;
}

void test_output_var_count(BmiGRPCService* s, Bmi* b)
{
    int count = 0;
    b->get_output_var_name_count(&count);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetVarNamesResponse* response = new bmi::GetVarNamesResponse();
    s->getOutputVarNames(NULL, request, response);
    assert(response->names().size() == count);
    delete request;
    delete response;
}

void test_output_vars(BmiGRPCService* s, Bmi* b)
{
    int count = 0;
    b->get_output_var_name_count(&count);
    char** names = (char**) malloc(sizeof(char*)*count);
    for(int i = 0; i < count; i++)
    {
        names[i] = (char*) malloc(sizeof(char)*BMI_MAX_VAR_NAME);
    }
    b->get_output_var_names(names);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetVarNamesResponse* response = new bmi::GetVarNamesResponse();
    s->getOutputVarNames(NULL, request, response);
    for(int i = 0; i < count; i++)
    {
        assert(std::string(names[i]) == response->names()[i]);
    }
    for(int i = 0; i < count; i++)
    {
        free(names[i]);
    }
    free(names);
    delete request;
    delete response;
}


void test_var_grid(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> names = get_bmi_varnames(b);
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::GetVarGridResponse* response = new bmi::GetVarGridResponse();
    for(std::vector<std::string>::size_type i = 0; i < names.size(); ++i)
    {
        int id = -999;
        b->get_var_grid(names[i].c_str(), &id);
        request->set_name(names[i]);
        s->getVarGrid(NULL, request, response);
        assert(id == response->grid_id());
    }
    delete request;
    delete response;
}

void test_var_type(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> names = get_bmi_varnames(b);
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::GetVarTypeResponse* response = new bmi::GetVarTypeResponse();
    for(std::vector<std::string>::size_type i = 0; i < names.size(); ++i)
    {
        char type[BMI_MAX_TYPE_NAME];
        b->get_var_type(names[i].c_str(), type);
        request->set_name(names[i]);
        s->getVarType(NULL, request, response);
        assert(std::string(type) == response->type());
    }
    delete request;
    delete response;
}

void test_var_itemsize(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> names = get_bmi_varnames(b);
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::GetVarItemSizeResponse* response = new bmi::GetVarItemSizeResponse();
    for(std::vector<std::string>::size_type i = 0; i < names.size(); ++i)
    {
        int itemsize = -999;
        b->get_var_itemsize(names[i].c_str(), &itemsize);
        request->set_name(names[i]);
        s->getVarItemSize(NULL, request, response);
        assert(itemsize == response->size());
    }
    delete request;
    delete response;
}

void test_var_nbytes(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> names = get_bmi_varnames(b);
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::GetVarNBytesResponse* response = new bmi::GetVarNBytesResponse();
    for(std::vector<std::string>::size_type i = 0; i < names.size(); ++i)
    {
        int nbytes = -999;
        b->get_var_nbytes(names[i].c_str(), &nbytes);
        request->set_name(names[i]);
        s->getVarNBytes(NULL, request, response);
        assert(nbytes == response->nbytes());
    }
    delete request;
    delete response;
}

void test_var_units(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> names = get_bmi_varnames(b);
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::GetVarUnitsResponse* response = new bmi::GetVarUnitsResponse();
    for(std::vector<std::string>::size_type i = 0; i < names.size(); ++i)
    {
        char type[BMI_MAX_UNITS_NAME];
        b->get_var_units(names[i].c_str(), type);
        request->set_name(names[i]);
        s->getVarUnits(NULL, request, response);
        assert(std::string(type) == response->units());
    }
    delete request;
    delete response;
}

void test_start_time(BmiGRPCService* s, Bmi* b)
{
    double t = -999.;
    b->get_start_time(&t);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetTimeResponse* response = new bmi::GetTimeResponse();
    s->getStartTime(NULL, request, response);
    assert(response->time() == t);
    delete request;
    delete response;
}

void test_current_time(BmiGRPCService* s, Bmi* b)
{
    double t = -999.;
    b->get_current_time(&t);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetTimeResponse* response = new bmi::GetTimeResponse();
    s->getCurrentTime(NULL, request, response);
    assert(response->time() == t);
    delete request;
    delete response;
}

void test_end_time(BmiGRPCService* s, Bmi* b)
{
    double t = -999.;
    b->get_end_time(&t);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetTimeResponse* response = new bmi::GetTimeResponse();
    s->getEndTime(NULL, request, response);
    assert(response->time() == t);
    delete request;
    delete response;
}

void test_time_step(BmiGRPCService* s, Bmi* b)
{
    double dt = -999.;
    b->get_time_step(&dt);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetTimeStepResponse* response = new bmi::GetTimeStepResponse();
    s->getTimeStep(NULL, request, response);
    assert(response->interval() == dt);
    delete request;
    delete response;
}

void test_time_units(BmiGRPCService* s, Bmi* b)
{
    char unit[BMI_MAX_UNITS_NAME];
    b->get_time_units(unit);
    bmi::Empty* request = new bmi::Empty();
    bmi::GetTimeUnitsResponse* response = new bmi::GetTimeUnitsResponse();
    s->getTimeUnits(NULL, request, response);
    assert(response->units() == std::string(unit));
    delete request;
    delete response;
}

void test_get_values(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> output_vars = get_bmi_varnames(b, SELECT_OUTPUT);
    char type[BMI_MAX_TYPE_NAME];
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::GetValueResponse* response = new bmi::GetValueResponse();
    for(std::vector<std::string>::iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        b->get_var_type(it->c_str(), type);
        if(std::string(type) != "double")
        {
            continue;
        }
        int nbytes = 0;
        b->get_var_nbytes(it->c_str(), &nbytes);
        void* vals = malloc(nbytes);
        b->get_value(it->c_str(), vals);
        request->set_name(*it);
        s->getValue(NULL, request, response);
        for(int i = 0; i < response->mutable_values_double()->values_size(); ++i)
        {
            assert(response->mutable_values_double()->values(i) == *(static_cast<double*>(vals) + i));
        }
        free(vals);
    }
    delete request;
    delete response;
}

void test_get_values_at_indices(BmiGRPCService* s, Bmi* b)
{
    std::vector<int>indices = {1, 3, 5, 7};
    std::vector<std::string> output_vars = get_bmi_varnames(b, SELECT_OUTPUT);
    char type[BMI_MAX_TYPE_NAME];
    bmi::GetValueAtIndicesRequest* request = new bmi::GetValueAtIndicesRequest();
    bmi::GetValueAtIndicesResponse* response = new bmi::GetValueAtIndicesResponse();
    for(std::vector<std::string>::iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        b->get_var_type(it->c_str(), type);
        if(std::string(type) != "double")
        {
            continue;
        }
        void* vals = malloc(indices.size() * sizeof(double));
        b->get_value_at_indices(it->c_str(), vals, indices.data(), indices.size());
        request->set_name(*it);
        for(std::vector<int>::const_iterator it = indices.begin(); it != indices.end(); ++it)
        {
            request->add_indices(*it);
        }
        s->getValueAtIndices(NULL, request, response);
        for(int i = 0; i < response->mutable_values_double()->values_size(); ++i)
        {
            assert(response->mutable_values_double()->values(i) == *(static_cast<double*>(vals) + i));
        }
        free(vals);
    }
    delete request;
    delete response;
}

void test_get_value_ptr(BmiGRPCService* s, Bmi* b)
{
    std::vector<std::string> output_vars = get_bmi_varnames(b, SELECT_OUTPUT);
    bmi::GetVarRequest* request = new bmi::GetVarRequest();
    bmi::Empty* response = new bmi::Empty();
    for(std::vector<std::string>::iterator it = output_vars.begin(); it != output_vars.end(); ++it)
    {
        request->set_name(*it);
        assert(s->getValuePtr(NULL, request, response).error_code() == ::grpc::StatusCode::UNIMPLEMENTED);
    }
    delete request;
    delete response;
}

void test_finalize(BmiGRPCService* s)
{
    bmi::Empty* request = new bmi::Empty();
    bmi::Empty* response = new bmi::Empty();
    assert(s->finalize(NULL, request, response).error_code() == ::grpc::StatusCode::OK);
    delete request;
    delete response;
}

int main(int argc, char* argv[])
{
    std::vector<double> u = {0.1, 0.2, 0.4, 0.8};
    std::vector<double> v = {-0.6, -0.4, -0.2, 0.};
    Bmi* bmi = new BmiTestExtension(u, v);
    BmiGRPCService* bmi_service = new BmiGRPCService(bmi);
    Bmi* bmi_copy = new BmiTestExtension(u, v);
    std::string testfunc(argv[1]);
    if(testfunc == "initialize")
    {
        test_initialize(bmi_service, bmi);
    }
    else if(testfunc == "component_name")
    {
        test_component_name(bmi_service, bmi);
    }
    else if(testfunc == "input_var_count")
    {
        test_input_var_count(bmi_service, bmi);
    }
    else if(testfunc == "input_vars")
    {
        test_input_vars(bmi_service, bmi);
    }
    else if(testfunc == "output_var_count")
    {
        test_output_var_count(bmi_service, bmi);
    }
    else if(testfunc == "output_vars")
    {
        test_output_vars(bmi_service, bmi);
    }
    else if(testfunc == "var_grid")
    {
        test_var_grid(bmi_service, bmi);
    }
    else if(testfunc == "var_type")
    {
        test_var_type(bmi_service, bmi);
    }
    else if(testfunc == "var_itemsize")
    {
        test_var_itemsize(bmi_service, bmi);
    }
    else if(testfunc == "var_nbytes")
    {
        test_var_nbytes(bmi_service, bmi);
    }
    else if(testfunc == "var_units")
    {
        test_var_units(bmi_service, bmi);
    }
    else if(testfunc == "start_time")
    {
        test_start_time(bmi_service, bmi);
    }
    else if(testfunc == "current_time")
    {
        test_current_time(bmi_service, bmi);
    }
    else if(testfunc == "end_time")
    {
        test_end_time(bmi_service, bmi);
    }
    else if(testfunc == "time_step")
    {
        test_time_step(bmi_service, bmi);
    }
    else if(testfunc == "time_units")
    {
        test_time_units(bmi_service, bmi);
    }
    else if(testfunc == "get_values")
    {
        test_get_values(bmi_service, bmi);
    }
    else if(testfunc == "get_values_at_indices")
    {
        test_get_values_at_indices(bmi_service, bmi);
    }
    else if(testfunc == "get_value_ptr")
    {
        test_get_value_ptr(bmi_service, bmi);
    }
    else if(testfunc == "finalize")
    {
        test_finalize(bmi_service);
    }
    else
    {
        throw std::invalid_argument("Unknown test function selection " + testfunc);
        return 1;
    }
    delete bmi_service;
    delete bmi_copy;
    delete bmi;
    return 0;
}
