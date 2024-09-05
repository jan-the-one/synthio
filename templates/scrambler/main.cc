#include <iostream>  
#include <math.h>
#include <limits>
#include <iomanip>
#include <sys/resource.h>

#ifndef FACTORIAL
#define FACTORIAL
#endif

#ifndef FIBO
#define FIBO
#endif

#ifndef PI_GEN
#define PI_GEN
#endif

#ifndef DFT
#define DFT
#endif

using namespace std;

#if FACTORIAL == 1
int factorial(int n) {
   //base case
   if(n == 0) {
      return 1;
   } else {
      return n * factorial(n-1);
   }
}
#endif


#if PI_GEN == 1
//Taylor series calculation of Pi 
double pi(int n) {    

    double sum = 0.0;
    double tmp = 0.0;

    for (int i = 0; i < n; ++i) {           
        double num = pow(-1.0, (double)i);
        double den = ((2 * (double)i) + 1.0);
        tmp += num / den;
        sum = tmp * 4;
    }
    return sum;
}
#endif

#if FIBO == 1
int fibonacci(int n) {

#if FACTORIAL == 1
    if (n == 40){
    #IP_1
        for (int i = 0; i < 80000; i++)
            factorial(1000);
    }
#endif
   if(n == 0){
      return 0;
   } else if(n == 1) {
      return 1;
   } else {

    #if PI_GEN == 1
    return pi((fibonacci(n-1)) + (fibonacci(n-2))); //! Glue FIBO ^ PI_GEN
    #else
    return fibonacci(n-1)*10 + fibonacci(n-2)*10;
    #endif
   }
}
#endif


#if DFT == 1
void dft(int seq[], int len)
{
    int xn[len] = {1};
    float Xr[len];
    float Xi[len];
    int i, k, n = 0;
    
    #if FACTORIAL == 1
    int N = factorial(6) + factorial(6) + factorial(4); //! Glue DFT ^ FAC
    #else
    int N = 1000;
    #endif
    
    #if PI_GEN == 1
    double pie = pi(100);
    #endif
    for (k = 0; k < N / 500; k++) {
        Xr[k] = 0;
        Xi[k] = 0;
        for (n = 0; n < len; n++) {

            //TODO can add an "interaction" here where we use the PI-generator
            #if PI_GEN == 1
            Xr[k] = (Xr[k] + xn[n] * cos(2 * pie * k * n / N)); //! GLUE DFT ^ PI_GEN
            Xi[k] = (Xi[k] - xn[n] * sin(2 * pie * k * n / N));
            #else 
            Xr[k] = (Xr[k] + xn[n] * cos(2 * 3.14 * k * n / N));
            Xi[k] = (Xi[k] - xn[n] * sin(2 * 3.14 * k * n / N));
            #endif
        }
        // printf("(%f) + j(%f)\n", Xr[k], Xi[k]);
    }
}
#endif

// Driver Code
int main()
{
    #if DFT == 1
        int sequence[] = {10, 22, 350, 461, 609, 1003, 1204, 1799, 3500, 10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100, 1003, 1204, 1799, 3500, 10, 1003, 1204, 1799, 3500, 10, 1003, 1204, 1799, 3500, 10, 1003, 1204, 1799, 3500, 10};
        int len = sizeof(sequence) / sizeof(sequence[0]);
        #IP_1
        for (int i = 0; i < 80000; i++){
            dft(sequence, len / 2);
        }
        #IP_2
        #IP_3

        #if PI_GEN == 1
            #IP_4
        #endif
    #elif FIBO == 1
        fibonacci(40);
    #elif FACTORIAL == 1
        #IP_1
        for (int i = 0; i < 80000; i++)
            factorial(1000);
        #IP_2
    #endif

    return 0;
}
