#include "cpptest.h"
#include "bmi-c/heat/bmi_heat.h"
#include "bmi_cpp_extension.h"


class BmiCppExtensionTests: public Test::Suite
{
    public:

        BmiCppExtensionTests()
        {
            TEST_ADD(BmiCppExtensionTests::test_constructor);
        }

    private:
        void test_constructor() const
        {
            return;
        }
};
