#include "bp_gadget.h"
#include <algorithm>
#include <ctime>
#include <iostream>
#include <time.h>

/*
Parts of this implementation were based on https://stackoverflow.com/questions/28961405/is-there-a-code-that-results-in-50-branch-prediction-miss
And verified/explained based on https://www.agner.org/optimize/microarchitecture.pdf
*/

//! BRUTE_FORCE feature has UNROLL enabled through a constraint in the f-model

#if BRUTE_FORCE == 1 && TOKENIZED == 0 && BAD_SORT == 0 && TAIL == 0

#if CUSTOM_RNG == 1

#define X   1203885245
#define Y   21111
#define M   2147483648 //TODO make into KNOB

unsigned long long NS_NAME::lcg()
{
  return ((X * NS_NAME::sd + Y) % M);
}

void NS_NAME::lcg_tick_high()
{
    NS_NAME::sd = lcg() % BASE_MODULUS;
    if (NS_NAME::sd >= (BASE_MODULUS / 2))
      NS_NAME::lcg_tick_high();
}

void NS_NAME::lcg_tick_low()
{
    NS_NAME::sd = lcg() % BASE_MODULUS;
    if (NS_NAME::sd < (BASE_MODULUS / 2))
      NS_NAME::lcg_tick_low();
}

#define REP(n)                      \
    n = lcg();                    \
    if (n % 2)                      \
        NS_NAME::lcg_tick_high();        \
    else                            \
        NS_NAME::lcg_tick_low();         \

#else

unsigned long long NS_NAME::rnd_gen()
{
  unsigned long long rnd = 0;
  asm volatile ("rdrand %0;" : "=r" (rnd));
  return rnd;
}

#define REP(n)              \
    n = NS_NAME::rnd_gen();  \
    if (n % 2)               \
        rnd_gen();  \
    else                     \
        rnd_gen();  \

#endif

#define UNROLL_4_TIMES(n)  REP(n) REP(n) REP(n) REP(n)
#define UNROLL_16_TIMES(n) UNROLL_4_TIMES(n) UNROLL_4_TIMES(n) UNROLL_4_TIMES(n) UNROLL_4_TIMES(n)
#define UNROLL_64_TIMES(n) UNROLL_16_TIMES(n) UNROLL_16_TIMES(n) UNROLL_16_TIMES(n) UNROLL_16_TIMES(n)
#define UNROLL_128_TIMES(n) UNROLL_64_TIMES(n) UNROLL_64_TIMES(n) UNROLL_64_TIMES(n) UNROLL_64_TIMES(n)
#define UNROLL_256_TIMES(n) UNROLL_128_TIMES(n) UNROLL_128_TIMES(n) UNROLL_128_TIMES(n) UNROLL_128_TIMES(n)

void NS_NAME::bf()
{

#if CUSTOM_RNG == 1
  NS_NAME::sd = NS_NAME::lcg() % 9999;
#endif

    unsigned long long n;
    for (int i = 0; i < LOOP; i++)
    {
        UNROLL_256_TIMES(n);
    }
}

#elif TOKENIZED == 1 && BAD_SORT == 0 && TAIL == 0 && BRUTE_FORCE == 0
/*
The best way to influence branch prediction is to have a branch and feed it with unpredictable data. What we do below is to have some list of values within a range,
and have a pseudo-normal distribution of those values. We make sure that these values are unsorted. 
Then, we feed this to a branch that should be taken if the value is higher than the mean. 

We extend this further, allowing for "lopsided" conditions, i.e. branch should not be taken when the value is in the 25th percentile.

Another key factor here is that the inner loop where the branch is runs for more than BTB_SIZE-instructions. BTB_SIZE is assumed to be 4096, so any long-term memory of the branch predictor
is stressed accordingly.
*/

