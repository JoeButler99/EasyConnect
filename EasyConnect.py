'''
Created on 24 Jan 2015

@author: joe
'''
import sys
from config import YAMLConfigLoader, CLIParser
from structures import build_from_config, HostGroup

def run():
    yaml_config    = YAMLConfigLoader()
    root_hostgroup = HostGroup("Main Menu",yaml_config) 
    build_from_config(yaml_config.get_section('hosts'),root_hostgroup,yaml_config)
    
    if len(sys.argv) > 1:
        cli_parser = CLIParser()
        cli_parser.run(yaml_config)
    else:
        # Give the user a menu system
        root_hostgroup.display_menu()