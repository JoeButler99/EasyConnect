About
=====

EasyConnect is a tidy up of a personal CLI toolkit I've used over the years. It's there to assist with connecting to or performing ad hoc actions against a set of hosts. 
The original worked with just a menu system, but I'm making all the features available from CLI calls with arguments so it will be script friendly. 


Setup
=====

 Clone the repo and run 'pip install -r requirements.txt'. You may want to do this from a virtualenv, however I'm aiming to keep the requirements list very small, so its not going to install a ton of dependencies if you install it systemwide.

 


Configuration
=============

See config.yaml.example for a working sample config. You could copy this 

    cp config.yaml.example config.yaml

and then open config.yaml with your favourite text editor to add your machines.


Running
=======

    ./ec      # Start EasyConnect in menu mode
    ./ec -h   # Get Help on the CLI argument options
    ./ec -l   # List the available actions to perform on hosts




Tips
====

 * Add the EasyConnect directory to your path and it can run anywhere with just 'ec'
