import sys
import os
import inspect


class bcolors:
    """ bcolors holds the available colours for use with the bash terminal """ 
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def quit_script(msg,exitcode):
    """ Exit with a message and exitcode. The message is displayed in red."""
    msg = "\n" + msg + "\n"
    if exitcode != 0:
        print bcolors.FAIL , msg , bcolors.ENDC
    else:
        print msg
    sys.exit(exitcode)
    
    
def clear_screen():
    os.system('clear')
    
    
# (Uses a bcolor as the colour argument)
def write_in_color(msg,color):
    """ Write to stdout in a given colour. The colour should be from the bcolors class"""
    print color + str(msg) + bcolors.ENDC


class ModuleParser:
    """ 
        Module parsers reaches into the modules.py file and grabs information
        about all the classes and their methods inside.
    """
    def __init__(self):
        raw_modules = { x[0] : x[1] for x in inspect.getmembers(sys.modules['modules'], inspect.isclass)}
        self.module_info = []
        self.action_map  = {}
        for classname , classreference in sorted(raw_modules.items()):
            d = {'classreference' : classreference,
                 'classname'      : classname, 
                 'classmethods'   : []}
            for methoditem in inspect.getmembers(classreference):
                if methoditem[0][0] != "_": # skip private and other types of method
                    method_info = {'methodname' : methoditem[0],
                                   'methodreference' : methoditem[1]}
                    d['classmethods'].append(method_info)
            self.module_info.append(d)
            
        # Auto assign a character to each action. (TODO)
        # This is outside of the above loop as ultimately I'd like a better way 
        # of doing this.
        self.start_char = 97
        for module in self.module_info:
            for method in module['classmethods']:
                method['actionkey'] = chr(self.start_char)
                self.action_map[chr(self.start_char)] = {'classname'  : module['classname'],
                                                         'methodname' : method['methodname'],
                                                         'action_str' : module['classname'] + "::" + method['methodname']}
                self.start_char += 1
                    
        
    def display_all_modules(self):
        write_in_color("\nModule\t\tActions", bcolors.OKGREEN) 
        for module in self.module_info:
            write_in_color("\n"+module['classname'], bcolors.WARNING)
            for module_method in module['classmethods']:
                print "\t\t- " + module_method['methodname']
        print
        
    


def check_int(choice,max_choice):
    try:
        c = int(choice)
        if c >= 0 and c <= max_choice:
            return c
        else:
            return None
    except:
        return None


def parse_menu_action(choice_string,menu_members):
    """
            parse_menu_action needs to return
            
            valid , host_indexes , action_name
            
    """
    module_parser = ModuleParser()
    if len(choice_string) == 1:
        # One action, all hosts
        if module_parser.action_map.has_key(choice_string):
            return ( True , 
                     [x for x in range(len(menu_members))] , 
                     module_parser.action_map[choice_string]['action_str'] )
        
    print len(choice_string)
    print choice_string
    print menu_members
    
    
    
            
            