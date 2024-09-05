
from enum import Enum
from benchgen.config_manager.core import ConfigTypes
from benchgen.config_manager import sanity_strategies
from benchgen.config_manager.manager import GadgetsConfig, TemplatesConfig, NativeLoader, IPConfig, ConfigManager
from benchgen.config_manager.core import Config
from pathlib import Path
import os
from .core import SynthIO
import random
from subprocess import run, Popen, PIPE, STDOUT
from benchgen.constants import OUTPUT_PATH, EXPERIMENTS_PATH, TEMPLATES_PATH
import json
import base64
import time
import itertools
from termcolor import colored

class SamplingIPConfig(Config):
    
    def __init__(self):
        self.config_type = ConfigTypes.IP
        super().__init__()

    def accept(self, configLoader):
        
        if "GADGET" not in os.environ: 
            self.__sample_range = [
                {"gadget_name":"bp_gadget", "variant": "c1"},
                {"gadget_name":"bp_gadget", "variant": "c2"},
                {"gadget_name":"bp_gadget", "variant": "c4"},
                {"gadget_name":"bp_gadget", "variant": "c5"},
                {"gadget_name":"bp_gadget", "variant": "c6"},
                {"gadget_name":"bp_gadget", "variant": "c7"},
                {"gadget_name":"bp_gadget", "variant": "c8"},
                {"gadget_name":"cache_gadget", "variant": "c1"},
                {"gadget_name":"cache_gadget", "variant": "c2"},
                {"gadget_name":"cache_gadget", "variant": "c3"},
                {"gadget_name":"cache_gadget", "variant": "c4"},
                {"gadget_name":"cache_gadget", "variant": "c5"},
                {"gadget_name":"cache_gadget", "variant": "c6"},
                {"gadget_name":"cache_gadget", "variant": "c7"},
                {"gadget_name":"cache_gadget", "variant": "c8"},
                {"gadget_name":"cache_gadget", "variant": "c13"},
                ]
        elif os.environ.get("GADGET").lower() == "bp":
            self.__sample_range = [
                {"gadget_name":"bp_gadget", "variant": "c1"},
                {"gadget_name":"bp_gadget", "variant": "c2"},
                {"gadget_name":"bp_gadget", "variant": "c4"},
                {"gadget_name":"bp_gadget", "variant": "c5"},
                {"gadget_name":"bp_gadget", "variant": "c6"},
                {"gadget_name":"bp_gadget", "variant": "c7"},
                {"gadget_name":"bp_gadget", "variant": "c8"},
            ] 
        elif os.environ.get("GADGET").lower() == "CG":
            self.__sample_range = [
                {"gadget_name":"cache_gadget", "variant": "c1"},
                {"gadget_name":"cache_gadget", "variant": "c2"},
                {"gadget_name":"cache_gadget", "variant": "c3"},
                {"gadget_name":"cache_gadget", "variant": "c4"},
                {"gadget_name":"cache_gadget", "variant": "c5"},
                {"gadget_name":"cache_gadget", "variant": "c6"},
                {"gadget_name":"cache_gadget", "variant": "c7"},
                {"gadget_name":"cache_gadget", "variant": "c8"},
                {"gadget_name":"cache_gadget", "variant": "c13"},
            ]            
        
        sample = [random.choice(self.__sample_range) for _ in self.__sample_range]
        
        items = []
        
        index = 0
        for el in  sample:
            # existing_item_with_same_variant = list(filter(lambda it: it['gadget_name'] == el['gadget_name'] and it['variant'] == el['variant'], items))
            
            # if existing_item_with_same_variant is None or len(existing_item_with_same_variant) == 0:
       
            item = {"id": str(index + 1), "gadget_name": el['gadget_name'], "variant": el['variant']}
            items.append(item)
            index += 1
        
        self.items = items
        
        
        self.__sample = sample
    
    def get_current_sample(self):
        
      return self.__sample

    def verify(self):
        ...

    def get_item(self, id):
        for ip in self.items:
            if ip['id'] == id:
                return ip
        return None

