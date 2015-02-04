'''
Created on 24 Jan 2015

@author: joe
'''

from config import YAMLConfigLoader
from structures import build_from_config, HostGroup

def run():

    yaml_config    = YAMLConfigLoader()
    root_hostgroup = HostGroup("Main Menu") 
    build_from_config(yaml_config.get_hosts(),root_hostgroup)

    root_hostgroup.display_menu()