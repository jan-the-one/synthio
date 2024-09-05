from abc import ABC, abstractmethod
import re

class Tokenizer(ABC):
    
    @property
    @abstractmethod
    def ip_token(self):
        ...
        
    @abstractmethod
    def tokenize(self, line):
        ...
        
    
class CppTokenizer(Tokenizer):
    
    def __init__(self):
        self.__ip_token = '^\s*[#]{1}[I,i]{1}[P,p]{1}_\d+$'

    @property
    def ip_token(self):
        return self.__ip_token
    @property
    def found_ips(self):
        return self.__found_ips

    def tokenize(self, line):
        
        matched_ip = re.search(self.__ip_token, line)
        if matched_ip is not None:
            matched_tokens = line.split('#')

            indent = matched_tokens[0]
            ip_identifier = matched_tokens[1].replace('_','').replace('IP','').strip() #TODO this part is what the Tokenizer is all about; extracting the ip_id
            
            return (indent, ip_identifier)

        return None