void NS_NAME::petrified_token() 
{
const unsigned sz = MEM_ALLOC / sizeof(int); //TODO standardize; make knob
unsigned long long data[sz];

for (int i=0; i < sz; i++){

#if TRUE_RND == 1
    unsigned long long rnd = 0;
    asm volatile ("rdrand %0;" : "=r" (rnd));
    data[i] = rnd % BASE_MODULUS;
#else
    data[i] = std::rand() % (BASE_MODULUS);
#endif
} 

#if IMPROVE_CPI == 1
  unsigned long long tmp = 0;
#endif

  for (unsigned i = 0; i < LOOP; ++i)
  {
    for (unsigned c = 0; c < sz; ++c)
    {
      if (data[c] >= MODULUS) //value here should be around half of the value used as % above.
      {
#if IMPROVE_CPI == 1
        tmp += data[c];
        tmp -= data[c];
#else
        __asm__("nop\n\t");
#endif
      }    
    }
  }
}

#elif TAIL == 1 && TOKENIZED == 0 && BAD_SORT == 0 && BRUTE_FORCE == 0

/*
In general, when we have two unbalanced recursing paths, the returns up the first (deeper) path will tend to be predicted based on the second (shorter) path.
Newer CPUs can handle this (we believe), but it can still cause some undersized effect.
This is what happens below, causing higher branch mispredictions (target)
*/

void NS_NAME::tail_wreck(int idx, int breakpoint, int size){

    if(idx == (breakpoint)) return;
    if(holdout_buff[idx] == 1) return;

    NS_NAME::tail_wreck(idx + 1, breakpoint, size);
    NS_NAME::tail_wreck(size - idx - 1, breakpoint, size);

#if IMPROVE_CPI == 1
    int tmp = holdout_buff[idx+1] + holdout_buff[idx+2];
#else
    __asm__("nop\n\t");
#endif
}

#elif BAD_SORT == 1 && TOKENIZED == 0 && TAIL == 0 && BRUTE_FORCE == 0

/*
Shaker Sort is a slight improvement of bubble sort, which will try to perform "swaps" in two directions simulatenously. 
This can reduce numbers of overall passes, but the branch miss rate can be amplified if we do wasteful work in one of the directions.
*/

void NS_NAME::swap(int *a, int *b) {
   int temp;
   temp = *a;
   *a = *b;
   *b = temp;
}

void NS_NAME::bad_sort() {
  
  int unsigned m = BTB_SIZE * ALLOC_SCALER; //todo knobify this
  // int unsigned m = MEM_ALLOC / 2; //todo knobify this

  int a[m];

  //!randomize
  for (unsigned c = 0; c < m; ++c)
    // a[c] = 123;
    a[c] = std::rand() % (127);

  int i, j, k;
  for(i = 0; i < m;) {
    for(j = i+1; j < m; j++) {
        if(a[j] < a[j-1])
          NS_NAME::swap(&a[j], &a[j-1]);
    }
    m--;

    for(k = m-1; k > i; k--) {
        if(a[k] < a[k-1])
        __asm__("nop\n\t");
    }
    i++;
  }
}

#endif

void NS_NAME::render()
{
#if BRUTE_FORCE == 1 && TOKENIZED == 0 && BAD_SORT == 0 && TAIL == 0

  NS_NAME::bf();

#elif TOKENIZED == 1 && BAD_SORT == 0 && TAIL == 0 && BRUTE_FORCE == 0

  NS_NAME::petrified_token();

#elif BAD_SORT == 1 && TOKENIZED == 0 && TAIL == 0 && BRUTE_FORCE == 0

  NS_NAME::bad_sort();

#elif TAIL == 1 && TOKENIZED == 0 && BAD_SORT == 0 && BRUTE_FORCE == 0

  size_t size = MEM_ALLOC;
  holdout_buff = new int[size];

  int breakpoint = size / (2 * (LOPSIDE + 1));
  int i;
  for(i=0;i<=breakpoint;i++){
      holdout_buff[i] = 0;
  }
  for(i=breakpoint+1;i<size;i++){
      holdout_buff[i] = 1;
  }
  for(i=0;i < LOOP;i++) {
      NS_NAME::tail_wreck(0, breakpoint, size);
  }

#else
    std::cout << "[BP GADGET] BAD WORKLOAD CONFIG!" << std::endl;
#endif

}
