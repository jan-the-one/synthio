import subprocess
import os
import pathlib
from subprocess import run, Popen, PIPE, STDOUT
import matplotlib.pyplot as plt
from enum import Enum
import getopt, sys
import binascii
from termcolor import colored


SRC_PATH = pathlib.Path(__file__).parent.absolute()
EXEC_PATH = str(SRC_PATH.parent.absolute())
ET_PATH = str(SRC_PATH.parent.absolute()) + "/out/empty_template"

skl_counters = ["cache-misses", "cache-references", "dTLB-loads", "dTLB-load-misses", "dTLB-stores", "dTLB-store-misses","L1-dcache-loads","L1-dcache-load-misses", "mem_load_retired.l1_hit","mem_load_retired.l1_miss",  "mem_load_retired.l2_hit","mem_load_retired.l2_miss",  "mem_load_retired.l3_hit","mem_load_retired.l3_miss", "cycles", "instructions", 'dtlb_load_misses.miss_causes_a_walk', 'l1d_pend_miss.fb_full', "LLC-stores", "LLC-store-misses", "dtlb_store_misses.stlb_hit", "dtlb_store_misses.miss_causes_a_walk", "branch-instructions", "branch-misses", "br_inst_retired_conditional", "br_misp_retired_conditional"]
hsw_counters = ["cache-misses", "cache-references", "dTLB-loads", "dTLB-load-misses", "dTLB-stores", "dTLB-store-misses","L1-dcache-loads","L1-dcache-load-misses", "mem_load_uops_retired.l1_hit","mem_load_uops_retired.l1_miss",  "mem_load_uops_retired.l2_hit","mem_load_uops_retired.l2_miss",  "mem_load_uops_retired.l3_hit","mem_load_uops_retired.l3_miss", "cycles", "instructions", 'dtlb_load_misses.miss_causes_a_walk, l1d_pend_miss.fb_full', "LLC-stores", "LLC-store-misses"]

#extend
skl_counters = skl_counters + ["topdown-total-slots", "topdown-fetch-bubbles","topdown-slots-retired", "topdown-slots-issued"]

counters = skl_counters #default

plt.rcParams.update({'font.size': 14})

class MICRO_ARCH(Enum):
    SKYLAKE = 1
    HASWELL = 2


