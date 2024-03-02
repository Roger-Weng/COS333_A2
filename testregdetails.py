#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
# Author: Roger Weng, Vishva Ilavelan
#-----------------------------------------------------------------------

import os
import sys
import contextlib
import sqlite3
import socket
import pickle

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def getclassids(): 
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT classid "
                stmt_str += "FROM classes "
                cursor.execute(stmt_str)
                table = cursor.fetchall()
                return table      
            
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def corruption_helper(table_name):
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "DROP TABLE " + table_name
                cursor.execute(stmt_str)

    except Exception as ex:
        print(ex)
        sys.exit(1)

def restore_table(command):
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = command
                cursor.execute(stmt_str)

    except Exception as ex:
        print(ex)
        sys.exit(1) 

def connect_server(host, port, comm_message):      
     try:
        with socket.socket() as sock:
            sock.connect((host, port))
            flo = sock.makefile(mode='wb')
            pickle.dump(comm_message, flo)
            flo.flush()

            flo = sock.makefile(mode = 'rb')
            search_results = pickle.load(flo)
            return search_results
          
     except Exception as ex: 
            print(ex)
     

#-----------------------------------------------------------------------

def print_flush(message): 
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def main(): 



    host = sys.argv[1]
    port = int(sys.argv[2])

    table = getclassids()

    


    # make sure help command is formatted correct

    
    
    

    print(connect_server(host, port, ["get_detail", 10109]))

    os.system("rm -f reg.sqlite")

    print(connect_server(host, port, ["get_detail", 10109]))
    print(connect_server(host, port, ["get_detail", 10109]))
    print(connect_server(host, port, ["get_detail", 10109]))
    print(connect_server(host, port, ["get_detail", 10109]))
    print(connect_server(host, port, ["get_detail", 10109]))
    print(connect_server(host, port, ["get_detail", 10109]))
    print(connect_server(host, port, ["get_detail", 10109]))
   
    os.system("cp /u/cos333/Asgt2Solution/reg.sqlite .")


    # Add more tests here.

if __name__ == '__main__':
    main()