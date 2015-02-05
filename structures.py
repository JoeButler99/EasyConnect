import inspect
import sys
from functions import clear_screen,  write_in_color, bcolors, quit_script, check_int
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
            action_name = self.config.get_section('config')['default_host_action']
            
        parts = action_name.split("::")
        if len(parts) != 2:
            raise Exception("Error with default_host_action in config. See config.yaml.example for a working example")
        else:
            classname , methodname = parts
        if classname not in available_modules.keys():
            raise Exception
        
        # Create a class instance and check the method exists.
        # then run the bastard...
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
#         else:
#             achoice = self.check_action(choice)
#             if achoice:
#                 achoice.action()
#             else:
#                 write_in_color("\nBAD CHOICE!\n",bcolors.FAIL)


def build_from_config(config,parent,yaml_config):
    """
        Takes a yaml config, and recurses over the hosts to
        replicate the groups and hosts structure.
    """
    for name , members in config.iteritems():
        hg = HostGroup(name,yaml_config,parent=parent)
        if isinstance(members, dict):
            build_from_config(members, hg,yaml_config)
        else:
            for hostname in members:
                hg.add_member(Host(hostname,yaml_config))
        parent.add_member(hg)