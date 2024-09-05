#include "test_gadget.h"
#include <iostream>

#ifndef FEATURE_A
#define FEATURE_A 1
#endif

#ifndef FEATURE_B
#define FEATURE_B 1
#endif

#define STR(x)   #x
#define SHOW_DEFINE(x) std::cout << ("%s=%s\n", #x, STR(x))

int NS_NAME::render()
{
#if FEATURE_A == 1 && FEATURE_B == 1
    return 1+1;
#elif FEATURE_B == 1
    NS_NAME::someVar = 7777;

    SHOW_DEFINE(RANDOM_KNOB);
    return 2*2;
#else
    NS_NAME::someVar = 5555;
    std::cout << "GADGET AT WORK:  " << NS_NAME::someVar << std::endl;
    return 6;
#endif

}