#!MOCK
class CountingIPConfig(Config):

    def __init__(self):
        self.config_type = ConfigTypes.IP
        super().__init__()

    def accept(self, configLoader):

        self.__sample_range = [
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c1"},
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c2"},
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c4"},
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c5"},
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c6"},
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c7"},
            {"id": '1', "gadget_name":"bp_gadget", "variant": "c8"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c1"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c2"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c3"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c4"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c5"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c6"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c7"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c8"},
            {"id": '1', "gadget_name":"cache_gadget", "variant": "c13"},
            ]

        data = ""
        next = 0  

        sync_file = Path("/tmp/synthio_sync")
        if not sync_file.is_file():
            os.mknod('/tmp/synthio_sync')
        else:
            with open('/tmp/synthio_sync', 'r') as f:
                data = f.readline()
        
        if data == "":
            data = "0"
            next = 0
        else:
            data = int(data)
            if data >= (len(self.__sample_range) - 1):
                data = "0"
                next = 0
            else:
                next = data + 1
                data = str(next)
            
        with open('/tmp/synthio_sync', 'w') as f:
            f.write(data)
        
        print(colored("[~~~WARNING~~~] For this experiment you MUST make sure to use only IP with ID 1.", "red"))
        self.items = [self.__sample_range[next]]

    def verify(self):
        ...

    def get_current_variant(self):
        
        with open('/tmp/synthio_sync', 'r') as f:
            data = f.readline()
        
        item = self.__sample_range[int(data)]
        
        return item['gadget_name'] + "_" + item['variant']
        
    def get_item(self, id):
        for ip in self.items:
            if ip['id'] == id:
                return ip
        return None

#!MOCK
class CombiningIPConfig(Config):

    def __gen_combinations(self):
        
        gadgets = list()
        if "GADGET" not in os.environ: 
            raise Exception("For this experiment you must specify a Gadget using the env variable GADGET, and values [BP, CG]")
        elif os.environ.get("GADGET").lower() == "bp":
            gadgets = [
                {"gadget_name":"bp_gadget", "variant": "c1"},
                {"gadget_name":"bp_gadget", "variant": "c2"},
                {"gadget_name":"bp_gadget", "variant": "c4"},
                {"gadget_name":"bp_gadget", "variant": "c5"},
                {"gadget_name":"bp_gadget", "variant": "c6"},
                {"gadget_name":"bp_gadget", "variant": "c7"},
                {"gadget_name":"bp_gadget", "variant": "c8"},
            ] 
        elif os.environ.get("GADGET").lower() == "cg":
            gadgets = [
                {"gadget_name":"cache_gadget", "variant": "c1"},
                {"gadget_name":"cache_gadget", "variant": "c2"},
                {"gadget_name":"cache_gadget", "variant": "c3"},
                {"gadget_name":"cache_gadget", "variant": "c4"},
                {"gadget_name":"cache_gadget", "variant": "c5"},
                {"gadget_name":"cache_gadget", "variant": "c6"},
                {"gadget_name":"cache_gadget", "variant": "c7"},
                {"gadget_name":"cache_gadget", "variant": "c8"},
                {"gadget_name":"cache_gadget", "variant": "c13"},
            ]


        combos = list(itertools.product(gadgets, gadgets))

        encoded_variants = list(map(self.__encode_config, combos))
        return encoded_variants
    
    def __decode_config(self, cnf):

        decoded_cnf = base64.b64decode(cnf)
        variants = decoded_cnf.decode("utf-8").split(";")
        return variants

    def __encode_config(self, variants):
        
        hashed_variants = ""
        
        for v in variants:
            if hashed_variants != "":
                hashed_variants += ";"
            hashed_variants += v['gadget_name'] + "_" + v['variant']            
            
        hashed_variants = (base64.b64encode(hashed_variants.encode('ascii'))).decode('utf-8')
        return hashed_variants

    def __init__(self):
        self.config_type = ConfigTypes.IP
        super().__init__()

    def accept(self, configLoader):

        combinations_file = ""
        if os.environ.get("GADGET").lower() == "bp":                    
            combinations_file = "/tmp/bp_combos"
        else:
            combinations_file = "/tmp/cg_combos"

        if not Path(combinations_file).is_file():
            os.mknod(combinations_file)

        if os.stat(combinations_file).st_size == 0:
            
            combos = self.__gen_combinations()
            with open(combinations_file, 'w') as f:
                for c in combos:
                    f.write(f"{c}\n")
     
        data = ""
        with open(combinations_file, 'r+') as f:
            data = f.readlines()
            f.seek(0)
            for l in data[1:]:
                f.write(l)
            f.truncate()

        variants = self.__decode_config(data[0])
        print(variants)

        self.items = []
        for i, v in enumerate(variants):
            toks = v.split("_")
            print(toks)
            self.items.append({'id': str(i+1), 'gadget_name': toks[0] + "_" + toks[1], 'variant': toks[2]})

        print(colored("[~~~WARNING~~~] For this experiment you MUST make sure to use only IPs with IDs 1, 2, 3 and so on. Otherwise the experiment will fail - it will result in a template with no weaved Gadgets! \n", "red"))

    def verify(self):
        ...

        
    def get_item(self, id):
        for ip in self.items:
            if ip['id'] == id:
                return ip
        return None


class EXP_TYPE(Enum):
    IMPACT_MAPPING=1
    CONSISTENCY=2
    BASELINE=3
    TEMPLATE=4
    COMBINATION=5

