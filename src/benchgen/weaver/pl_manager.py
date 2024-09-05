from abc import ABC, abstractmethod
from benchgen import constants
import os
import subprocess
from termcolor import colored

class PLManager(ABC):
    
    @abstractmethod
    def derive(self):
        ...
    
    @abstractmethod
    def cleanup(self):
        ...

    @abstractmethod
    def prep_env(self):
        ...

    @property
    @abstractmethod
    def pl_config(self):
        ...

    @pl_config.setter
    @abstractmethod
    def pl_config(self, plc):
        ...
        
    @property
    @abstractmethod
    def target_template(self):
        ...
    @target_template.setter
    @abstractmethod
    def target_template(self, tt):
        ...

class CppTemplatePlManager(PLManager):
    
    def __init__(self):
        self.__template_targets = list()
        self.__target = None
        self.__target_variant = None
        self.__lib_names = dict()
        self.__found_ips = dict()

    @property
    def pl_config(self):
        return self.__template_targets
    
    @pl_config.setter
    def pl_config(self, plc):
        if plc is None or len(plc) == 0:
            raise Exception("ERROR: TPL Handler received bad config.")
        self.__template_targets = plc['template_targets']
        self.__lib_names = plc['lib_names']
        self.__found_ips = plc['found_ips']

    @property
    def target_template(self):
        return self.__target

    @target_template.setter
    def target_template(self, tt):
        self.__target = tt

    def prep_env(self):
        
        #! Check existence of weaved template
        #! Check existence of given template in the template targets
        #! Check if makefile exists
        
        if self.__target is None or self.__target == "":
            raise RuntimeError("ERROR: No target template provided to the TPL handler")

        if self.__template_targets is None or len(self.__template_targets) == 0:
            raise RuntimeError("ERROR: No config provided to the TPL handler")

        template_config = None
        for tc in self.__template_targets:
            if tc['name'] == self.__target:
                template_config = tc
                break

        if template_config is None:
            raise RuntimeError("Template Config not found!")
        
        weaved_template_path = constants.OUTPUT_PATH + "/" + template_config['name']
        makefile_path = weaved_template_path + "/Makefile"

        if not os.path.isfile(makefile_path):
            raise RuntimeError("Binding layer not found for targeted template!")
        
        cmd0 = "cd "+ weaved_template_path
        cmd1 = cmd0 + "; grep -o '^[^#[:space:]].*:' Makefile"
        process = subprocess.Popen(cmd1, shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)        

        output, errors = process.communicate()
        if errors.decode('utf-8') != "":
            raise RuntimeError("Binding layer malformed for template!")

        makefile_targets = output.decode('utf-8')
        found_target = False
               
        for line in makefile_targets.splitlines():
            if line.replace(':','').strip() == template_config['target_variant']:
                found_target = True
                break

        if found_target == False:
            raise RuntimeError("Binding layer malformed for template: could not find variant target")

        cmd_clean = cmd0 + "; make clean"
        process = subprocess.Popen(cmd_clean, shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)   

        _, errors = process.communicate()
        if errors.decode('utf-8') != "":
            raise Exception(errors)

        self.__target_variant = template_config['target_variant']
        
    def derive(self):
        
        print(colored(f"Starting derivation of template `{self.__target}:{self.__target_variant}`....\n", "blue"))

        if self.__target_variant is None:
            raise Exception("Target variant not available.")
        
        t_path = constants.OUTPUT_PATH + self.__target

        cmd0 = "cd " + t_path        
        cmd1 = cmd0 + "; make" + " " + self.__target_variant

        process = subprocess.Popen(cmd1, shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)        

        output, errors = process.communicate()
        errs = errors.decode('utf-8')
                
        if errs != "":
            raise Exception(errs)

        print(f"Target {self.__target_variant} in {self.__target} reported:\n\n{output.decode('utf-8')}\n---------------\n")

        cmd0 = "cd " + t_path
        cmd1 = ""
        if len(self.__found_ips) != 0:

            cmd1 = cmd0 + "; g++ -o final.bin main.o"
        
            for ip in self.__found_ips.values():
                gname = ip['gadget_name']
                base_name = self.__lib_names[gname]['base']
                extension = self.__lib_names[gname]['format']
                lib_name = "../" + constants.REPO_NAME + "/" + base_name + "_" + ip['variant'] + extension
                cmd1 += " " + lib_name
            
            cmd1 += " -lm; make tidy"
        else:
            cmd1 = cmd0 + "; g++ -o final.bin main.o; make tidy" 

        process = subprocess.Popen(cmd1, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        output, errors = process.communicate()
        errs = errors.decode('utf-8')
                
        if errs != "":
            raise Exception(errs)

    def cleanup(self):
        pass