from abc import ABC, abstractmethod
import os
import shutil
from benchgen import constants

class ModuleBinder(ABC):
    
    @property
    @abstractmethod
    def project_path(self):
        ...
    @property
    @abstractmethod
    def module_configs(self):
        ...
        
    @module_configs.setter
    @abstractmethod
    def module_configs(self, t):
        ...
        
    @abstractmethod
    def bind_modules(self):
        ...

class CPPModuleBinder(ModuleBinder):
       
    @property
    def module_configs(self):
        return self.__module_configs
    
    @module_configs.setter
    def module_configs(self, mcf):
        self.__module_configs = mcf
        
    @property
    def project_path(self):
        return self.__project_path

    @project_path.setter
    def project_path(self, path):
        self.__project_path = path    

    #TODO prepend header guard
    #TODO append header guard closing statement
    
    def bind_modules(self):
        if self.__project_path is None:
            raise RuntimeError("No path given to the import handler")

        headers_path = self.__project_path + "/gadget_headers"
        os.mkdir(headers_path)
        

        for ip in self.__module_configs['found_ips'].values():
            gadget_header_path = self.__module_configs['header_paths'][ip['gadget_name']]
            buffer = list()
            try:
                with open(gadget_header_path, 'r') as g_header:
                    buffer = g_header.readlines()
                    for i, line in enumerate(buffer, 0): #makes value replacements in the header
                        
                        if "NS_NAME" in line:
                            if "namespace" in line:
                                line = line.replace("NS_NAME", ip['gadget_name'] + "_" + ip['variant'])
                        if "#if" in line or "#else" in line or "#def" in line or "#undef" in line or "#endif" in line or "#elif" in line or "//" in line:
                            line = ""
                        buffer[i] = line

            except Exception as e:
                print(f"[WARNING]: Gadget Header not found for gadget {ip['gadget_name']}. Weaving will be incomplete due to err: {e=}")
                continue

            header_guard = ip['gadget_name'].upper() + "_" + ip['variant'].upper() + "_GUARD"
            
            buffer.insert(0, "#define " + header_guard + "\n\n")
            buffer.insert(0, "#ifndef " + header_guard + "\n")

            buffer.append("\n#endif")

            try:
                with open(headers_path + "/" + ip['gadget_name'] + "_" + ip['variant'] + ".h", 'w+') as file:
                    file.writelines(buffer) #writes the new header, in the template location
            except Exception as e:
                print(f"[WARNING]: Header {ip['gadget_name']}_{ip['variant']} could not be added. Weaving will be incomplete due to err: {e=}")