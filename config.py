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
            
    def get_hosts(self):
        if self.config.has_key("hosts"):
            if isinstance(self.config['hosts'],dict):
                return self.config['hosts']
            else:
                quit_script("config.yaml has an error in the 'hosts' section. This should be a map of groups and hosts. See config.yaml.example for a prototype.", 3)
        else:
            quit_script("config.yaml has no 'hosts' section. Unable to continue.", 3)