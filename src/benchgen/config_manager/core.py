from abc import ABC, abstractmethod
from enum import Enum
from benchgen.constants import SRC_PATH

INJECTION_CONFIG_PATH = str(SRC_PATH.parent.absolute()) + "/configs/injection_points.yml"
GADGET_REGISTRATION_CONFIG_PATH = str(SRC_PATH.parent.absolute()) + "/configs/gadget_registration.yml"
TEMPLATE_REGISTRATION_CONFIG_PATH = str(SRC_PATH.parent.absolute()) + "/configs/template_registration.yml"

class ConfigTypes(Enum):
    GADGET = 1
    IP = 2
    TEMPLATE = 3
    
    def has_member(self, name):
        if name in self.__members__:
            return True
        return False

#Visitor Interface
class ConfigLoader(ABC):

    @abstractmethod
    def load_gadgets(self, cnf):
        ...

    @abstractmethod
    def load_ips(self, cnf):
        ...
        
    @abstractmethod
    def load_templates(self, cnf):
        ...

class Config(ABC):

    @abstractmethod
    def get_item(self, id):
        ...

    @abstractmethod
    def accept(self, configLoader):
        ...
    
    @abstractmethod
    def verify(self):
        ...
        
    def __init__(self):
        self.__items = dict()

    @property
    def config_type(self):
        return self.__config_type

    @config_type.setter
    def config_type(self, ct):
        self.__config_type = ct
        
    @property
    def items(self):
        return self.__items
    
    @items.setter
    def items(self, cf):
        self.__items = cf