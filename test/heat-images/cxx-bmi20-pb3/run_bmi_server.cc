#include "bmi_grpc_server.h"
#include <bmi.h>
#include "bmi_heat.h"

int main(int argc, char* argv[])
{
    Bmi *model = (Bmi *) malloc(sizeof(Bmi));
    register_bmi_heat(model);
    run_bmi_server(model, argc, argv);
    return 0;
}