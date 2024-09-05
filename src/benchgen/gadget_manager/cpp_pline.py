from .core import GadgetProductLine, PLArtifact
import subprocess
import benchgen.constants as constants
import os, shutil
from termcolor import colored

#TODO use later; must make mockable
class CPPGadgetArtifact(PLArtifact):
    
    def __init__(self):
        self.__module = None
        self.__binding_layer = None #These artifacts should be set automatically here. 
    @property
    def module_definition(self):
        return self.__module

    @module_definition.setter
    def module_definition(self, mdf):
        self.__module = mdf

    @property
    def binding_layer_definition(self):
        return self.__binding_layer

class GplCppHandler(GadgetProductLine):

    def __init__(self):
        self.__gadget_targets = list()
        #! Must inject as PLArtifact
        self.__artifacts = dict() # gadget_name => artifacts metadata or buffered files; depends on the Artifact class implementation

    def get_default_handle(self):
        return "render()"

    def get_module_info(self):
        if len(self.__gadget_targets) == 0:
            raise RuntimeError("Could not fetch module info for gadget: Gadget Config is empty")

        #! we take a shortcut here, though we should use the Artifacts dictionary        
        header_paths = dict()
        lib_base_names = dict()
        for cnf in self.__gadget_targets:            
            header_paths[cnf['name']] = constants.GADGETS_PATH + cnf['name'] + "/" + cnf['name']+".h"
             # a bit redundant here, but abides by principles. 
             # in theory, the lib names can differ from the standard we are using here
             # it is the job of the GM to decide the lib names in any case
            lib_base_names[cnf['name']] = {"format": ".a", "base": cnf['name']}
        return {"header_paths": header_paths, "lib_names": lib_base_names} 
        
    @property
    def pl_config(self):
        return self.__gadget_targets

    @pl_config.setter
    def pl_config(self, conf):
        if conf is None or len(conf) == 0:
            raise Exception("ERROR: GPL Handler received bad config.")
        self.__gadget_targets = conf #todo should make mockable

    def prep_env(self):
        lib_path = constants.OUTPUT_PATH + "gadgets_repo"
        for filename in os.listdir(lib_path):
            file_path = os.path.join(lib_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise Exception('Failed to delete %s. Reason: %s' % (file_path, e))


    def derive_variants(self):
        self.__verify_binding_layer()        
        self.prep_env()

        for config in self.__gadget_targets:
            print(colored(f"Starting work on Gadget `{config['name']}`....\n", "blue"))

            for target in config['variants']:
                g_path = constants.GADGETS_PATH + config['name']
                cmd0 = "cd "+ g_path + "/" + config['makefile_path']
                knobs = list()
                
                if 'options' in target and len(target['options']) != 0:
                    knobs = target['options']
                
                knob_flags = ""
                if len(knobs):
                    for k in knobs:
                        for key, val in k.items():
                            knob_flags += f"{key.upper()}={val} "
                    print(colored(f"Using knob setting: {knob_flags}", "yellow"))                    

                if knob_flags != "":
                    cmd1 = cmd0 +  ";make " + knob_flags + " " + target['id']
                else:
                    cmd1 = cmd0 +  ";make " + target['id']
                    

                cmd2 = cmd0 + ";make clean"
                
                process = subprocess.Popen(cmd1, shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
                
                output, errors = process.communicate()
                errs = errors.decode('utf-8')
                
                if errs != "":
                    raise Exception(errs)

                print(f"Target {target['id']} in gadget {config['name']} reported:\n\n{output.decode('utf-8')}\n---------------\n")
                
                lib_name = g_path + "/" + config['name'] + "_" + target['id'] + ".a"

                if os.path.isfile(lib_name):
                    shutil.copy(lib_name, constants.OUTPUT_PATH + "/" + constants.REPO_NAME + "/")
                else:
                    print(f"[WARNING] Library {lib_name} could not be generated!\n")

                cl_proc = subprocess.Popen(cmd2, shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
                
                _, errors = cl_proc.communicate()
                errs = errors.decode('utf-8')
                if errs != "":
                    print(f"[WARNING]: Could not cleanup Make artifacts in the source of lib {lib_name}: {errs}")
                    
            print(colored(f"Gadget `{config['name']}` ---> [DONE]\n\n===============\n", "blue"))


    def __verify_binding_layer(self):
        
        if len(self.__gadget_targets) == 0:
            raise RuntimeError("No gadget targets provided to the Gadget Manager!")

        for rg in self.__gadget_targets:

            rg_path = constants.GADGETS_PATH + rg['name'] + "/" + rg['makefile_path']
            makefile_path = rg_path + "/Makefile"

            if not os.path.isfile(makefile_path):
                return False

            cmd = "cd "+ rg_path
            cmd += "; grep -o '^[^#[:space:]].*:' Makefile"
            process = subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)

            output, errors = process.communicate()
            if errors.decode('utf-8') != "":
                return False

            makefile_targets = output.decode('utf-8')
            found_target = False
            for tg in rg['variants']:
                for line in makefile_targets.splitlines():
                    if line.replace(':','').strip() == tg['id'].strip():
                        found_target = True
                        continue

            if found_target == False:
                return False
            
        return True
    
    def cleanup(self):
        pass