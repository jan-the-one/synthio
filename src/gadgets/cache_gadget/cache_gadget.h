#include <stddef.h>
#include <stdint.h>
#ifndef NS_NAME
#define NS_NAME cache_gadget_default
#endif

//! Feature Flags
#ifndef READS_WORKLOAD
#define READS_WORKLOAD 0
#endif

#ifndef WRITES_WORKLOAD
#define WRITES_WORKLOAD 0
#endif

#ifndef REDUCE_CACHEING
#define REDUCE_CACHEING 0
#endif

// #ifndef WRECK_L1
// #define WRECK_L1 0
// #endif

#ifndef WRECK_L2
#define WRECK_L2 0
#endif

#ifndef WRECK_L3
#define WRECK_L3 0
#endif

#ifndef IMPROVE_L1_RATE
#define IMPROVE_L1_RATE 0
#endif

#ifndef IMPROVE_L1_RATE
#define IMPROVE_L1_RATE 0
#endif

#ifndef BIG_WRITES
#define BIG_WRITES 0
#endif

//! Knobs 
#ifndef ALLOC_SCALER
    #define ALLOC_SCALER 2
#elif ALLOC_SCALER > 8
    #undef ALLOC_SCALER
    #define ALLOC_SCALER 8
#elif ALLOC_SCALER < 0
    #undef ALLOC_SCALER
    #define ALLOC_SCALER 2
#endif

#ifndef OPS_SCALER
    #define OPS_SCALER 1
#elif OPS_SCALER > 1000
    #undef OPS_SCALER
    #define OPS_SCALER 1000
#elif OPS_SCALER < 1
    #undef OPS_SCALER
    #define OPS_SCALER 1
#endif

#if !defined(WORKING_SET_SCALER)
#define WORKING_SET_SCALER 4
#elif WORKING_SET_SCALER > 16
    #undef WORKING_SET_SCALER
    #define WORKING_SET_SCALER 16
#elif WORKING_SET_SCALER < 1
    #undef WORKING_SET_SCALER
    #define WORKING_SET_SCALER 1
#endif

//! General Configs
#define KiB 1024
#define MiB 1024*KiB
#define GiB 1024L*MiB

#ifndef CACHE_LINE
#define CACHE_LINE 64
#endif

#ifndef L1_CACHE_SIZE 
#define L1_CACHE_SIZE (32 * KiB)
#endif

#ifndef L2_CACHE_SIZE 
#define L2_CACHE_SIZE (256 * KiB)
#endif

#ifndef L3_CACHE_SIZE
#define L3_CACHE_SIZE (4 * MiB)
#endif

#ifndef PAGE
#define PAGE (4 * KiB)
#endif

#ifndef TYPE_SIZE
#define TYPE_SIZE sizeof(size_t)
#endif

#ifndef OPERATIONS
#define OPERATIONS (100000 * OPS_SCALER)
#endif

#ifndef MEM_ALLOC
#define MEM_ALLOC (L1_CACHE_SIZE * ALLOC_SCALER)
#endif

namespace NS_NAME
{

// #if READS_WORKLOAD == 1 && WRITES_WORKLOAD == 0
    void read_workload();
// #elif READS_WORKLOAD == 0 && WRITES_WORKLOAD == 1
    void write_workload();
// #endif
    void render();
}