#TODO add support later
class MICRO_ARCH(Enum):
    SKYLAKE = 1
    HASWELL = 2

class Experiment(SynthIO):
    
    def reparse_metric(self, metric, results): #=> post-processing of results produced by `ocperf`
        
        counters = []
        for c in self.counters:
            cc = c
            if ":u" in c:
                cc = cc.replace(":u", '')
            counters.append(cc)
    
        values = []

        if os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "zen3":
        #   self.counters = [
        #     "branch-instructions",
        #     "branch-misses",
        #     "cycles",
        #     "instructions",
        #     "L1-dcache-loads",
        #     "L1-dcache-load-misses",
        #     "l2_request_g1.rd_blk_l",
        #     "l2_request_g1.rd_blk_x"   
        #   ]
        
            if (metric == "L1-load-miss-rate"):
                cm_refs = results[counters[4].replace('.','_')]
                cm_misses = results[counters[5].replace('.','_')]

                for i in range (0, len(cm_refs)):
                    if cm_refs[i] == 0:
                        values.append(-1)
                    else:
                        values.append(cm_misses[i] / cm_refs[i])
            elif (metric == "BR_MISS_RATE"):
                b_refs = results[counters[0].replace('.','_')]
                b_misses = results[counters[1].replace('.','_')]
                values = list(map(lambda x,y: x / y, b_misses, b_refs))
            elif (metric == "CPI"):
                cycles = results[counters[2]]
                instructions = results[counters[3]]
                values = list(map(lambda x,y:x / y, cycles, instructions))
            elif (metric == "BR_REFERENCES"):
                values = results[counters[0].replace('.','_')]
            elif (metric == "L1-loads"):
                values = results[counters[4].replace('.','_')]
            elif (metric == "BC_REFERENCES"):
                values = results[counters[8].replace('.','_')]
            elif (metric == "BR_CONDITIONAL_MISS_RATE"):
                bc_refs = results[counters[8].replace('.','_')]
                bc_misses = results[counters[9].replace('.','_')]
                values = list(map(lambda x,y:x / y, bc_misses, bc_refs))

            return values
    
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
            cm_refs = list(map(lambda x,y: (x + y), cm_misses, cm_hits))

            for i in range (0, len(cm_refs)):
                if cm_refs[i] == 0:
                    values.append(-1)
                else:
                    values.append(cm_misses[i] / cm_refs[i])
        elif (metric == "L1-hit-miss-ratio"):
            cm_hits = results[counters[8].replace('.','_')]
            cm_misses = results[counters[9].replace('.','_')]
        elif (metric == "L2-load-miss-rate"):
            cm_hits = results[counters[10].replace('.','_')]
            cm_misses = results[counters[11].replace('.','_')]
            cm_refs = list(map(lambda x,y: (x + y), cm_misses, cm_hits))

            for i in range (0, len(cm_refs)):
                if cm_refs[i] == 0:
                    values.append(-1)
                else:
                    values.append(cm_misses[i] / cm_refs[i])
        elif (metric == "L2-hit-miss-ratio"):
            cm_hits = results[counters[10].replace('.','_')]
            cm_misses = results[counters[11].replace('.','_')]
            values = list(map(lambda x,y:x / y, cm_misses, cm_hits))

            cm_refs = list(map(lambda x,y: (x + y), cm_misses, cm_hits))

            for i in range (0, len(cm_refs)):
                if cm_refs[i] == 0:
                    values.append(-1)
                else:
                    values.append(cm_misses[i] / cm_refs[i])
        elif (metric == "L3-load-miss-rate"):
            cm_hits = results[counters[12].replace('.','_')]
            cm_misses = results[counters[13].replace('.','_')]
            cm_refs = list(map(lambda x,y: (x + y), cm_misses, cm_hits))

            for i in range (0, len(cm_refs)):
                if cm_refs[i] == 0:
                    values.append(-1)
                else:
                    values.append(cm_misses[i] / cm_refs[i])
        elif (metric == "L3-load-miss-count"):
            cm_misses = results[counters[13].replace('.','_')]
            values = cm_misses
        elif (metric == "CPI"):
            cycles = results[counters[14]]
            instructions = results[counters[15]]
            values = list(map(lambda x,y:x / y, cycles, instructions))
        elif (metric == "Cycles"):
            values = results[counters[14]]
        elif (metric == "Instructions"):
            values = results[counters[15]]
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
        elif (metric == "L3-loads"):
            loads_1 = results[counters[12].replace('.','_')]
            loads_2 = results[counters[13].replace('.','_')]
            values = list(map(lambda x,y: x + y, loads_1, loads_2))        
        elif (metric == "FILL_BUFFER"):
            values = results[counters[17].replace('.','_')]
        elif (metric == "L3-stores"):
            cm_refs = results[counters[18].replace('.', '_')]
            values = cm_refs
        elif (metric == "L3-store-miss-rate"):
            cm_refs = results[counters[18].replace('.','_')]
            cm_misses = results[counters[19].replace('.','_')]
            values = []
            # print(cm_refs)
            # print(cm_misses)
            for i in range (0, len(cm_refs)):
                if cm_refs[i] == 0:
                    values.append(-1)
                else:
                    values.append(cm_misses[i] / cm_refs[i])
            # values = list(map(lambda x,y: x / y, cm_misses, cm_refs))
        elif (metric == "Store-page-walks"):
            values = results[counters[21].replace('.','_')]
        elif (metric == "BR_REFERENCES"):
            values = results[counters[22].replace('.','_')]
        elif (metric == "BC_REFERENCES"):
            values = results[counters[24].replace('.','_')]
        elif (metric == "BN_REFERENCES"):
            total = results[counters[22].replace('.','_')]
            conditional = results[counters[24].replace('.','_')]
            values = list(map(lambda x,y: x - y, total, conditional))
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
        elif (metric == "BR_NON_CONDITIONAL_MISS_RATE"):
            b_refs = results[counters[22].replace('.','_')]
            b_misses = results[counters[23].replace('.','_')]
            bc_refs = results[counters[24].replace('.','_')]

            bc_misses = results[counters[25].replace('.','_')]

            refs = list(map(lambda x,y: x - y, b_refs, bc_refs))
            misses = list(map(lambda x,y: x - y, b_misses, bc_misses))
            for i, m in enumerate(misses):
                if m < 0:
                    misses[i] = 0
            
            values = list(map(lambda x, y: x / y, misses, refs))

        elif (metric == "F_BOUND") and os.environ.get("ARCH") is None:
            b_refs = results[counters[26].replace('.','_')]
            b_misses = results[counters[27].replace('.','_')]
            values = list(map(lambda x,y: x / y, b_misses, b_refs))
        elif (metric == "BAD_SPEC") and os.environ.get("ARCH") is None:
            b_refs = results[counters[28].replace('.','_')]
            b_refs_2 = results[counters[29].replace('.','_')]
            values = list(map(lambda x,y: 1 - (x / y), b_refs, b_refs_2))
            
        return values

    def __prep_data_im(self, results, variant_name = "", for_template = False):
        
        #! PATCHING
        
        if for_template:
            l1_loads = self.reparse_metric("L1-loads", results)
            l2_loads = self.reparse_metric("L2-loads", results)
            l3_loads = self.reparse_metric("L3-loads", results)
            l3_stores = self.reparse_metric("L3-stores", results)
            l1_values = self.reparse_metric("L1-load-miss-rate", results)
            l2_values = self.reparse_metric("L2-load-miss-rate", results)
            l3_values = self.reparse_metric("L3-load-miss-rate", results)
            l3s_values = self.reparse_metric("L3-store-miss-rate", results)

            br_refs = self.reparse_metric("BR_REFERENCES", results)
            bc_refs = self.reparse_metric("BC_REFERENCES", results)
            bn_refs = self.reparse_metric("BN_REFERENCES", results)
            bmr_values = self.reparse_metric("BR_MISS_RATE", results)
            blr_values = self.reparse_metric("BR_CONDITIONAL_MISS_RATE", results)
            bcr_values = self.reparse_metric("BR_NON_CONDITIONAL_MISS_RATE", results)

            if os.environ.get("ARCH") is None:
                fbd_values = self.reparse_metric("F_BOUND", results)
                bs_values = self.reparse_metric("BAD_SPEC", results)
            else:
                bs_values = []
                fbd_values = []

            cpi_values = self.reparse_metric("CPI", results)
            instructions = self.reparse_metric("Instructions", results)

            return {
                "l1-loads": l1_loads,
                "l2-loads": l2_loads,
                "l3-loads": l3_loads,
                "l1-load-miss-rate": l1_values,
                "l2-load-miss-rate": l2_values,
                "l3-load-miss-rate": l3_values,
                "l3-stores": l3_stores,
                "l3-store-miss-rate": l3s_values,
                "instructions": instructions,
                "cpi": cpi_values,
                "branch-references": br_refs,
                "branch-non-conditional-references": bn_refs,
                "branch-conditional-references": bc_refs,
                "br-miss-rate": bmr_values,
                "br-conditionals-miss-rate": blr_values,
                "br-non-conditionals-miss-rate": bcr_values,
                "frontend-boundedness": fbd_values,
                "bad-speculation": bs_values,
            }

        elif "GADGET" in os.environ:
            if os.environ.get("GADGET").lower() == "bp":
                variant_name = "bp"
            else:
                variant_name = "cache"
        
        if "cache" in variant_name:

            l1_loads = self.reparse_metric("L1-loads", results)
            l2_loads = self.reparse_metric("L2-loads", results)
            l3_loads = self.reparse_metric("L3-loads", results)
            l3_stores = self.reparse_metric("L3-stores", results)
            l1_values = self.reparse_metric("L1-load-miss-rate", results)
            l2_values = self.reparse_metric("L2-load-miss-rate", results)
            l3_values = self.reparse_metric("L3-load-miss-rate", results)
            cpi_values = self.reparse_metric("CPI", results)
            l3s_values = self.reparse_metric("L3-store-miss-rate", results)
            pw_values = self.reparse_metric("Load-page-walks", results)
            pws_values = self.reparse_metric("Store-page-walks", results)
            
            return {
                "l1-loads": l1_loads,
                "l2-loads": l2_loads,
                "l3-loads": l3_loads,
                "l1-load-miss-rate": l1_values,
                "l2-load-miss-rate": l2_values,
                "l3-load-miss-rate": l3_values,
                "l3-stores": l3_stores,
                "cpi": cpi_values,
                "l3-store-miss-rate": l3s_values,
                "load-page-walks": pw_values,
                "store-page-walks": pws_values                
            }
            
        elif "bp" in variant_name:

            br_refs = self.reparse_metric("BR_REFERENCES", results)
            bc_refs = self.reparse_metric("BC_REFERENCES", results)
            bn_refs = self.reparse_metric("BN_REFERENCES", results)

            bmr_values = self.reparse_metric("BR_MISS_RATE", results)
            if os.environ.get("ARCH") is None:
                fbd_values = self.reparse_metric("F_BOUND", results)
                bs_values = self.reparse_metric("BAD_SPEC", results)
            else:
                fbd_values = []
                bs_values = []

            blr_values = self.reparse_metric("BR_CONDITIONAL_MISS_RATE", results)
            bcr_values = self.reparse_metric("BR_NON_CONDITIONAL_MISS_RATE", results)
            cpi_values = self.reparse_metric("CPI", results)

            return {
                "branch-references": br_refs,
                "branch-non-conditional-references": bn_refs,
                "branch-conditional-references": bc_refs,
                "br-miss-rate": bmr_values,
                "frontend-boundedness": fbd_values,
                "bad-speculation": bs_values,
                "br-conditionals-miss-rate": blr_values,
                "br-non-conditionals-miss-rate": bcr_values,
                "cpi": cpi_values
            }

        else:
            raise Exception("Wrong variant name during IM extraction.")

    def __init__(self, weaver = None):
        super().__init__(weaver)
        self.mode = EXP_TYPE.IMPACT_MAPPING
        if os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "zen3":
          self.counters = [
            "branch-instructions",
            "branch-misses",
            "cycles",
            "instructions",
            "L1-dcache-loads",
            "L1-dcache-load-misses",
            "l2_request_g1.rd_blk_l",
            "l2_request_g1.rd_blk_x",
            "ex_ret_cond",
            "ex_ret_cond_misp"
          ]

        elif os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "haswell":        
            self.counters = [
                "cache-misses",
                "cache-references", 
                "dTLB-loads", 
                "dTLB-load-misses", 
                "dTLB-stores", 
                "dTLB-store-misses",
                "L1-dcache-loads",
                "L1-dcache-load-misses", 
                "mem_load_uops_retired.l1_hit",
                "mem_load_uops_retired.l1_miss", 
                "mem_load_uops_retired.l2_hit",
                "mem_load_uops_retired.l2_miss",  
                "mem_load_uops_retired.l3_hit",
                "mem_load_uops_retired.l3_miss", 
                "cycles", 
                "instructions", 
                'dtlb_load_misses.miss_causes_a_walk', 
                'l1d_pend_miss.fb_full', 
                "LLC-stores", 
                "LLC-store-misses", 
                "dtlb_store_misses.stlb_hit", 
                "dtlb_store_misses.miss_causes_a_walk", 
                "branch-instructions", 
                "branch-misses", 
                "br_inst_retired.conditional", 
                "br_misp_retired.conditional",
            ]
        elif os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "kabylake":
            self.counters = [
                "cache-misses:u",
                "cache-references:u", 
                "dTLB-loads:u", 
                "dTLB-load-misses:u", 
                "dTLB-stores:u", 
                "dTLB-store-misses:u",
                "L1-dcache-loads:u",
                "L1-dcache-load-misses:u", 
                "mem_load_retired.l1_hit:u",
                "mem_load_retired.l1_miss:u", 
                "mem_load_retired.l2_hit:u",
                "mem_load_retired.l2_miss:u",  
                "mem_load_retired.l3_hit:u",
                "mem_load_retired.l3_miss:u", 
                "cycles:u", 
                "instructions:u", 
                'dtlb_load_misses.miss_causes_a_walk:u', 
                'l1d_pend_miss.fb_full:u', 
                "LLC-stores:u", 
                "LLC-store-misses:u", 
                "dtlb_store_misses.stlb_hit:u", 
                "dtlb_store_misses.miss_causes_a_walk:u", 
                "branch-instructions:u", 
                "branch-misses:u", 
                "br_inst_retired_conditional:u", 
                "br_misp_retired_conditional:u"
            ]
        else:
            self.counters = [
                "cache-misses:u",
                "cache-references:u", 
                "dTLB-loads:u", 
                "dTLB-load-misses:u", 
                "dTLB-stores:u", 
                "dTLB-store-misses:u",
                "L1-dcache-loads:u",
                "L1-dcache-load-misses:u", 
                "mem_load_retired.l1_hit:u",
                "mem_load_retired.l1_miss:u", 
                "mem_load_retired.l2_hit:u",
                "mem_load_retired.l2_miss:u",  
                "mem_load_retired.l3_hit:u",
                "mem_load_retired.l3_miss:u", 
                "cycles:u", 
                "instructions:u", 
                'dtlb_load_misses.miss_causes_a_walk:u', 
                'l1d_pend_miss.fb_full:u', 
                "LLC-stores:u", 
                "LLC-store-misses:u", 
                "dtlb_store_misses.stlb_hit:u", 
                "dtlb_store_misses.miss_causes_a_walk:u", 
                "branch-instructions:u", 
                "branch-misses:u", 
                "br_inst_retired_conditional:u", 
                "br_misp_retired_conditional:u",
                "topdown-total-slots:u", 
                "topdown-fetch-bubbles:u",
                "topdown-slots-retired:u", 
                "topdown-slots-issued:u"
            ]

    @property
    def gv_hash(self):
        return self.__gv_hash
    
    @gv_hash.setter
    def gv_hash(self, gvp):
        self.__gv_hash = gvp

    def __boot_config_manager(self, configs, strategy):
        configLoader = NativeLoader()
        configManager = ConfigManager(configs, configLoader)
        configManager.load_configs()

        configManager.sanity_strategy = strategy
        configManager.make_sanity_checks()

        return configManager

    def __weave_combination(self):
        configs = [GadgetsConfig(), CombiningIPConfig(), TemplatesConfig()]
        if self.with_second_level:
            configs.append(TemplatesConfig())
        strategy = sanity_strategies.GPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)
        gadgetManager = self.boot_gadget_manager(configManager)
        self.boot_weaver(configManager, gadgetManager)

        tmp_configs = configManager.get_config_for(ConfigTypes.TEMPLATE).items
        for tc in tmp_configs:
            if tc['name'] == self.target_template:
                self.__target_template_variant = tc['target_variant']
                break

        self.weaver.weave()
        
        if self.with_second_level:            
            self.weaver.derive_variants()

    def __weave_baseline(self, mock_weaver = True):
        configs = [GadgetsConfig(), IPConfig(), TemplatesConfig()]
        if self.with_second_level:
            configs.append(TemplatesConfig())
                        
        strategy = sanity_strategies.GPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)
        gadgetManager = self.boot_gadget_manager(configManager) 

        self.boot_weaver(configManager, gadgetManager, mock=mock_weaver)
        
        tmp_configs = configManager.get_config_for(ConfigTypes.TEMPLATE).items
        for tc in tmp_configs:
            if tc['name'] == self.target_template:
                self.__target_template_variant = tc['target_variant']

        self.weaver.weave()

        if self.with_second_level:            
            self.weaver.derive_variants()

    def __weave_cons(self):
        configs = [GadgetsConfig(), SamplingIPConfig(), TemplatesConfig()]
        if self.with_second_level:
            configs.append(TemplatesConfig())
                        
        strategy = sanity_strategies.GPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)
        gadgetManager = self.boot_gadget_manager(configManager) 

        self.boot_weaver(configManager, gadgetManager)

        tmp_configs = configManager.get_config_for(ConfigTypes.TEMPLATE).items
        for tc in tmp_configs:
            if tc['name'] == self.target_template:
                self.__target_template_variant = tc['target_variant']
                break

        self.weaver.weave()
        
        if self.with_second_level:            
            self.weaver.derive_variants()

    def __get_im(self):

        reps = 100
        if "REPS" in os.environ:
            reps = int(os.environ.get("REPS"))
        
        results = dict()
        
        cmd = "cd " + OUTPUT_PATH + self.target_template +"; "
        #!accomomdate need for "/scratch/geal00001/pmu-tools/ocperf"
        
        perf_command = cmd + "ocperf stat -r 1" 

        if os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "haswell":        
            perf_command = cmd + "/scratch/geal00001/pmu-tools/ocperf stat -r 1"
        elif os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "zen3":
            perf_command = cmd + "perf stat -r 1"

        for c in self.counters:
            perf_command+= " -e "+ c

        perf_command += " taskset -c 1 ./final.bin"

        print(colored("\nStarting instrumentation.. \n", "green"))
        
        for i in range(0, reps):
            perf_process = Popen(perf_command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)

            report = perf_process.communicate()[0].decode().splitlines()
            print(colored(f"\t\tGot report {i+1} - Moving on to the next measurement \n", "green"))
            for j in range(3,len(self.counters) + 3):
                items = report[j].split()
                if len(items) == 0:
                    continue

                key = items[1]
                # if ">" in key:
                #     key = items[2]
                #     if key in results:
                #         results[key].append(0)
                #     else:
                #         results[key] = [0]
                #     continue

                if ":u" in key:
                    key = key.replace(":u", '')

                if key in results:
                    results[key].append(int(items[0].replace('.','')))
                else:
                    results[key] = [int(items[0].replace('.',''))]
                    
        return results
    
    def __weave_im(self):

        configs = [GadgetsConfig(), CountingIPConfig(), TemplatesConfig()]
        if self.with_second_level:
            configs.append(TemplatesConfig())
                        
        strategy = sanity_strategies.GPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)

        gadgetManager = self.boot_gadget_manager(configManager) 

        self.boot_weaver(configManager, gadgetManager)
        self.weaver.weave()

        if self.with_second_level:            
            self.weaver.derive_variants()
 
        #!this only works for the mocked Config
        self.__current_variant = configManager.get_config_for(ConfigTypes.IP).get_current_variant()
        
    def run(self):
        
        print("Running in experimentation mode..")

        if self.weaver is None:
            raise RuntimeError("Weaver is not initialized!")
        
        if self.mode == EXP_TYPE.IMPACT_MAPPING:
            self.target_template = "empty_template"
            self.__weave_im()
            data = self.__get_im() #should return a dictionary for the current variant
            
            res = self.__prep_data_im(data, self.__current_variant)

            #! File must exists
            if os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "haswell":        
                dump_file = EXPERIMENTS_PATH + "haswell_im.json"
            elif os.environ.get("ARCH") is not None and os.environ.get("ARCH").lower() == "kabylake":
                dump_file = EXPERIMENTS_PATH + "kabylake_im.json"
            else:
                dump_file = EXPERIMENTS_PATH + "skylake_im.json"
                
            existing_dump = {}
            with open(dump_file, "r+") as f:
                existing_dump = json.load(f)
                f.seek(0)

                if len(existing_dump) == 0:
                    new_dump = {self.__current_variant: res}
                else:                    
                    existing_dump[self.__current_variant] = res
                    #TODO search for a given key           
                    # filtered_items = list(filter(lambda item: self.__current_variant not in item, existing_dump))
                    # filtered_items.append(to_dump)

                    new_dump = existing_dump

                json.dump(new_dump, f)
                f.truncate()
        
        elif self.mode == EXP_TYPE.CONSISTENCY:
            
            # for _ in range(0,10):

            self.__weave_cons()

            #! ################# ADDENDUM ####################
            results_dir = EXPERIMENTS_PATH + self.target_template + "_" + self.__target_template_variant + "_results"            
            if not os.path.isdir(results_dir):
                os.mkdir(results_dir)
                with open(results_dir+"/consistency_results.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/baseline.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/actual.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/combos.json", "w") as f:
                    f.write("{}")
            #! ################# ADDENDUM ####################

            dump_file = results_dir + "/consistency_results.json"

            data = self.__get_im() #should return a dictionary for the current variant
            
            res = self.__prep_data_im(data, for_template=True)

            variants = [ip['id'] + "_" + ip['gadget_name']+"_"+ip['variant'] for ip in self.weaver.found_ips.values()]
            
            hashed_variants = variants[0]
            for v in variants[1:]:
                hashed_variants += ";" + v
            
            hashed_variants = (base64.b64encode(hashed_variants.encode('ascii'))).decode('utf-8')

            existing_measurements = {}
            with open(dump_file, 'r+') as f:
                existing_measurements = json.load(f)
                f.seek(0)

                res['timestamp'] = int(time.time()) 

                if(os.environ.get("ARCH") is not None):
                    res['env'] = os.environ.get("ARCH").lower()

                if len(existing_measurements) == 0:
                    existing_measurements={hashed_variants:{'variants': variants, 'measurements': [res]}}
                else:
                    if hashed_variants in existing_measurements:
                        existing_measurements[hashed_variants]['measurements'].append(res)
                    else:
                        existing_measurements[hashed_variants] = {'variants': variants, 'measurements': [res]}

                json.dump(existing_measurements, f)
                f.truncate()

            # self.weaver = CppWeaver() # clears out the Weaver's state to prevent weaving issues in subsequent runs

        elif self.mode == EXP_TYPE.BASELINE:
            
            self.__weave_baseline()

            results_dir = EXPERIMENTS_PATH + self.target_template + "_" + self.__target_template_variant + "_results"
            if not os.path.isdir(results_dir):
                os.mkdir(results_dir)
                with open(results_dir+"/consistency_results.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/baseline.json", "w") as f:
                    f.write("{}")
            
                with open(results_dir+"/actual.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/combos.json", "w") as f:
                    f.write("{}")

            data = self.__get_im() #should return a dictionary for the current variant
            res = self.__prep_data_im(data, for_template=True)
            
            dump_file = results_dir + "/baseline.json"

            existing_measurements = {}
            with open(dump_file, 'r+') as f:
                existing_measurements = json.load(f)
                f.seek(0)

                res['timestamp'] = int(time.time())
                if(os.environ.get("ARCH") is not None):
                    res['env'] = os.environ.get("ARCH").lower()

                if len(existing_measurements) == 0:
                    existing_measurements={"baseline":{'measurements': [res]}}
                else:
                    # if "baseline" in existing_measurements:
                    #     existing_measurements["baseline"]['measurements'].append(res)
                    # else:
                    existing_measurements["baseline"] = {'measurements': [res]}

                json.dump(existing_measurements, f)
                f.truncate()

        elif self.mode == EXP_TYPE.TEMPLATE:
            self.__weave_baseline(mock_weaver = False) 
            
            results_dir = EXPERIMENTS_PATH + self.target_template + "_" + self.__target_template_variant + "_results"
            if not os.path.isdir(results_dir):
                os.mkdir(results_dir)
                with open(results_dir+"/consistency_results.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/baseline.json", "w") as f:
                    f.write("{}")
            
                with open(results_dir+"/actual.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/combos.json", "w") as f:
                    f.write("{}")

            dump_file = results_dir + "/actual.json"

            data = self.__get_im()            
            res = self.__prep_data_im(data, for_template=True)
            variants = [ip['gadget_name']+"_"+ip['variant'] for ip in self.weaver.found_ips.values()]
            
            hashed_variants = variants[0]
            for v in variants[1:]:
                hashed_variants += ";" + v            
            hashed_variants = (base64.b64encode(hashed_variants.encode('ascii'))).decode('utf-8')
            existing_measurements = {}

            with open(dump_file, 'r+') as f:
                existing_measurements = json.load(f)
                f.seek(0)

                res['timestamp'] = int(time.time()) 

                if len(existing_measurements) == 0:
                    existing_measurements={hashed_variants:{'variants': variants, 'measurements': [res]}}
                else:
                    if hashed_variants in existing_measurements:
                        existing_measurements[hashed_variants]['measurements'].append(res)
                    else:
                        existing_measurements[hashed_variants] = {'variants': variants, 'measurements': [res]}
                json.dump(existing_measurements, f)
                f.truncate()

        elif self.mode == EXP_TYPE.COMBINATION:
            self.__weave_combination()
            
            results_dir = EXPERIMENTS_PATH + self.target_template + "_" + self.__target_template_variant + "_results"
            if not os.path.isdir(results_dir):
                os.mkdir(results_dir)
                with open(results_dir+"/consistency_results.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/baseline.json", "w") as f:
                    f.write("{}")
            
                with open(results_dir+"/actual.json", "w") as f:
                    f.write("{}")

                with open(results_dir+"/combos.json", "w") as f:
                    f.write("{}")

            dump_file = results_dir + "/combos.json"

            data = self.__get_im()            
            
            res = self.__prep_data_im(data)
            
            existing_measurements = {}
            print(self.weaver.found_ips.values())
            variants = [ip['id'] + "_" + ip['gadget_name']+"_"+ip['variant'] for ip in self.weaver.found_ips.values()]
            
            hashed_variants = variants[0]
            for v in variants[1:]:
                hashed_variants += ";" + v
            
            hashed_variants = (base64.b64encode(hashed_variants.encode('ascii'))).decode('utf-8')

            with open(dump_file, 'r+') as f:
                existing_measurements = json.load(f)
                f.seek(0)

                res['timestamp'] = int(time.time()) 

                if len(existing_measurements) == 0:
                    existing_measurements={hashed_variants:{'variants': variants, 'measurements': [res]}}
                else:
                    if hashed_variants in existing_measurements:
                        existing_measurements[hashed_variants]['measurements'].append(res)
                    else:
                        existing_measurements[hashed_variants] = {'variants': variants, 'measurements': [res]}

                json.dump(existing_measurements, f)
                f.truncate()


        else:
            raise Exception("Unkown execution mode provided")