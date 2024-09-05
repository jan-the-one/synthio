#include "cache_gadget.h"
#include <stdio.h>
#include <x86intrin.h>
#include <unistd.h>
#include <stdint.h>
#include <iostream>
#include <cstring>
#include <sys/resource.h>

/*
Parts of this implementation were based on https://stackoverflow.com/questions/73281197/program-with-intentionally-high-l1-cache-miss-rate
And verified/explained based on https://people.freebsd.org/~lstewart/articles/cpumemory.pdf
*/


//! Business Logic
#if READS_WORKLOAD != WRITES_WORKLOAD
//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

//>>>>>>>> CONFIGS
#if REDUCE_CACHEING == 0

 #if READS_WORKLOAD == 1 && WRITES_WORKLOAD == 0
    #undef OPERATIONS
    #define OPERATIONS (1000000 * OPS_SCALER)
 #endif
 
 #if WRECK_L3 == 1
    #undef MEM_ALLOC
    #define MEM_ALLOC (L3_CACHE_SIZE * 2 * ALLOC_SCALER)

    #if READS_WORKLOAD == 1 //! needed because the mem_alloc is quite large already and we have higher latency overall
     #undef OPERATIONS
     #define OPERATIONS (500000 * OPS_SCALER)
    #endif
 #elif WRECK_L2 == 1
    #undef MEM_ALLOC
    #define MEM_ALLOC (L2_CACHE_SIZE * ALLOC_SCALER)
 #else
    #undef MEM_ALLOC
    #define MEM_ALLOC (L1_CACHE_SIZE * ALLOC_SCALER)
 #endif

#else
 //TODO perhaps operations also need the default value
 #if READS_WORKLOAD == 1 && WRITES_WORKLOAD == 0
    #undef OPERATIONS
    #define OPERATIONS (1000 * OPS_SCALER)
 #else
    #undef OPERATIONS
    #define OPERATIONS (1000 * OPS_SCALER)
 #endif

#endif

//>>>>>>>> ACTUAL IMPLEMENTATION

#if READS_WORKLOAD == 1 && WRITES_WORKLOAD == 0

#if REDUCE_CACHEING == 0
  static char array[MEM_ALLOC] = {1};
#endif

inline __attribute__((always_inline)) void NS_NAME::read_workload(){
//######################## NORMAL WRECK #############################
#if REDUCE_CACHEING == 0

    volatile register char* arr asm ("r12") = array;
    volatile register unsigned long idx asm("r13") = 0;
    volatile register unsigned long dummy_sum asm("r14") = 0;
    volatile register unsigned long cnt asm ("r15") = 0;
    register size_t strd asm ("r10") = WORKING_SET_SCALER * KiB;

    #if (WRECK_L2 == 1 || WRECK_L3 == 1) && IMPROVE_L1_RATE == 1
    volatile unsigned long extra_dummy_sum = 0;
    volatile unsigned long s_cnt = 0;
    #endif

    while(++cnt < OPERATIONS)
    {
        idx += strd;
        idx %= MEM_ALLOC;
        dummy_sum = arr[idx];

    #if (WRECK_L2 == 1 || WRECK_L3 == 1) && IMPROVE_L1_RATE == 1
        while(s_cnt++ < OPERATIONS){
            extra_dummy_sum += dummy_sum + 1;
        }
        extra_dummy_sum = 0;
    #endif
        
    }
//####################### REDUCE_CACHEING ###############################
#else
    char buff[CACHE_LINE * ALLOC_SCALER] = {1}; 

    volatile char *tmp;
    volatile register unsigned long cnt = 0; 
    volatile register u_int64_t i;
    register unsigned int dummy = 0;
    
     while(++cnt < OPERATIONS)
    {
        for (i = 0; i < CACHE_LINE; ++i) {
        _mm_clflush(buff);
        tmp = &buff[i];        
        dummy = *tmp;
        }    
    }

#endif
}

#elif READS_WORKLOAD == 0 && WRITES_WORKLOAD == 1

void NS_NAME::write_workload(){

#if REDUCE_CACHEING == 0

    register size_t *buffer asm("r15") = (size_t *) malloc(MEM_ALLOC);
    if (buffer==NULL) std::cout <<"[CACHE GADGET EXCEPTION #4]" << std::endl;

    volatile register size_t limit asm("r13") = MEM_ALLOC / TYPE_SIZE - 1;

    register size_t inc asm("r14") = (KiB * WORKING_SET_SCALER) / TYPE_SIZE;
    volatile register size_t offset asm("r12") = 0;

    int ops = OPERATIONS;
    while(ops-- != 0){
#if BIG_WRITES == 1
        memset(buffer + offset, 0x0f, KiB * WORKING_SET_SCALER);
#else 
        memset(buffer + offset, 0x0f, TYPE_SIZE);
#endif
        offset += inc;
        if (offset > limit){
            offset = 0;
        }
    }
    free(buffer);

//####################### REDUCE_CACHEING ###############################
#else

    static long long int *buffer  = nullptr;
    register int szt = sizeof(long long int);

    posix_memalign((void **) &buffer, szt * 8, CACHE_LINE);

    register long long int writable asm("r14") = 0x1f;
    register long long int dummy asm("r15") = 0x2f;

    int ops = OPERATIONS;
    while(ops-- != 0){
        for(int i = 0; i < (CACHE_LINE / szt); i += 1) {
            _mm_stream_si64(&buffer[i], writable); 
            buffer[i] = dummy;
        }
    }

    free(buffer);
#endif
}
#endif

//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#endif

//! Entry Point
void NS_NAME::render()
{
#if READS_WORKLOAD == 1 && WRITES_WORKLOAD == 0
    NS_NAME::read_workload();
#elif READS_WORKLOAD == 0 && WRITES_WORKLOAD == 1
    NS_NAME::write_workload();
#elif
    std::cout << "[CACHE GADGET] BAD WORKLOAD CONFIG!" << std::endl;
#endif

}
