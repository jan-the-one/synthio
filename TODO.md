# TODO

### Phase 1

1. ~~Outline configurations~~ 
   1. ~~Start with Injection Points configs~~
   2. ~~Create sample YML file~~
2. ~~Define syntax for Injection Points~~
3. ~~Build conf_loader units~~
4. ~~Build ip replacer (recursive)~~
5. ~~ Build header_generator_unit~~
   1. ~~Define a simple exemplary Gadget first!~~
   2. ~~Might want to add a config for *namespace* and *gadget_path* in the gadget config file ⚠️~~

---

1. ~~Add a simple template with two features / configurations~~
2. ~~Add a simple gadget with two configurations~~
3. ~~Scope difficulty in linking the two gadgets~~
4. ~~Assess steps needed to add new Gadgets~~

---

1. ~~Think about providing Inputs to the Gadgets!~~
2. ~~Think about an explicit *Knobs* section in the configs, and how to provision knobs to the Gadget code.~~
   1. ~~This should help us avoid inputs!~~
   2. ~~But it couples the user interface (i.e. config files) to the Gadget SPL, and I don't like it!~~

### Phase 2 [DONE - CacheGadget]

In this phase we start integrating Gadgets / building more Gadgets. We also introduce some very simple templates and test things out.

Currently, we need to do the following:

~~1. For each config in the CG, weave a template and run it --> current status: we need to test each config and fix its behavior by configuring the Stride, WSL, MemAlloc, Operations.~~
~~2. Use a measurement script (adapt the old ones) and check the counters.~~
~~   1. The script would be best if it was more parametric, although it is not part of the "framework" itself.~~   
~~3. Identify knobs and add them to the Makefile~~
~~   1. Fix the subcompiler to handle knobs correctly (almost done)~~
4. ~~NOTE: The list of counters should be minified first!~~
~~5. Derive IMR for each configuration as a final step (plots for each counter of interest)~~

### Phase 3 [DONE - BrancPredictionGadget]
~~1. We experiment with Branch Prediction Ideas and try to identify features, configurations for the BPG~~
~~   1. Sorting algorithms~~
~~   2. Unsorted list~~
~~   3. BTB warmups~~
~~2. We also do minor refactors~~
~~   1. Move "configs" out of src folder~~
~~   2. Move "gadgets" inside src folder~~
~~   3. Make code more readable~~

~~### Phase 4~~
~~First, we make a big refactor based on the component architecture in the thesis. [DONE]~~

~~Then we add simple templates, and test things out. One thing to try out is the composing of multiple gadget types, as well as multiple variants from the same or different gadgets. 
We can even try using the same Gadget multiple times. [DONE]~~

~~The templates should contain minor workloads of their own, just to provide us with a baseline. Also, the template workload should not be "atomic", i.e. we should add Gadgets anywhere in between, though we need to keep in mind the semantics of a Gadget so that we don't get long-running benchmarks (Gadget = atomic workload unit that handles scaling on its own.) So the main goal here is to simply be able to add more workloads to a given feature implementation. [DONE]~~

~~We also document how the templates should look like and what requirements are there. We can [optionally] then try to build final executables for any arbitrary template - given some structure that we can anticipate. For now we leave the linking up to the user, though we make use of it in our scripts.~~

~~As a last step, we add the ability to build things in a 2-level SPL fashion.~~

### Evaluation

~~1. Must add header "guards" manually, in the weaver~~
~~   1. Otherwise experiments where two IPs map to the same variant are not possible ~~
~~   2. If not possible, we need to "limit" the experiments to cases where we don't use the same Gadget multiple times ~~
~~   3. Or alternatively, we need to use two different template configurations; in one of the configs we have repetitions of the same IP~~
~~ 4. Or alternatively x2, we can have the "shuffling" logic happen at the weaver somehow. ~~
   ~~   1. We have a pre-processing phase where we do "pre-weave" and simply shuffle around the IPs, e.g. from `#IP_1` to `#IP_3` ~~
~~2. Must add "timestamps" to the measurement we perform for the "consistency" experiments. We can have an ID which lists all variants somehow (perhaps we use some two-way hash / base64 encoding)~~

1. Gather data for the IM of Gadgets [DONE]
   1. Manually extract data relevant to the knobs [DONE]
2. Do a full reproducibility run and note down "differences"
   1. Need to check how to run Jobs with single-CPU affinity
3. Normalize 1-2 template configurations
4. Run the combo's experiment (10 times)
   1. Manually extract some data

## Issues
1. Extensibility
   1. Gadgets
   2. Templates
2. Correctness
3. Strong coupling between the Weaving process, and the Gadget's structure
   This issue is evident mostly in the fact that the Weaving process must also prepare Gadget Headers for the weaved template.


## Eval Notes:

### Side Effects (simple evaluation)

- The reproducibility test for the Gadgets can also capture
- "side-effects". If a config does not target a counter, but we see very different values across microarchs, that means we need to standardize it more to reduce discrepancies.

- The same logic applies to the simple evaluation of CIs for each counter. 