import inspect
import sys
from functions import clear_screen,  write_in_color, bcolors, quit_script, check_int, parse_menu_action
from modules import *

class Host:
    def __init__(self,hostname,config):
        self.name         = hostname
        self.config       = config
        
    def action(self,action_name=None):
        """
            Action trys to run the action. Based on the action name it
            will try to dynamically instantiate a class and excute the
            required method.
        """
        available_modules = { x[0] : x[1] for x in inspect.getmembers(sys.modules['modules'], inspect.isclass)}
        
        # Make sure we have a module to execute
        if not action_name:
            default_used = True
            action_name = self.config.get_section('config')['default_host_action']
        else:
            default_used = False
            
        parts = action_name.split("::")
        if len(parts) != 2:
            if default_used:
                quit_script("Error with default_host_action in config. See config.yaml.example for a working example", 5)
            else:
                quit_script("Could not perform action {0}. Does this exist in modules?".format(action_name), 5)
        else:
            classname , methodname = parts
        if classname not in available_modules.keys():
            quit_script("Could not find class {0} in modules".format(classname), 5)
        
        # Create a class instance and check the method exists.
        action_module = available_modules[classname]()
        method = getattr(action_module, methodname)
        method(self.name,self.config)
        
        

class HostGroup:
    def __init__(self,name,config,parent=None,prompt="Select Choice: "):
        self.name       = name
        self.members    = []
        self.parent     = parent
        self.prompt     = prompt
        self.catch_menu = False

    def add_member(self,member):
        if isinstance(member, Host) or isinstance(member, HostGroup):
            self.members.append(member)
        else:
            raise Exception("Members must be of type Host or HostGroup")
        
    def action(self):
        self.display_menu()

    def display_menu(self):
        while True:
            #clear_screen()
            try:
                # Create the display
                max_choice = 1
                write_in_color("\t" + self.name +"\n", bcolors.WARNING)
                for entry in self.members:
                    print "  " + str(max_choice) ,")" , entry.name 
                    max_choice += 1
                
                # Create a 'back' system
                if self.parent == None:
                    print "\n  0) Exit to System.\n"
                else:
                    print "\n  0) Back to %s\n" % self.parent.name
                # Handle 'back' request           
                if self.wait_for_choice(max_choice) == None:
                    if self.parent:
                        self.parent.catch_menu = True
                    if not self.catch_menu:
                        break
                self.catch_menu = False
                            
            except KeyboardInterrupt:
                quit_script("Exit requested.",0)

    def wait_for_choice(self,max_choice):
        """
            Get the users input and do their bidding
        """
        choice = raw_input(self.prompt)
        ichoice = check_int(choice,max_choice)
        if ichoice != None:
            if ichoice == 0:
                return None
            else:
                self.members[ichoice-1].action()
                return True
        else:
            valid , host_indexes , action_name = parse_menu_action(choice,self.members)
            if valid:
                # TODO - Sanity check, logging here
                write_in_color("\nRunning - " + action_name+"\n", bcolors.OKGREEN)
                for host_index in host_indexes:
                    self.members[host_index].action(action_name)
                print "\n"
                return True
            else:
                write_in_color("\nBAD CHOICE!\n",bcolors.FAIL)
                return False


def build_from_config(config,parent,yaml_config):
    """
        Takes a yaml config, and recurses over the hosts to
        replicate the groups and hosts structure.
    """
    for name , members in sorted(config.items()):
        hg = HostGroup(name,yaml_config,parent=parent)
        if isinstance(members, dict):
            build_from_config(members, hg,yaml_config)
        else:
            if not members:
                quit_script("Error in config.yaml - group '{0}' has no members".format(name), 3)
            for hostname in sorted(members):
                hg.add_member(Host(hostname,yaml_config))
        parent.add_member(hg)