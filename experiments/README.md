## Description

The IM extraction script is used to test the Gadgets themselves and to extract the Influence-Map of each Gadget.

The extracted data are then stored under `gadgets/<gadget>/docs`. 

### How To Use 

Normally we need to do the following:

- Weave the empty template using `python src/app.py generate_benchmark -t empty_template`

- After weaving the `empty_template`, one can simply go to the `out/empty_template` directory and follow two steps:

1. Compile the empty_template itself: `g++ -c -O0 main.cc -Igadget_headers`
2. Linke the generated libraries that correspond to the weaved template code:
    `g++ O0 -o final.exe main.o ../gadgets_repo/test_gadget_c1.a ../gadgets_repo/test_gadget_c2.a -lm`
    
    **Note**: Here we used two compiled gadget variants just as an example. 

The steps above apply for *any* template. You weave first, than you manually link everything.


However, the `gadget_im_extract` script will do the above automatically, for the `empty_template`. It will then run `perf` to measure
a list of predefined counters.


### Knobs

For c1-c6 --> the WSS knob does not have any impacts; logically the write-segment size is irrelevant for reproducibility. The ALLOC_SIZE does have an impact, as it offers adaptability in terms of the cache_sizes.
However, for reads with "reduce_cacheing" (c2) we also expect the behavior to be reproducible regardless of the ALLOC_SCALER, since the alloc_size does not matter for that configuration.

For c7-c10 --> the WSS knob has a pronounced impact (except for the "reduce_cacheing" case in c8). The ALLOC_SIZE also has an impact, as it offers adaptability in terms of cache_sizes.
The WSS impact is such that a value higher than the default will be less agressive on the TLB performance and thus Page Walks, but *may* induce more CPI due to larger units being written. The exact opposite is true if WSS is smaller than the default value. Our chosen default value corresponds to a "PAGE" size, but in other systems the TLB-subsystem may be organized differently and one might benefit from this knob.

For c1-c8 --> The OPS_SCALER will have a direct impact on 1. latency and 2. absolute numbers of cache references and cache misses. That's because the workload will be larger. A larger workload can simply help increase "resolution" in terms of the other metrics/counters and thus we allow some configurability w.r.t its size.