def plot_figs(results, fname, iterations, gadget_name):

    if gadget_name == "cache_gadget":
        fig, ax = plt.subplots(7, figsize=(14,14), constrained_layout=True)

        l1_values = reparse_metric("L1-load-miss-rate", results)
        ax[0].hist(l1_values, bins = 10, color = 'green', edgecolor = 'black', label = 'L1_LOAD_MISS_RATE')
        ax[0].legend(loc="upper left")

        l2_values = reparse_metric("L2-load-miss-rate", results)
        ax[2].hist(l2_values, bins = 10, color = 'blue', edgecolor = 'black', label = 'L2_LOAD_MISS_RATE')
        ax[2].legend(loc="upper left")
        
        l3_values = reparse_metric("L3-load-miss-rate", results)
        ax[3].hist(l3_values, bins = 10, color = 'cyan', edgecolor = 'black', label = 'L3_LOAD_MISS_RATE')
        ax[3].legend(loc="upper left")
        
        cpi_values = reparse_metric("CPI", results)
        ax[1].hist(cpi_values, bins = 10, color = 'red', edgecolor = 'black', label = 'CPI')
        ax[1].legend(loc="upper right")
        
        l3s_values = reparse_metric("L3-store-miss-rate", results)
        ax[4].hist(l3s_values, bins = 10, color = 'purple', edgecolor = 'black', label = 'L3_STORE_MISS_RATE')
        ax[4].legend(loc="upper left")
        
        pw_values = reparse_metric("Load-page-walks", results)
        ax[5].hist(pw_values, bins = 10, color = 'orange', edgecolor = 'black', label = 'LOAD_PAGE_WALKS')
        ax[5].legend(loc="upper left")

        pws_values = reparse_metric("Store-page-walks", results)
        ax[6].hist(pws_values, bins = 10, color = 'olive', edgecolor = 'black', label = 'STORE_PAGE_WALKS')
        ax[6].legend(loc="upper left")
        
        fname = str(SRC_PATH.parent.absolute()) + "/experiments/CG_IM/" + fname + "_"+ binascii.hexlify(os.urandom(2)).decode() +".png"

    elif gadget_name == "bp_gadget":
        fig, ax = plt.subplots(6, figsize=(14,14), constrained_layout=True)

        br_values = reparse_metric("BR_REFERENCES", results)
        ax[0].hist(br_values, bins = 10, color = 'green', edgecolor = 'black', label = 'BRANCH INSTRUCTIONS')
        ax[0].legend(loc="upper left")

        bmr_values = reparse_metric("BR_MISS_RATE", results)
        ax[1].hist(bmr_values, bins = 10, color = 'red', edgecolor = 'black', label = 'BRANCH MISS RATE')
        ax[1].legend(loc="upper left")

        fbd_values = reparse_metric("F_BOUND", results)
        ax[2].hist(fbd_values, bins = 10, color = 'blue', edgecolor = 'black', label = 'FRONTEND BOUNDEDNESS')
        ax[2].legend(loc="upper left")
        
        bs_values = reparse_metric("BAD_SPEC", results)
        ax[3].hist(bs_values, bins = 10, color = 'orange', edgecolor = 'black', label = 'BAD SPECULATION (%)')
        ax[3].legend(loc="upper left")

        blr_values = reparse_metric("BR_CONDITIONAL_MISS_RATE", results)
        ax[4].hist(blr_values, bins = 10, color = 'cyan', edgecolor = 'black', label = 'BRANCH CONDITIONALS MISS RATE')
        ax[4].legend(loc="upper left")
        
        cpi_values = reparse_metric("CPI", results)
        ax[5].hist(cpi_values, bins = 10, color = 'red', edgecolor = 'black', label = 'CPI')
        ax[5].legend(loc="upper right")
        
        
        fname = str(SRC_PATH.parent.absolute()) + "/experiments/BP_IM/" + fname + "_"+ binascii.hexlify(os.urandom(2)).decode() +".png"

    else:        
        raise Exception("Wrong Gadget name!")
    
    plt.savefig(fname, dpi=150)


