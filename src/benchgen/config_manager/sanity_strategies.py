from abc import ABC, abstractmethod
from .. import constants
import os.path
import subprocess
from . import core
class SanityStrategy(ABC):
    
    @abstractmethod
    def execute(self, configs, cm): #configs will also vary with the concrete sanity strategy.
        ... 

class GPLSanity(SanityStrategy):

    def execute(self, cm):
        pass

class TMPLSanity(SanityStrategy):

    def execute(self, cm):
        pass

class CrossSanity(SanityStrategy):

    def cross_check_ips_variants(self, configs):
        
        matches = dict()
        gadget_cnf = None
        ip_cnf = None
        for c in configs:
            if c.config_type == core.ConfigTypes.GADGET:
                gadget_cnf = c
                
            elif c.config_type == core.ConfigTypes.IP:
                ip_cnf = c
            
        if gadget_cnf is None or ip_cnf is None:
            raise Exception("Could not perform cross-checking of configurations.")
        
        for ip in ip_cnf.items:
            choice_found = False
            chosen_gadget = None

            for rg in gadget_cnf.items:
                if rg['name'] == ip['gadget_name']:
                    choice_found = True
                    chosen_gadget = rg
                    break

            if choice_found == False:
                print(f"Gadget required for IP with id #{ip['id']} is not registered!")
                return dict()

            target_found = False
            chosen_target = None
            for target in chosen_gadget['variants']:
                if target['id'] == ip['variant']:
                    target_found = True
                    chosen_target = target
                    break

            if target_found == False:
                print(f"Gadget found for IP with id #{ip['id']} but the targeted variant is not registered!")
                return dict()
            else:

                if chosen_gadget['name'] not in matches:
                    gv = {
                        "name": chosen_gadget['name'],
                        "makefile_path": chosen_gadget['makefile_path'],
                        "variants": [chosen_target]
                    }
                    matches[chosen_gadget['name']] = gv
                else:
                    matches[chosen_gadget['name']]['variants'].append(chosen_target) 
    
        return matches
        

    def execute(self, configManager):
        
        matches = self.cross_check_ips_variants(configManager.configs)
        if len(matches) == 0:
            raise Exception("Sanity Check failed: [Cross-Check]")      

        configManager.matched_ips_variants = matches
