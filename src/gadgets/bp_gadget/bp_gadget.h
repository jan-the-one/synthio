
#ifndef NS_NAME
#define NS_NAME bp_gadget_default
#endif

//! FEATURES
#ifndef BRUTE_FORCE
#define BRUTE_FORCE 0
#endif

#ifndef TRUE_RND
#define TRUE_RND 0
#endif

#ifndef TOKENIZED
#define TOKENIZED 0
#endif

#ifndef BAD_SORT
#define BAD_SORT 0
#endif

#ifndef TAIL
#define TAIL 0 
#endif

#ifndef IMPROVE_CPI
#define IMPROVE_CPI 0
#endif

#ifndef CUSTOM_RNG
#define CUSTOM_RNG 0
#endif

#define BASE_MODULUS 1024
#define LOP_SIZE 128
#define BASE_SIZE 16384 //bytes


//! KNOBS
#ifndef LOPSIDE
    #define LOPSIDE 0 //default 0; range 0-2
#elif LOPSIDE > 2
    #undef LOPSIDE
    #define LOPSIDE 0
#elif LOPSIDE < 0
    #undef LOPSIDE
    #define LOPSIDE 0
#endif

#ifndef ALLOC_SCALER
    #define ALLOC_SCALER 2 //default 2; range 1-4
#elif ALLOC_SCALER > 4
    #undef ALLOC_SCALER
    #define ALLOC_SCALER 2
#elif ALLOC_SCALER < 1
    #undef ALLOC_SCALER
    #define ALLOC_SCALER 2
#endif

#ifndef OPS_SCALER
    #define OPS_SCALER 1 //default 1; range 1-50
#elif OPS_SCALER > 100
    #undef OPS_SCALER
    #define OPS_SCALER 100
#elif OPS_SCALER < 1
    #undef OPS_SCALER
    #define OPS_SCALER 1
#endif

//! CONFIGS
#define LOOP (1000 * OPS_SCALER)

#define MEM_ALLOC (ALLOC_SCALER * BASE_SIZE)

#define MODULUS ((BASE_MODULUS / 2) - (LOP_SIZE * LOPSIDE))

#define KiB 1024
#define MiB 1024*KiB
#define GiB 1024L*MiB

#ifndef BTB_SIZE
#define BTB_SIZE (4 * KiB)
#endif

namespace NS_NAME
{
// #if BRUTE_FORCE == 1 && TOKENIZED == 0 && BAD_SORT == 0 && TAIL == 0

    // #if CUSTOM_RNG == 0
    static unsigned long long rnd;
    unsigned long long rnd_gen();
    // #else
        static unsigned long long sd;
        unsigned long long lcg();
        void lcg_tick_high();
        void lcg_tick_low();

    void bf();

// #elif TOKENIZED == 1 && BAD_SORT == 0 && TAIL == 0 && BRUTE_FORCE == 0
    
    void petrified_token();

// #elif TAIL == 1 && TOKENIZED == 0 && BAD_SORT == 0 && BRUTE_FORCE == 0
    static int *holdout_buff;
    void tail_wreck(int idx, int half, int size);
// #elif BAD_SORT == 1 && TOKENIZED == 0 && TAIL == 0 && BRUTE_FORCE == 0
    void swap(int *a, int *b);
    void bad_sort();
// #endif

    void render();
}

//! TODO add checks for the knobs