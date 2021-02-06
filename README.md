# su-cracker
A script that performs a dictionary attack locally using su, to elevate privileges to root or other users.

################################################################################################
# SU-Cracker.py
# Developped by: Elaffifi Omar Badis
# email        : elaffifibadis@gmail.com        
################################################################################################
# This script has been developped under python3
# The aim of this script is launch a dictionnary attack on 'su' in order to elevate privileges
# either horizontally using existing acounts, or vertically using the 'root' account as a target
################################################################################################
# Tested on: Kali GNU/Linux 2020.4 
################################################################################################
# usage: python3 su-cracker.py [-h] username wordlist [threads]
#
# positional arguments: 
#   username    Username to switch to, must be entered
#   wordlist    Name or Path to Wordlist to use, must be entered
#   threads     Number of threads to launch, recommended between [100-200], 100 by default
#
# optional arguments:
# -h, --help  show this help message and exit  
################################################################################################
