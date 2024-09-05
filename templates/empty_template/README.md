## Description

This template is used to test the Gadgets themselves and to extract the Influence-Map of each Gadget.

The extracted data are then stored under `gadgets/docs`. 


### How To Use

- Weave the empty template using `python src/app.py generate_benchmark -t empty_template`

- After weaving the `empty_template`, one can simply go to the `out/empty_template` directory and follow two steps:

1. Compile the empty_template itself: `g++ -c main.cc -Igadget_headers`
2. Linke the generated libraries that correspond to the weaved template code:
    `g++ -o final.exe main.o ../gadgets_repo/test_gadget_c1.a ../gadgets_repo/test_gadget_c2.a -lm`
    
    **Note**: Here we used two compiled gadget variants just as an example. 

The steps above apply for *any* template. You weave first, than you manually link everything.
