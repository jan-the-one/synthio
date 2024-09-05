#!MOCK
from benchgen.constants import OUTPUT_PATH, EXPERIMENTS_PATH, TEMPLATES_PATH
from .core import Weaver
from .pl_manager import CppTemplatePlManager
from .tokenizer import CppTokenizer
import shutil
import os

class MonkeyWeaver(Weaver):

    def __init__(self):
        self.__ip_tokenizer = CppTokenizer()
        self.__target_template = None
        self.__pl_manager = CppTemplatePlManager()
        self.__pl_config = None

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


    def derive_variants(self):
        if self.__pl_manager is None:
            raise RuntimeError("PL Manager not configured for weaver")

        self.__pl_manager.pl_config = {"template_targets": self.__pl_config, "lib_names": [], "found_ips": []}
        self.__pl_manager.target_template = self.__target_template
        self.__pl_manager.prep_env()
        self.__pl_manager.derive()

    def weave(self):
        
        if self.__target_template is None:
            raise Exception("ERROR: No template specified for weaving")
        
        self.__template_path = TEMPLATES_PATH + "/" + self.__target_template
        self.__output_path = OUTPUT_PATH + "/" + self.__target_template
        
        self.prep_env()
        
        for root, _, files in os.walk(self.__output_path):
            for filename in files:
                if filename.endswith(".cpp") or filename.endswith(".cc"):
                    self.process_file(os.path.join(root, filename))
        
    def process_file(self, path):

        with open(path, 'r') as file:
            buffer = file.readlines()
            if buffer is None:
                raise RuntimeError("Ran into an empty file. Make sure to remove it from the template!")
        
            for i, line in enumerate(buffer, 0):
                
                tokens = self.__ip_tokenizer.tokenize(line)

                if tokens is not None:

                    buffer[i]=""
                    continue

                buffer[i] = line

        with open(path, 'w') as file:
            file.writelines(buffer)

    def cleanup(self):
        ...

    @property
    def ip_tokenizer(self):
        return self.__ip_tokenizer

    @ip_tokenizer.setter
    def ip_tokenizer(self, ipt):
        self.__ip_tokenizer = ipt
        
    @property
    def module_info(self):
        return self.__module_info

    @module_info.setter
    def module_info(self, info):
        self.__module_info = info

    @property
    def target_template(self):
        return self.__target_template

    @target_template.setter
    def target_template(self, tt):
        self.__target_template = tt

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
    def handle(self):
        return self.__handle

    @handle.setter
    def handle(self, h):
        self.__handle = h
