# Generate Benchmarks

## How to use the framework [WIP]

- The framework is quite minimal, as it provides only two commands: `generate_benchmarks` and `compile_gadgets`. 
  Overall, the framework relies on two config files found under `src/configs/`. Besides the two commands, these config files are your main interface with the framework. 
- The `compile_gadgets` command will tell the framework to read the `gadget_registration.yml` config, which contains a description of the `gadgets`
  and their available configurations. 

  [WIP]
  
  `g++ -c main.cc -Igadget_headers`
  `g++ -o final.exe main.o ../gadgets_repo/test_gadget_c1.a ../gadgets_repo/test_gadget_c2.a -lm`

## How To Use the Weaved Templates in /out

- Make sure to provide an -Ipath option during compilation, where you include the *gadget_headers* path there. Otherwise the weaved
headers will not be found during compilation for the files in which the program weaves-in headers. We only weave headers naively, i.e. using `#include "header.h"` statements. The headers themselves are stored under `out/<your_weaved_template>/gadget_headers`.
## How to use the framework [WIP]

- The framework is quite minimal, as it provides only two commands: `generate_benchmarks` and `compile_gadgets`. 
  Overall, the framework relies on two config files found under `src/configs/`. Besides the two commands, these config files are your main interface with the framework. 
- The `compile_gadgets` command will tell the framework to read the `gadget_registration.yml` config, which contains a description of the `gadgets`
  and their available configurations. 

  [WIP]
  

## How To Use the Weaved Templates in /out

- Make sure to provide an -Ipath option during compilation, where you include the *gadget_headers* path there. Otherwise the weaved
headers will not be found during compilation for the files in which the program weaves-in headers. We only weave headers naively, i.e. using `#include "header.h"` statements. The headers themselves are stored under `out/<your_weaved_template>/gadget_headers`.

This is simply because we cannot anticipate a fixed project structure, and we also don't want to pollute the files with statements
like `#include "../../../header.h"`. 

- Make sure to link libraries correctly; you need to use the -L option, providing the path to the `out/gadgets_repo` to it. We only put libraries in this "global" repository w.r.t. the weaved templates, so as not to keep multiple duplicates around. For each weaved template, you should link the libraries that correspond to the headers that are auto-genereated for your template, found under `out/<your_weaved_template>/gadget_headers`. 

- Note: The compiled libraries are global also because we decouple the library compilation from the weaving. You can re-weave your template and skip the compilation of libraries. This is helpful when you already have the desired libraries (or want to use some manually generated one), and simply want to modify your injection points in the template. Alternatively, you can choose to only compile libraries based on the config files, and handle the weaving on your own.

## How To Add new Gadgets [WIP]

The problem of adding new Gadgets is a bit cumbersome at this point, since there are two things to consider:

1. How do we compile the Gadget with a specific configuration, and make it into a library?
2. How do we enable a given template system to compile after we have weaved the gadgets in it?

For the first issue, it is enough for the framework to use the gadget_registration file, and go into each gadget folder expecting to find a Makefile there with a certain structure. More specifically, the framework expects to find a Makefile at the root of a Gadget. In that Makefile, it will search for the targets provided in the Gadget Registration config. Each target must correspond to a single configuration of the gadget (in terms of its feature model) - we call these targets `configuration-targets` hereafter. Each configuration-target must result in the generation of a unique library that has a name like: `<gadget_name>_<configuration_name>.a`.

Regarding the second issue, the framework uses the injection-points file to figure out what function calls to inject in a given template system. The injected calls typically look like `<gadget_name>_<gadget_configuration>::render()`. Note that the part preceding `::` is a Namespace. Since we will have compiled a separate library for each Gadget configuration, we don't want to have name-clashes on the `render()` call when we weave two different variants of the same gadget in the same template. 
Therefore, we must use Namespaces: the Gadget code must have a namespace, and only one header-exported function `render` within that namespace. The namespace name must be *unique* for each compiled library, so we require it to be uniquely defined by each configuration-target in the Makefile; that's why we suggest it is defined as a MACRO in the code, so that each configuration-target can manipulate it (just like with any other preprocessor directive). This means that inside each Gadget folder there should be a header file that contains the macro-defined namespace (and the `render` function within) - note that this header file **must** have the same name as the gadget (folder). Also note that the macro name for the Namespace must be `NS_NAME`, for now.

Once we have the above in place, the framework will take care to add a manually-crafted header file to the template, for each gadget variant that it intends to use. This ensures the compilation of the template after weaving. Linking libraries is then left to the user to do, which should be straightfoward considering that there will already be a library for each gadget variant.

So, to summarize:

1. The Gadget code needs to have a header file with the same name as the Gadget.
2. Inside that Header file we have a macro-defined Namespace, inside of which there is the definition of a function named `render()`. 
3. The Gadget code must have a Makefile in which we define an explicit target for each configuration of the Gadget. We call these `configuration-targets`.
4. Each `configuration-target` must provide a unique name to the Namespace macro in step 2, and result in the creation of a library. For now, we **require** the namespace name to be provided as `<gadget_name>_<configuration_target>`, which also guarantees uniqueness.
5. The framework will use configuration targets to compile the needed gadget variants (i.e. a library for each variant).
6. The framework will also add header files to the template system, one for each gadget variant. Note that these headers resemble the header file mentioned in step 1, but the namespace names will have been replaced with the `<gadget_name>_<configuration_target>` beforehands. This way we ensure that the template code compiles, and that the generated object file can be linked correctly with the libraries.
7. Note that the names of these `configuration_targets` are what should be used in the gadget_registration and injection_points files. We recommend to always name these targets as `c1`, `c2` etc., for uniformity.

### Improvements