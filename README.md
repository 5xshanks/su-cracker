# su-cracker
This script has been developped under python3, it aims to launch a dictionnary attack on 'su' in order to elevate privileges either horizontally using existing acounts, or vertically using the 'root' account as a target.

# Tested on:
Kali GNU/Linux 2020.4 

# Usage:
```
python3 su-cracker.py [-h] username wordlist [threads]

positional arguments:
  username    Username to switch to, must be entered
  wordlist    Name or Path to Wordlist to use, must be entered
  threads     Number of threads to launch, recommended between [100-200], 100 by default

optional arguments:
  -h, --help  show this help message and exit
```

# POC
## with root:
![](Test_root.PNG)

## with another user:
![](Test_testuser.PNG)

# Developper:
Elaffifi Omar Badis / elaffifibadis@gmail.com

Alias: 5xshanks
