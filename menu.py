'''
Created on 16 Jan 2014

@author: joe
'''
from functions import clear_screen,  write_in_color, bcolors, quit_script


class MenuEntry:
    def __init__(self,text,action):
        self.text   = text
        self.action = action
        
class MenuAction:
    def __init__(self,text,action,key):
        self.text   = text
        self.action = action
        self.key    = key
        
class Menu:
    def __init__(self,title,parent=None,prompt="Select Choice: "):
        self.title   = title
        self.parent  = parent
        self.entries = []
        self.actions = []
        self.prompt  = prompt
            
    def check_int(self,choice,max_choice):
        try:
            c = int(choice)
            if c >= 0 and c <= max_choice:
                return c
            else:
                return None
        except:
            return None
        
    def check_action(self,choice):
        for a in self.actions:
            if a.key == choice:
                return a
        return None
            

    def display(self):
        clear_screen()
        while True:
            try:
                write_in_color(self.title, bcolors.WARNING)
                max_choice = 1
                print
                for e in self.entries:
                    print max_choice,")" , e.text
                    max_choice += 1
                    
                if self.actions:
                    write_in_color("\nAvailable Actions", bcolors.HEADER)
                    for a in self.actions:
                        print a.key,")" , a.text
                
                if self.parent == None:
                    print "\n0) Exit to System.\n"
                else:
                    print "\n0) Back to %s\n" % self.title
                    
                # Check what kind of choice the user made
                choice = raw_input(self.prompt)
                ichoice = self.check_int(choice,max_choice)
                if ichoice != None:
                    if ichoice == 0:
                        break
                    else:
                        self.entries[ichoice-1].action()
                else:
                    achoice = self.check_action(choice)
                    if achoice:
                        achoice.action()
                    else:
                        write_in_color("\nBAD CHOICE!\n",bcolors.FAIL)
            
            except KeyboardInterrupt:
                quit_script("Exit requested.",0)




        
