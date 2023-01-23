#include "bmi_grpc_server.h"
#include <bmi.hxx>
#include "bmi_heat.hxx"

int main(int argc, char* argv[])
{
    bmi::Bmi* model = new BmiHeat();
    run_bmi_server(model, argc, argv);
    return 0;
}