def reparse_metric(metric, results): #=> post-processing of results produced by `ocperf`
    
    #TODO the reparsing below is specific for the SKL counters. 
    #! TODO adapt the script for HSW.
    values = -1
    if (metric == "cache-miss-rate"):
            cm_refs = results[counters[1]]
            cm_misses = results[counters[0]]  
            values = list(map(lambda x,y:x / y, cm_misses, cm_refs))
    elif (metric == "L1-load-miss-count"):
        values = results[counters[9].replace('.','_')]
    elif (metric == "L2-load-miss-count"):
        values = results[counters[11].replace('.','_')]
    elif (metric == "L1-load-miss-rate"):
        cm_hits = results[counters[8].replace('.','_')]
        cm_misses = results[counters[9].replace('.','_')]
        values = list(map(lambda x,y: x / (x + y), cm_misses, cm_hits))
    elif (metric == "L1-hit-miss-ratio"):
        cm_hits = results[counters[8].replace('.','_')]
        cm_misses = results[counters[9].replace('.','_')]
        values = list(map(lambda x,y:x / y, cm_misses, cm_hits))
    elif (metric == "L2-load-miss-rate"):
        cm_hits = results[counters[10].replace('.','_')]
        cm_misses = results[counters[11].replace('.','_')]
        values = list(map(lambda x,y: x / (x + y), cm_misses, cm_hits))
    elif (metric == "L2-hit-miss-ratio"):
        cm_hits = results[counters[10].replace('.','_')]
        cm_misses = results[counters[11].replace('.','_')]
        values = list(map(lambda x,y:x / y, cm_misses, cm_hits))
    elif (metric == "L3-load-miss-rate"):
        cm_hits = results[counters[12].replace('.','_')]
        cm_misses = results[counters[13].replace('.','_')]
        values = list(map(lambda x,y: x / (x + y), cm_misses, cm_hits))
    elif (metric == "L3-load-miss-count"):
        cm_misses = results[counters[13].replace('.','_')]
        values = cm_misses
    elif (metric == "CPI"):
        cycles = results[counters[14]]
        instructions = results[counters[15]]
        values = list(map(lambda x,y:x / y, cycles, instructions))
    elif (metric == "Cycles"):
        values = results[counters[14]]
    elif (metric == "Load-page-walks"):
        values = results[counters[14].replace('.','_')]
    elif (metric == "L1-loads"):
        loads_1 = results[counters[8].replace('.','_')]
        loads_2 = results[counters[9].replace('.','_')]
        values = list(map(lambda x,y: x + y, loads_1, loads_2))
    elif (metric == "L2-loads"):
        loads_1 = results[counters[10].replace('.','_')]
        loads_2 = results[counters[11].replace('.','_')]
        values = list(map(lambda x,y: x + y, loads_1, loads_2))
    elif (metric == "FILL_BUFFER"):
        values = results[counters[17].replace('.','_')]
    elif (metric == "L3-store-miss-rate"):
        cm_refs = results[counters[18].replace('.','_')]
        cm_misses = results[counters[19].replace('.','_')]
        values = list(map(lambda x,y: x / y, cm_misses, cm_refs))
    elif (metric == "Store-page-walks"):
        values = results[counters[21].replace('.','_')]
    elif (metric == "BR_REFERENCES"):
        values = results[counters[22].replace('.','_')]
    elif (metric == "BR_MISSES"):
        values = results[counters[23].replace('.','_')]
    elif (metric == "BR_LOADS"):
        values = results[counters[24].replace('.','_')]
    elif (metric == "BR_MISS_RATE"):
        b_refs = results[counters[22].replace('.','_')]
        b_misses = results[counters[23].replace('.','_')]
        values = list(map(lambda x,y: x / y, b_misses, b_refs))
    elif (metric == "BR_CONDITIONAL_MISS_RATE"):
        b_refs = results[counters[24].replace('.','_')]
        b_misses = results[counters[25].replace('.','_')]
        values = list(map(lambda x,y: x / y, b_misses, b_refs))
    elif (metric == "F_BOUND"):
        b_refs = results[counters[26].replace('.','_')]
        b_misses = results[counters[27].replace('.','_')]
        values = list(map(lambda x,y: x / y, b_misses, b_refs))
    elif (metric == "BAD_SPEC"):
        b_refs = results[counters[28].replace('.','_')]
        b_refs_2 = results[counters[29].replace('.','_')]
        values = list(map(lambda x,y: 1 - (x / y), b_refs, b_refs_2))
        
    return values


############## FRAMEWORK WEAVING & BUILDING ##############
def run_fw():
    cmd = "cd " + EXEC_PATH + "; python3 src/app.py generate_benchmark -t empty_template"
    
    process = subprocess.Popen(cmd, shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)

    _, errors = process.communicate()
    errs = errors.decode('utf-8')

    if errs != "":
        raise Exception(errs)
