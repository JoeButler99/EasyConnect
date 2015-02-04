import sys
import os


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



def check_int(choice,max_choice):
    try:
        c = int(choice)
        if c >= 0 and c <= max_choice:
            return c
        else:
            return None
    except:
        return None