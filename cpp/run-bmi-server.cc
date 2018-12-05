#include <string>
#include <iostream>

#include "bmi-c/heat/bmi_heat.h"
#include "bmi-c/bmi/bmilib.h"
#include "bmi_grpc_server.h"

int main(int argc, char* argv[])
{
    BMI_Model* model = (BMI_Model*)malloc (sizeof(BMI_Model));
    register_bmi_heat(model);
    BMI_Initialize(model, NULL);
    run_bmi_server(model, argc, argv);
    delete model;
    return 0;
}