################### TEMPLATE LINKING #####################
def link_template_gadgets(gadget_name):

    if gadget_name == "cache_gadget":
        cmd = "cd " + ET_PATH + "; g++ -c -O0 main.cc -Igadget_headers; g++ -O0 -o final.exe main.o ../gadgets_repo/cache_gadget_c1.a ../gadgets_repo/cache_gadget_c2.a ../gadgets_repo/cache_gadget_c3.a ../gadgets_repo/cache_gadget_c4.a ../gadgets_repo/cache_gadget_c5.a ../gadgets_repo/cache_gadget_c6.a ../gadgets_repo/cache_gadget_c7.a ../gadgets_repo/cache_gadget_c8.a ../gadgets_repo/cache_gadget_c9.a ../gadgets_repo/cache_gadget_c10.a ../gadgets_repo/cache_gadget_c13.a -lm"
    elif gadget_name == "bp_gadget":
        cmd = "cd " + ET_PATH + "; g++ -c -O0 main.cc -Igadget_headers; g++ -O0 -o final.exe main.o ../gadgets_repo/bp_gadget_c1.a ../gadgets_repo/bp_gadget_c2.a ../gadgets_repo/bp_gadget_c3.a ../gadgets_repo/bp_gadget_c4.a ../gadgets_repo/bp_gadget_c5.a ../gadgets_repo/bp_gadget_c6.a ../gadgets_repo/bp_gadget_c7.a ../gadgets_repo/bp_gadget_c8.a -lm"
    else:
        raise Exception("Could not link.. wrong gadget name")
    
    process = subprocess.Popen(cmd, shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)

    _, errors = process.communicate()
    errs = errors.decode('utf-8')

    if errs != "":
        raise Exception(errs)

################ RUNNER ##############    
def run_experiment(iterations, perf_command):

    results = dict()

    for _ in range(0, iterations):
        perf_process = Popen(perf_command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)

        report = perf_process.communicate()[0].decode().splitlines()

        for j in range(3,len(counters) + 3):
            items = report[j].split()
            if len(items) == 0:
                continue

            key = items[1]
            if key in results:
                results[key].append(int(items[0].replace('.','')))
            else:
                results[key] = [int(items[0].replace('.',''))]
                
    return results

############### MAIN #################
def main():
    arch = MICRO_ARCH(1)
    arg_help = "{0} -m <microarchitecture name> [only for intel] -e <experiment name> [saves plot in files starting with <experiment name>] -r [number of experiment runs] -s [skip rebuilding of template]".format(sys.argv[0])
    arg_march = ""
    arg_ename = ""
    arg_repeat = 50
    skip_rebuild = False
    gadget_name = "bp_gadget" #default
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:e:r:g:s", ["help", "microarchitecture=", "experiment=", "repeat=", "gadget=", "skip"])
    except:
        print("Provided option flag is not recognized. \nUsage: \n\t\t")
        print(arg_help)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-m", "--microarchitecture"):
            arg_march = arg
        elif opt in ("-e", "--experiment"):
            arg_ename = arg
        elif opt in ("-g", "--gadget"):
            gadget_name = arg
        elif opt in ("-s", "--skip"):
            skip_rebuild = True
        elif opt in ("-r", "--repeat"):
            arg_repeat = int(arg)


    if arg_march != "":
        arch = MICRO_ARCH[arg_march.upper()]

    if arch == MICRO_ARCH.SKYLAKE:
        counters = skl_counters
    elif arch == MICRO_ARCH.HASWELL:
        counters = hsw_counters
        
    if not skip_rebuild:
        print(colored("Invoking framework..", "green"))
        run_fw() #=> Will run the framework on the `empty_template`
    else:
        print(colored("Skipping framework invocation..", "green"))

    link_template_gadgets(gadget_name)

    perf_command="ocperf stat -r 1"

    for c in counters:
        perf_command+= " -e "+ c
    
    perf_command += " " + ET_PATH + "/final.exe"
    
    print(colored("Running experiment..", "green"))
    data = run_experiment(arg_repeat, perf_command) #=> Will run `perf stat` on the compiled `empty_template`` executable
    
    print(colored("Plotting and saving results..", "green"))
    plot_figs(data, arg_ename, arg_repeat, gadget_name)# => Will plot each counters' distribution

if __name__ == "__main__":
    main()