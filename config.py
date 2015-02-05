'''
Created on 24 Jan 2015

@author: joe
'''
import yaml

from functions import quit_script

class YAMLConfigLoader:
    
    def __init__(self,filename="config.yaml"):
        self.config = {}
        try:
            with open(filename,'r') as f:
                self.config = yaml.load(f.read())
        except IOError:
            quit_script("Error opening config.yaml", 2)
        except yaml.parser.ParserError as e:
            print "\n"
            print e
            quit_script("Configuration error found in config.yaml. Please check YAML syntax.", 3)
            
    def get_section(self,section):
        if self.config.has_key(section):
            if isinstance(self.config[section],dict):
                return self.config[section]
            else:
                quit_script("config.yaml has an error with the '{0}' section. See config.yaml.example for a prototype.".format(section), 3)
        else:
            quit_script("config.yaml has no '{0}' section. Unable to continue.".format(section), 3)
            

        