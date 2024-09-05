
from enum import Enum
from benchgen.config_manager.core import ConfigTypes
from benchgen.config_manager import sanity_strategies
from benchgen.config_manager.manager import ConfigManager
from benchgen.gadget_manager.cpp_pline import GplCppHandler
from benchgen.config_manager.manager import GadgetsConfig, IPConfig, TemplatesConfig, NativeLoader
from .core import SynthIO
class FW_TYPE(Enum):
    COMPILE_ONLY=1
    WEAVE_ONLY=2
    FULL_RUN=3
    TWO_LEVEL_SPL=4

class Framework(SynthIO):
            
    def __init__(self, weaver = None):
        super().__init__(weaver)
        self.mode = FW_TYPE.FULL_RUN

    # def __boot_weaver(self, configManager, gadgetManager):
        
    #     if self.weaver is None:
    #         raise RuntimeError("Weaver is not initialized!") 
    #     self.weaver.handle = gadgetManager.get_default_handle()    
    #     self.weaver.module_info = gadgetManager.get_module_info()

    #     self.weaver.ip_config = configManager.get_config_for(ConfigTypes.IP)
    #     self.weaver.target_template = self.target_template
        
    #     if self.with_second_level:
    #         self.weaver.pl_config = configManager.get_config_items_for(ConfigTypes.TEMPLATE)

    def __boot_config_manager(self, configs, strategy):
        configLoader = NativeLoader()
        configManager = ConfigManager(configs, configLoader)
        configManager.load_configs()

        configManager.sanity_strategy = strategy
        configManager.make_sanity_checks()

        return configManager

    # def __boot_gadget_manager(self, configManager):
    #     gadgetManager = GplCppHandler()
    #     gadgetManager.pl_config = configManager.get_config_items_for(ConfigTypes.GADGET)
    #     return gadgetManager

    def __compile_only(self):
                
        configs = [GadgetsConfig()]
        strategy = sanity_strategies.GPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)
        gadgetManager = self.boot_gadget_manager(configManager)

        gadgetManager.derive_variants()

    def __weave_only(self):
        
        configs = [GadgetsConfig(), IPConfig()]
        if self.with_second_level:
            configs.append(TemplatesConfig())

        strategy = sanity_strategies.TMPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)
        gadgetManager = self.boot_gadget_manager(configManager)
        self.boot_weaver(configManager, gadgetManager)
        self.weaver.weave()
        
        if self.with_second_level:            
            self.weaver.derive_variants()

    def __full_run(self):

        configs = [GadgetsConfig(), IPConfig()]

        if self.with_second_level:
            configs.append(TemplatesConfig())
                        
        strategy = sanity_strategies.GPLSanity()
        configManager = self.__boot_config_manager(configs, strategy)
        gadgetManager = self.boot_gadget_manager(configManager) 
        self.boot_weaver(configManager, gadgetManager)

        gadgetManager.derive_variants()
        self.weaver.weave()

        #!second-level derivation is restricted to only the full-run case        
        if self.with_second_level:            
            self.weaver.derive_variants()

    def __experiment(self):
        ...

    def run(self):
        if self.mode == FW_TYPE.COMPILE_ONLY:
            self.__compile_only()
        elif self.mode == FW_TYPE.WEAVE_ONLY:
            self.__weave_only()
        elif self.mode == FW_TYPE.FULL_RUN:
            self.__full_run()
        elif self.mode == FW_TYPE.EXPERIMENT:
            self.__experiment()
        else:
            raise Exception("Unkown execution mode provided")
