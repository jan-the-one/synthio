from abc import ABC, abstractmethod

class Weaver(ABC):

    @abstractmethod
    def prep_env(self):
        ...

    @abstractmethod
    def derive_variants(self):
        ...

    @abstractmethod
    def weave(self):
        ...
        
    @abstractmethod
    def process_file(self, path):
        ...

    @abstractmethod
    def cleanup(self):
        ...

    @property
    @abstractmethod
    def ip_tokenizer(self):
        ...

    @ip_tokenizer.setter
    @abstractmethod
    def ip_tokenizer(self, ipt):
        ...
        
    @property
    @abstractmethod
    def module_info(self):
        ...

    @module_info.setter
    @abstractmethod
    def module_info(self):
        ...

    @property
    @abstractmethod
    def target_template(self):
        ...

    @target_template.setter
    @abstractmethod
    def target_template(self, tt):
        ...

    @property
    @abstractmethod
    def ip_config(self):
        ...

    @ip_config.setter
    @abstractmethod
    def ip_config(self, ipc):
        ...

    @property
    @abstractmethod
    def pl_config(self):
        ...

    @ip_config.setter
    @abstractmethod
    def pl_config(self, ipc):
        ...
        
    @property
    @abstractmethod
    def handle(self):
        ...

    @handle.setter
    @abstractmethod
    def handle(self, h):
        ...