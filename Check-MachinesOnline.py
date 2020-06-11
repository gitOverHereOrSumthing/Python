# -*- coding: utf-8 -*-
"""Script to monitor a list of machines to see when they come online
 
Description:
    Monitors a list of machines to see when they come online
     
Parameters:
    monitorfile: Used to pass the list of machines being monitored to the script.
    startmonitoring: Tells the script to start monitoring as soon as it starts
     
Outputs:
    File system
    On screen
 
Example:
    Python Check-MachinesOnline.py --monitorfile <path>
    Python Check-MachinesOnline.py --monitorfile <path> --startmonitoring

Notes:
    Author:     Simon Goodon
    Date:       10/06/2020
    Ticket:     N/A
    Document:   N/A
"""

#-------------------------------[Initialisations]------------------------------#
import json
import sys
import os
from os import path
import argparse
import subprocess
import platform
import time

#------------------------------------------------------------------------------#

#--------------------------------[Declarations]--------------------------------#
ScriptName = os.path.basename(__file__)  

class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

#------------------------------------------------------------------------------#

#---------------------------------[Functions]----------------------------------#
def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', current_ip_address ), shell=True, universal_newlines=True)
        if 'unreachable' in str(output):
            return False
        else:
            return True
    except Exception:
            return False

def clearScreen():
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def Menu(Machines):
    clearScreen()
    print("************MAIN MENU**************")

    choice = input("""
      1: Start Monitoring
      2: Add machine to monitor
      3: Add multiple machines to monitor
      4: Remove machine from monitoring
      5: Remove multiple machines from monitoring
      6: List machines
      Q: Quit/Log Out

    Please enter your choice: """)

    if choice == "1" :
        startMonitorCheck(Machines)
    elif choice == "2":
        AddMachine(Machines)
    elif choice == "3":
        AddMachines(Machines)
    elif choice == "4":
        RemoveMachine(Machines)
    elif choice == "5":
        RemoveMachines(Machines)
    elif choice == "6":
        ListMachines(Machines)
    elif choice=="Q" or choice=="q":
        clearScreen()
        sys.exit
    else:
        Menu(Machines)

def startMonitorCheck(Machines):
    try:
        #Used to tract the status of the machines
        MachineDict = {}

        #Loading the dictionary for the first run
        for Machine in Machines:
            MachineDict[Machine] = "checking..."
        
        #Starting infinite loop until cntl-c is pressed
        while True:
            #Calling the function to ping the machines and to return the updated MachineDict
            MachineDict = processMachines(MachineDict,Machines)
            time.sleep(20)
    except KeyboardInterrupt:
        Menu(Machines)

def processMachines(MachineDict,Machines):
    #Refreshing the screen
    printMonitoringOutput(MachineDict,Machines)
    for Machine in Machines:
        if ping_ip(Machine):
            MachineDict[Machine] = "online"
        else:
            MachineDict[Machine] = "offline"
        #Refreshing the screen
        printMonitoringOutput(MachineDict,Machines)
    return MachineDict


def printMonitoringOutput(MachineDict,Machines):
    clearScreen()
    print("************ Monitoring **************")
    print()
    for MachineItem in MachineDict:
        if MachineDict[MachineItem] == "online":
            print(f"{bcolors.GREEN}{MachineItem} is online. Reason for monitoring: {Machines[MachineItem]}{bcolors.ENDC}")
        elif MachineDict[MachineItem] == "offline":
            print(MachineItem + " is " + MachineDict[MachineItem])
        else:
            print(MachineItem + " is " + MachineDict[MachineItem])

    print()
    print("Press Cntl-C to return to menu")

def AddMachine(Machines):
    MachineName = input("Enter machine name to add: ")
    MonitorReason = input("Enter the reason for monitoring: ")

    if MachineName not in Machines:
        Machines[MachineName] = MonitorReason
    
    SaveMonitorFile(Machines)
    Menu(Machines)

def AddMachines(Machines):
    MachineList = input("Enter machines (comma seperated) to add: ").split(",")
    MonitorReason = input("Enter the reason for monitoring: ")

    for MachineName in MachineList:
        if MachineName not in Machines:
            Machines[MachineName] = MonitorReason
    
    SaveMonitorFile(Machines)
    Menu(Machines)

def RemoveMachine(Machines):
    MachineName = input("Enter machine name to remove: ")

    if MachineName in Machines:
        Machines.pop(MachineName)

    SaveMonitorFile(Machines)  
    Menu(Machines)

def RemoveMachines(Machines):
    MachineList = input("Enter machines (comma seperated) to remove: ").split(",")
    
    for MachineName in MachineList:
        if MachineName in Machines:
            Machines.pop(MachineName)

    SaveMonitorFile(Machines)  
    Menu(Machines)

def ListMachines(Machines):
    clearScreen()
    print("************ Machines **************")
    print()

    for MachineName in Machines:
        print(MachineName + " - " + Machines[MachineName])

    print()
    input("Press any key to return to main menu...")  
    Menu(Machines)

def SaveMonitorFile(Machines):
    try:
        f = open(monitorfile, 'w')
        print(Machines)
        json.dump(Machines, f)
    except Exception as err:
        print("Error saving machine list to " + monitorfile + ". Error reads " + str(err))

#------------------------------------------------------------------------------#
 
#---------------------------------[Main Logic]---------------------------------#

def main():
    # Getting command line arguments from the script
    parser = argparse.ArgumentParser(description='Monitors a list of machines to see when they come online')
    parser.add_argument('--monitorfile', type=str, default="", help='Used to pass the list of machines being monitored to the script')
    parser.add_argument('--startmonitoring', action="store_true", default=False ,help='Tells the script to start monitoring as soon as it starts')
    args = parser.parse_args()

    global monitorfile
    monitorfile = args.monitorfile

    # Creating an empty dictionary for the machines to be stored in.
    Machines = {}

    try:
        if path.exists(monitorfile):
                f = open(monitorfile,"r")
                Machines = json.load(f)
    except Exception as err:
        print("Error loading machine list from " + monitorfile + ". Error reads " + str(err))

    if args.startmonitoring:
        if len(Machines) > 0:
            startMonitorCheck(Machines)
        else:
            Menu(Machines)
    else:
        Menu(Machines)

if __name__ == '__main__':
    main()
#------------------------------------------------------------------------------#