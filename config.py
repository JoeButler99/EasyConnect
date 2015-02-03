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
            quit_script("Configuration error found in config.yaml. Please check YAML syntax.", 2)
            
            
    def get_tokens(self,key):
        try:
            return self.config['tokens'][key]
        except:
            print "Did not find config for module: %s. Has this been configured in config.yaml?" % key