'''
Created on 4 Feb 2015

@author: joe
'''
import os
import subprocess


class Shell:
    def open_ssh_terminal(self,hostname,user,config):
        command = "{0} -e 'ssh {1}@{2}' &".format(config['terminal_binary'],
                                                  user, hostname)
        os.system(command)
