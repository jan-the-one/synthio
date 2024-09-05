import yaml
from .. import constants
from . import sanity_strategies
from .core import Config, ConfigLoader, ConfigTypes, GADGET_REGISTRATION_CONFIG_PATH, INJECTION_CONFIG_PATH, TEMPLATE_REGISTRATION_CONFIG_PATH

# Concrete "visitor" that handles two types of configs
class NativeLoader(ConfigLoader):

    def load_gadgets(self, cnf):
        
        with open(GADGET_REGISTRATION_CONFIG_PATH) as f:
            items = yaml.safe_load(f)
            cnf.items = items['gadgets']

    def load_ips(self, cnf):

        with open(INJECTION_CONFIG_PATH) as f:
            items = yaml.safe_load(f)
            cnf.items = items['injection_points']

    def load_templates(self, cnf):

        with open(TEMPLATE_REGISTRATION_CONFIG_PATH) as f:
            items = yaml.safe_load(f)
            cnf.items = items['templates']
            
class TemplatesConfig(Config):
    def __init__(self):
        self.config_type = ConfigTypes.TEMPLATE
        super().__init__()

    def accept(self, configLoader):
        configLoader.load_templates(self)
        self.verify()
        
    def verify(self):
        found_names = list()
        for tc in self.items:
            if tc['name'] not in found_names:
                found_names.append(tc['name'])
            else:
                raise Exception("Malformed Template registration file.")
        
    def get_item(self, id):
        pass

#Concrete Config Instances
class GadgetsConfig(Config):
    
    def __init__(self):
        self.config_type = ConfigTypes.GADGET
        super().__init__()
    
    def accept(self, configLoader):
        configLoader.load_gadgets(self)
        self.verify()
    
    def verify(self):
        found_names = list()

        for gc in self.items:
            if gc['name'] not in found_names:
                found_names.append(gc['name'])
            else:
                raise Exception("Malformed Gadget registration file.")

    def get_item(self, id):
        pass

class IPConfig(Config):
    
    def __init__(self):
        self.config_type = ConfigTypes.IP
        super().__init__()
    
    def accept(self, configLoader):
        configLoader.load_ips(self)
        self.verify()
    
    def verify(self):
        found_ids = list()
        for ip in self.items:
            if ip['id'] not in found_ids:
                found_ids.append(ip['id'])
            else:
                raise Exception("Malformed IP configs file.")

    def get_item(self, id):
        for ip in self.items:
            if ip['id'] == id:
                return ip
        return None

#The CM component itself
class ConfigManager:
    
    __configs = list()
    __loader = None

    def __init__(self, configs, loader):
        self.__configs = configs
        self.__sanity_strategy = None
        self.__loader = loader
    
    @property 
    def configs(self):
        return self.__configs
    
    @property
    def sanity_strategy(self):
        return self.__sanity_strategy

    @property
    def matched_ips_variants(self):
        return self.__matched_ip_gvs
    
    @matched_ips_variants.setter
    def matched_ips_variants(self, miv):
        self.__matched_ip_gvs = miv

    @sanity_strategy.setter
    def sanity_strategy(self, strategy):
        if isinstance(strategy, sanity_strategies.SanityStrategy):
            self.__sanity_strategy = strategy
        else:
            raise Exception("Wrong sanity strategy provided to Config Manager.")

    def load_configs(self):
        if self.__loader is None:
            raise Exception("No loader configured for Config Manager.")
        for c in self.__configs:
            c.accept(self.__loader)

    def get_config_items_for(self, handle):
        if isinstance(handle, ConfigTypes):
            for c in self.__configs:
                if c.config_type == handle:
                    return c.items

    def get_config_for(self, handle):
        if isinstance(handle, ConfigTypes):
            for c in self.__configs:
                if c.config_type == handle:
                    return c

    def make_sanity_checks(self):
        if self.__sanity_strategy == None:
            print("No strategy provided to config manager for sanity checks. Skipping ...")      
            return 
        self.__sanity_strategy.execute(self)                

