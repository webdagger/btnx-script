# btnx-script
Tool to automate the call of btnx. The daemon for some reason keeps shutting down
## Problem the script attempts to solve
Note, this script is an attempt to automate a program call `sudo btnx`.  
[BTNX ](https://github.com/cdobrich/btnx) (Button Extension) is a daemon that enables rerouting of mouse button events through uinput as keyboard and other mouse button combinations.]
Except the daemon keeps dying and never starts up on its own.
This script just keeps restarting the daemon whenever it acts up.
