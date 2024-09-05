import benchgen.constants as constants
import os
import shutil
from termcolor import colored
from .core import Weaver
from .module_binder import CPPModuleBinder
from .tokenizer import CppTokenizer
from .pl_manager import CppTemplatePlManager

class CppWeaver(Weaver):
    
    def __init__(self):
        self.__ip_tokenizer = CppTokenizer()
        self.__module_binder = CPPModuleBinder()
        self.__pl_manager = CppTemplatePlManager()
        self.__target_template = None
        self.__handle = None #see Gadget Manager
        self.__module_info = None #pass to the module binder; see Gadget Manager
        self.__ip_config = None   #see Config Manager
        self.__pl_config = None
        self.__found_ips = dict() #internal state
    
    @property 
    def found_ips(self):
        return self.__found_ips

    @property
    def handle(self):
        return self.__handle

    @handle.setter
    def handle(self, h):
        self.__handle = h

    @property
    def ip_config(self):
        return self.__ip_config

    @ip_config.setter
    def ip_config(self, ipc):
        self.__ip_config = ipc

    @property
    def pl_config(self):
        return self.__pl_config

    @ip_config.setter
    def pl_config(self, plc):
        self.__pl_config = plc

    @property
    def target_template(self):
        return self.__target_template

    @target_template.setter
    def target_template(self, tt):
        self.__target_template = tt

    @property
    def module_info(self):
        return self.__module_info

    @module_info.setter
    def module_info(self, info):
        self.__module_info = info

    @property
    def ip_tokenizer(self):
        return self.__ip_tokenizer

    @ip_tokenizer.setter
    def ip_tokenizer(self, ipt):
        self.__ip_tokenizer = ipt


    def prep_env(self):
        
        if (self.__template_path is None or self.__template_path == ""):
            raise Exception("ERROR: Malformed path for target template")

        if os.path.isdir(self.__template_path) == False:                
            raise RuntimeError("Could not find a directory for the given template name!")
        
        if (self.__output_path is None or self.__output_path == ""):
            raise Exception("ERROR: Malformed path for benchmarks")
        
        if os.path.exists(self.__output_path):
            shutil.rmtree(self.__output_path)
        shutil.copytree(self.__template_path, self.__output_path, dirs_exist_ok=True)

    def process_file(self, filepath):
        buffer = None
        headers_stash = None
        
        with open(filepath, 'r') as file:
            buffer = file.readlines()
            if buffer is None:
                raise RuntimeError("Ran into an empty file. Make sure to remove it from the template!")
            headers_stash = dict()
        
            new_buffer = []
            for line in buffer:
                
                tokens = self.__ip_tokenizer.tokenize(line)

                if tokens is not None:

                    indent = tokens[0]
                    ip_identifier = tokens[1]
                    
                    ip_data = self.__ip_config.get_item(ip_identifier)
                    if ip_data is None:
                        print(f"[WARNING] Injection Point with ID {ip_identifier} was found in template, but does not have a configured match!\n")
                        new_buffer.append("")
                        continue

                    if ip_identifier not in self.__found_ips.keys():
                        self.__found_ips[ip_identifier] = ip_data
                    
                    namespace = ip_data['gadget_name'] + "_" + ip_data['variant']
                    line = indent + namespace + "::" + self.__handle + ";\n" 

                    if ip_identifier not in headers_stash.keys():
                        headers_stash[ip_identifier] = "#include " + "\"" + namespace + ".h\"\n"                 
                
                new_buffer.append(line)

            buffer = new_buffer

        if headers_stash is not None and len(headers_stash) != 0:
            with open(filepath, 'w') as file:
                file.writelines(headers_stash.values())
                file.writelines(buffer)
        else:
            with open(filepath, 'w') as file:
                file.writelines(buffer)

    def weave(self):
        if self.__handle is None:
            raise Exception("ERROR: No handle provided to the Weaver")

        if self.__ip_config is None:
            raise Exception("ERROR: No IP configuration provided to the Weaver")
        
        if self.__target_template is None:
            raise Exception("ERROR: No template specified for weaving")
        
        if self.__module_info is None:
            raise Exception("ERROR: No module info provided to the Weaver")
        
        self.__template_path = constants.TEMPLATES_PATH + "/" + self.__target_template
        self.__output_path = constants.OUTPUT_PATH + "/" + self.__target_template
        
        self.prep_env()

        for root, _, files in os.walk(self.__output_path):
            for filename in files:
                if filename.endswith(".cpp") or filename.endswith(".cc"):
                    print(colored("Processing " + filename + " in `" + self.__target_template + "`....", "blue"), end='')
                    self.process_file(os.path.join(root, filename))
                    print(colored("[DONE]","blue"))


        print(colored("Preparing headers after weaving..","blue"), end='')
        self.__module_binder.project_path = self.__output_path
        self.__module_binder.module_configs = {"header_paths": self.__module_info['header_paths'], "found_ips": self.__found_ips}
        self.__module_binder.bind_modules()
        print(colored("[DONE]","blue"))

    def derive_variants(self):
        if self.__pl_manager is None:
            raise RuntimeError("PL Manager not configured for weaver")
        
        #! Three sets of dependencies needed overall
        #! 1. The templates config from the CM
        #! 2. The module info from the GM
        #! 3. The identified IPs in the template

        self.__pl_manager.pl_config = {"template_targets": self.__pl_config, "lib_names": self.__module_info['lib_names'], "found_ips": self.__found_ips}
        self.__pl_manager.target_template = self.__target_template
        self.__pl_manager.prep_env()
        self.__pl_manager.derive()
        
    def cleanup(self):
        pass