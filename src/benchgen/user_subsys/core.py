
from enum import Enum
from benchgen.config_manager.core import ConfigTypes
from benchgen.gadget_manager.cpp_pline import GplCppHandler
from benchgen.weaver.monkey_weaver import MonkeyWeaver

class SynthIO:
    
    @property
    def target_template(self):
        return self.__target_template

    @target_template.setter
    def target_template(self, target_template):
        self.__target_template = target_template

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode

    @property
    def with_second_level(self):
        return self.__second_level_derivation

    @with_second_level.setter
    def with_second_level(self, wsl):
        self.__second_level_derivation = wsl

    @property
    def weaver(self):
        return self.__weaver

    @weaver.setter
    def weaver(self, weaver):
        self.__weaver = weaver
        
    def __init__(self, weaver = None):
        self.__weaver = weaver
        
    def boot_weaver(self, configManager, gadgetManager, mock = False):
        
        if mock:
            self.__weaver = MonkeyWeaver()

        if self.__weaver is None:
            raise RuntimeError("Weaver is not initialized!") 
        self.__weaver.handle = gadgetManager.get_default_handle()    
        self.__weaver.module_info = gadgetManager.get_module_info()

        self.__weaver.ip_config = configManager.get_config_for(ConfigTypes.IP)
        self.__weaver.target_template = self.target_template
        
        if self.__second_level_derivation:
            self.__weaver.pl_config = configManager.get_config_items_for(ConfigTypes.TEMPLATE)
    
    def boot_gadget_manager(self, configManager):
        gadgetManager = GplCppHandler()
        gadgetManager.pl_config = configManager.get_config_items_for(ConfigTypes.GADGET)
        return gadgetManager
