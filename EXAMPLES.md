
Using the Menu
==============



Shell Module
============

Open a single hosts terminal
----------------------------

    ./ec -g Local::localhost -a Shell::open_ssh_terminal

Open a terminal for all hosts in a group
----------------------------------------

    ./ec -g MadeUpApp::Test -a Shell::open_ssh_terminal


Open a terminal for all hosts in sub groups
-------------------------------------------

    ./ec -g MadeUpApp -a Shell::open_ssh_terminal
