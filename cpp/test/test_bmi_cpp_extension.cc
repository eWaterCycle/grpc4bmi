#include <assert.h>
#include "bmi-c/heat/bmi_heat.h"
#include "bmi_cpp_extension.h"
#include "test/bmi_test_extension.h"

BmiCppExtension* create_bmi()
{
    std::vector<double> u = {0.1, 0.2, 0.4, 0.8};
    std::vector<double> v = {-0.6, -0.4, -0.2, 0.};
    return new BmiTestExtension(u, v);
}

void test_constructor()
{
    Bmi* b = create_bmi();
    assert(b != NULL);
}

int main(int argc, char* argv[])
{
    test_constructor();
}
