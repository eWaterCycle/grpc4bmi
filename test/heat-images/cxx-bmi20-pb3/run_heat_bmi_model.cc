#include "bmi_grpc_server.h"
#include "bmi_heat.hxx"

int main(int argc, char* argv[])
{
    Bmi* model = new BmiHeat();
    run_bmi_server(model, argc, argv);
    delete model;
    return 0;
}