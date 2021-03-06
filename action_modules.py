'''
Created on 4 Feb 2015

@author: joe
'''
import os
import sys
import subprocess
import nmap

"""
        You should just be able to add new modules in here and they will work as
        if by magic in the rest of the program. :-)
        
        Each method should have the required args of hostname and config in addition
        to self.
        
        The method names will be polished up to be used as actions so brief but descriptive is good
        
        Method names prefixed with '_' are not included, and they will be considered a 'private' 
        method.
"""
   


class Shell:
    def open_ssh_terminal(self,hostname,config):
        config  = config.get_section('config')
        command = "{0} 'ssh {1}@{2}' &".format(config['terminal_binary'],
                                                  config['default_user'], 
                                                  hostname)
        os.system(command)
    
    def open_in_browser(self,hostname,config):
        config  = config.get_section('config')
        command = "{0} {1} 2&1 > /dev/null  &".format(config['browser_binary'],hostname)
        os.system(command)
        
    def _longrunning_subprocess(self,command):
        child = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
        while True:
            try:
                out = child.stderr.read(1)
                if out == '' and child.poll() != None:
                    break
                if out != '':
                    sys.stdout.write(out)
                    sys.stdout.flush()
            except KeyboardInterrupt:
                            
                child.kill()
                break

    def tail_remote_log(self,hostname,config):
        config  = config.get_section('config')
        command = "ssh {0}@{1} 'tail -f /var/log/boot.log'".format(config['default_user'],hostname)
        self._longrunning_subprocess(command)


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