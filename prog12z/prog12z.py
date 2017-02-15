# -*- coding: utf-8 -*-
"""
ucanSystec.py
Author: SMFSW
Version: 1.0
Copyright (c) 2016-2017 SMFSW

v0.1: python 2 release
v1.0: script compatible with python 2 & 3

The MIT License (MIT)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import os
# import platform
# from _winreg import *


# Paths lists where to find exe
# think about "" when spaces are in the path & special characters escaping with \
p12z_lst = ['C:\\PEMicro\\PROG12Z\\cprog12z.exe',
            '\"C:\\Program Files\\PEMicro\\cprog12z.exe\"',
            '\"C:\\Program Files (x86)\\PEMicro\\cprog12z.exe\"']


task_dict = {1: 'PROG',
             2: 'DUMP',
             3: 'QUIT'}


p12z = str()        # prog12s exe + path
task = 0            # chosen task
interface = 0       # used interface
cfg_file = str()    # cfg file name


def launch_cmd():
    """ SET PATH (LOOKING FOR RIGHT PATH IN REG) """
    global p12z

    # aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    #
    # if platform.machine().endswith('64'):
    #     aKey = OpenKey(aReg, r"SOFTWARE\Wow6432Node\PEMicro\PROG12Z")
    # else:
    #     aKey = OpenKey(aReg, r"SOFTWARE\PEMicro\PROG12Z")
    #
    # try:
    #     keyname = EnumValue(aKey, 0)
    #     if keyname[0] == 'InstallPath':
    #         p12z = keyname[1]
    #         p12z += "\\PROG12Z\\cprog12z.exe"
    #         # print(p12z)
    #         p12z += " {} Interface={} port=USB1 freq 16000000".format(cfg_file, interface)
    #         ret = os.system(p12z)
    #         print("Error {}: {}".format(ret, err_dict.get(ret)))
    # except WindowsError:
    #     print("sorry, but you should install PEmicro first!\nExiting")
    #     exit(-1)

    for i, filepath in enumerate(p12z_lst):
        if os.path.isfile(filepath):
            p12z = filepath
            p12z += " {} Interface={} port=USB1 freq 16000000".format(cfg_file, interface)
            ret = os.system(p12z)
            print("Error {}: {}".format(ret, err_dict.get(ret)))
            break   # break for when found

    if p12z == "":
        print("sorry, but you should install PEmicro first!\nExiting")


def set_task():
    """ prompt for task """
    global task, cfg_file

    print("Choose task:")
    for k, txt in task_dict.items():
        print("{}: {}".format(k, txt))
    task = int(input("$>"))
    try:
        assert task > 0
        assert task <= len(task_dict)
    except AssertionError:
        print("out of range, try again!")
    else:
        if task == 1:
            cfg_file = "cprog12w.cfg"
        elif task == 2:
            cfg_file = "crecup12w.cfg"
        elif task == 3:
            exit(0)
    finally:
        return cfg_file


def set_interface():
    """ prompt for interface """
    global interface

    print("Choose interface:")
    for k, txt in interface_dict.items():
        print("{}: {}".format(k, txt))
    tmp_interface = int(input("$>"))
    try:
        assert tmp_interface > 0
        assert tmp_interface <= len(interface_dict)
    except AssertionError:
        print("out of range, try again!")
    else:
        if tmp_interface == 5:
            exit(0)
        interface = interface_dict.get(tmp_interface)
    finally:
        return interface


def hash_check():
    """ Checking files integrity with fsum """
    try:
        size_sfv = os.stat("s19.sfv")
        if size_sfv.st_size != 0:
            command = "fsum.exe -c -js -s s19.sfv"
            ret = os.system(command)
            if ret == 1:
                print("s19 file(s) corrupted.\nExit")
                exit(-1)
        else:
            print("s19.sfv file empty.\nContinue without hash check...")
            pass
    except:
        print("fsum.exe not found!\nContinue without hash check...")


err_dict = {0: "Program completed with no errors.\nFLASHING IS DONE!!!",
            1: "Cancelled by user",
            2: "Error reading S record file",
            3: "Verify error",
            4: "Verify cancelled by user",
            5: "S record file is not selected",
            6: "Starting address is not in module",
            7: "Ending address is not in module or is less than starting address",
            8: "Unable to open file for uploading",
            9: "File write during upload",
            10: "Upload cancelled by user",
            11: "Error opening .12P file",
            12: "Error reading .12P file",
            13: "Device did not initialize",
            14: "Error loading .12P file",
            15: "Error enabling module just selected",
            16: "Specified S record file not found",
            17: "Insufficient buffer space specified by .12P to hold a file S record",
            18: "Error during programming",
            19: "Start address does not point into module",
            20: "Error during last byte programming",
            21: "Programming address no longer in module",
            22: "Start address is not on an aligned word boundary",
            23: "Error during last word programming",
            24: "Module could not be erased",
            25: "Module word not erased",
            26: "Selected .12P file does not implement byte checking",
            27: "Module byte not erased",
            28: "Word erase starting address must be even",
            29: "Word erase ending address must be even",
            30: "User parameter is not in the range",
            31: "Error during .12P specified function",
            32: "Specified parallel printer port is not available",
            33: "Command is inactive for this .12P file",
            34: "Cannot enter background mode. Check connnections",
            35: "Not able to access processor. Try a software reset",
            36: "Invalid .12P file",
            37: "Not able to access processor RAM. Try a software reset",
            38: "Initialization cancelled by user",
            39: "Error converting hexadecimal command number",
            40: "Configuration file not specified and file prog.cfg does not exist",
            41: ".12P file does not exist",
            42: "Error in io_delay number on command line",
            43: "Can not talk to cable",
            44: "Error specifying decimal delay in milliseconds",
            45: "Can not talk to cable",
            46: "Unknown error",
            47: "Error in script file",
            48: "Unknown error",
            49: "Cable not detected",
            50: "S-Record file does not contain valid data",
            51: "Checksum Verification failure - S-record data does not match MCU memory",
            52: "Sorting must be enabled to verify flash checksum",
            53: "S-Records not all in range of module (see \"v\" commandline parameter)",
            54: "Error detecting in settings on commandline for port/interface"}


interface_dict = {1: 'CYCLONEPRO',
                  2: 'USBMULTILINK',
                  3: 'BDMMULTILINK',
                  4: 'CABLE12',
                  5: 'QUIT'}


if __name__ == "__main__":
    while cfg_file == "":
        set_task()
    while interface == 0:
        set_interface()
    hash_check()
    launch_cmd()
    os.system("PAUSE")
