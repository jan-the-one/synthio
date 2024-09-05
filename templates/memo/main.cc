#include <iostream>  
#include <math.h>
#include <limits>
#include <iomanip>
#include <sys/resource.h>
#include <climits>
#include <vector>
#include <fstream>
#include <filesystem>

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

int maxSubArraySum(int arr[], int n)
{
    if (n == 1) {
        return arr[0];
    }

    int m = n / 2;

    int left_max = maxSubArraySum(arr, m);

    int right_max = maxSubArraySum(arr + m, n - m);

    int left_sum = INT_MIN, right_sum = INT_MIN, sum = 0;
    for (int i = m; i < n; i++) {
        sum += arr[i];
        right_sum = max(right_sum, sum);
    }
    sum = 0;
    for (int i = m - 1; i >= 0; i--) {
        sum += arr[i];
        left_sum = max(left_sum, sum);
    }
    int cross_max = left_sum + right_sum;

    return max(cross_max, max(left_max, right_max));
}

bool isSubsetSum(int set[], int n, int sum){
    if (sum == 0)
        return true;
    if (n == 0)
        return false;
 
    if (set[n - 1] > sum)
        return isSubsetSum(set, n - 1, sum);
 
    return isSubsetSum(set, n - 1, sum) || isSubsetSum(set, n - 1, sum - set[n - 1]);
}
 
void memy(int n){
#define SIZE 100
unsigned int is[SIZE] = {1};
unsigned int sum = 0;
size_t i = 0, j = 0;
for (i = 0; i < n; i++)
{
    for (j = 0; j < SIZE; j++)
        sum = is[j];
    }
}

void memy_allocy(int n){
    char *p;
    int i,j;
    int size = 100;

    for (i=0; i < n; i++){

        p = (char *) malloc(size);

        for (j=0; j < size; j++){
        
            p[j] = 1;
        }
    }
}

void cachy(int n){

    int numrows = 4 * 1024;
    int *data;

    int i, j, k;
    int cs = 64;
    const rlim_t kStackSize = cs * 1024;
    struct rlimit rl;
    int result;

    result = getrlimit(RLIMIT_STACK, &rl);

    data = (int *) malloc(cs * numrows * sizeof(int));

    for (k=0; k < n; k++){
        for (i=0; i < numrows; i++){

            for (j=0; j < cs; j++){
                    data[j + cs * i] = 99;
                }
            }
        }
    
    // for (k=0; k < n; k++){
    //     for (i=0; i < numrows; i++){

    //         for (j=0; j < cs; j++){
    //             data[i * cs + j] = 99;
    //         }
    //     }
    // }
}


void fily(int n){

    for (int k=0; k < n; k++){
     
        std::FILE* tmpf = std::tmpfile();
        std::fputs("Hello, world", tmpf);
        std::rewind(tmpf);
        int fd;
    }
}

/**
In this template we don't provide any intentional "glue" code. Feature interactions can be simulated
by injecting an IP under the correct preprocessor-nest.
*/
int main()
{
        #if COMPUTE == 1
        int set[] = {10, 22, 350, 461, 609, 1003, 1204, 1799, 3500, -10, -22, -35, -40, 45, 50, 80, 82};
        int n = sizeof(set) / sizeof(set[0]);    
        int sum = 512512525;
        #endif

        int ks = 10000;
        #if MEM_USAGE == 1
            memy(ks);
            memy_allocy(ks);
            // cachy(ks);

            #if FS_USAGE == 1 && COMPUTE == 1
                fily(ks);
                for (int i = 0; i < 500; i++){
                    isSubsetSum(set, n, sum);
                    maxSubArraySum(set, n);
                }
            #elif FS_USAGE == 1
                fily(ks);
            #elif COMPUTE == 1
                for (int i = 0; i < 1000; i++){
                    isSubsetSum(set, n, sum);
                    maxSubArraySum(set, n);
                }
            #endif

        #else
            fily(ks);
            isSubsetSum(set, n, sum);
            maxSubArraySum(set, n);
        #endif
    
    return 0;
}
