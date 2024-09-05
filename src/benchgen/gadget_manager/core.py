from abc import ABC, abstractmethod

class GadgetProductLine(ABC):
    
    @abstractmethod
    def derive_variants(self):
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
    def pl_config(self):
        ...

    @abstractmethod
    def get_module_info(self):
        ...
    
    @abstractmethod
    def get_default_handle(self):
        ...

class PLArtifact(ABC):
    
    @property
    @abstractmethod
    def module_definition(self):
        ...

    @module_definition.setter
    @abstractmethod
    def module_definition(self, mdf):
        ...

    @property
    @abstractmethod
    def binding_layer_definition(self):
        ...
