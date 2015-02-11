'''
Created on 4 Feb 2015

@author: joe
'''
import os
import subprocess
import nmap

"""
        You should just be able to add new modules in here and they will work as
        if by magic in the rest of the program. :-)
        
        Each method should have the required args of hostname and config in addition
        to self.
"""


   


class Shell:
    def open_ssh_terminal(self,hostname,config):
        config  = config.get_section('config')
        command = "{0} 'ssh {1}@{2}' ".format(config['terminal_binary'],
                                                  config['default_user'], 
                                                  hostname)
        test = os.system(command)
        print command
        
        
        p = subprocess.Popen(command,shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        p.wait()
        print p.__dict__
        print p.pid



#
#    Interaction with the python nmap module
#
class Nmap:
    def ping_host(self,hostname,config):
        nm      = nmap.PortScanner()
        nm.scan(hosts=hostname,arguments='-n -sP')
        if int(nm.scanstats()['uphosts']) == 1:
            print hostname , "\t" , nm._scan_result['scan'].itervalues().next()['status']['state']
        else:
            print hostname , "\t" , "down"