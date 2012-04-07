#!/usr/bin/env python

import os
import sys
import fnmatch
import subprocess


lib_list = []

def use_cache():
    """load cache with filepath of sqlite files"""
    global lib_list
    with open('cache.list') as c_f:
        lib_list = [l.strip() for l in c_f.readlines()]

def search_lib(s_path):
    """search sqlite3 database in userpath"""
    global lib_list
    sqlstr = 'SQLite format 3'
    for path, dirs, files in os.walk(s_path):
        for file in fnmatch.filter(files,  "*"):
            fullname = path + os.sep + file
            try:
                if os.stat(fullname).st_size > 1024*1024*100:
                    continue
                with open(fullname,  encoding="latin-1") as fdesc:
                    if fdesc.read(15) == sqlstr:
                        lib_list.append(fullname)
            except UnicodeDecodeError:
                print("UnicodeDecodeError   " + path + os.sep + file)
            except OSError:
                print("Os error" + fullname)
            except IOError:
                print("io error" + fullname)

def optimize_it():
    """
    run sqlite3 for searched files with vacuum command
    """
    global lib_list
    for lib in lib_list:
        try:
            st1 = os.stat(lib)
            subprocess.check_output("sqlite3 " + lib.replace(' ',  '\ ') + " 'vacuum;reindex;'", shell = True,  stderr = subprocess.STDOUT)
            st2 = os.stat(lib)
            print(lib + ' size win = ' + str(st1.st_size - st2.st_size))
        except subprocess.CalledProcessError:
            print(lib + " CalledProcessError")

def save_cache():
    with open('cache.list',  'wt') as c_f:
        for l in lib_list:
            c_f.write(l + '\n')

if __name__ == '__main__':
    print("start")
    if len(sys.argv) > 1 and sys.argv[1] == '--cache':
        use_cache()
    else:
        search_lib("/home/cool/.config")
        search_lib("/home/cool/.mozilla")
        search_lib("/home/cool/.thunderbird")
    print(lib_list)
    optimize_it()
    save_cache()
    print("exit")
