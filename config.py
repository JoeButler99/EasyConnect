'''
Created on 24 Jan 2015

@author: joe
'''
import sys
import os
import yaml
import argparse
from utilities import quit_script, ModuleParser
from structures import Host

class YAMLConfigLoader:
    
    def __init__(self,filename="config.yaml"):
        path = os.path.dirname(__file__)
        self.config = {}
        try:

            with open(path+"/"+filename,'r') as f:
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
            

        
        
class CLIParser:
    
    def __init__(self):
        self.parser = self.create_parser()
        self.args, self.extra_args = self.parser.parse_known_args()

    def flatten_groups(self,host_list,group):
        if isinstance(group, dict):
            for group_members in group.values():
                self.flatten_groups(host_list, group_members)
        else:
            for host in group:
                host_list.append(host)
        return host_list
        
    class ModuleListAction(argparse.Action):
        """ Use a custom action for the --list arg """
        def __call__(self, parser, namespace, values, option_string=None):
            ModuleParser().display_all_modules()
            sys.exit()
        
    
    def create_parser(self):
        parser = argparse.ArgumentParser(description="EasyConnect CLI Toolkit")
        parser.add_argument("-g", "--group", action="store", dest="group", required=True,type=str)
        parser.add_argument("-a", "--action", action="store", dest="action", required=True,type=str)
        # Cheat below - I've 'repurposed' the version exception to handle module listing
        parser.add_argument("-l", "--list-available-actions", action=self.ModuleListAction,nargs=0)
        return parser
    
    def run(self,yaml_config):
        assert isinstance(yaml_config, YAMLConfigLoader) 
        # Check the group exists, has hosts and grab it
        use_hosts = yaml_config.get_section("hosts")
        try:
            for g in self.args.group.split("::"):
                if isinstance(use_hosts,dict):
                    use_hosts = use_hosts[g]
                else:
                    # If use_hosts is not a dict, we should be looking for a 
                    # hostname within the group
                    use_hosts = [g]
        except KeyError:
            quit_script("Did not find group {0} in config.yaml ".format(self.args.group),4)

        # If we have dict, then flatten it to get all hosts
        if isinstance(use_hosts,dict):
            use_hosts = self.flatten_groups([], use_hosts)

        # Now we can create Host objects for the list of machines and run the action
        [ Host(host,yaml_config).action(self.args.action) for host in use_hosts ]
            
