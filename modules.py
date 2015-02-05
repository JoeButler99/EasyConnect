'''
Created on 4 Feb 2015

@author: joe
'''
import os
import subprocess

"""
        You should just be able to add new modules in here and they will work as
        if by magic in the rest of the program. :-)

"""


class Shell:
    def open_ssh_terminal(self,hostname,config):
        config  = config.get_section('config')
        command = "{0} -e 'ssh {1}@{2}' &".format(config['terminal_binary'],
                                                  config['default_user'], 
                                                  hostname)
        test = os.system(command)
        print test
