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






    print(connect_server(host, port, ["get_detail", 8000]))
    print(connect_server(host, port, ["get_detail", 1]))
    print(connect_server(host, port, ["get_detail", 394929138498230498091283409810329480912830981203948091238409128340981298798797987987987987656565093475098324583042958094802193840]))
    print(connect_server(host, port, ["get_detail", "asdjfkljlkj324jk234000"]))
    print(connect_server(host, port, ["get_detail", "q23ksdf 0001 "]))






    # test how responds to missing tables / database corruption

    corruption_helper("profs ")

    print(connect_server(host, port, ["get_detail", 10109]))

    restore_table("CREATE TABLE profs (profid INTEGER DEFAULT NULL, profname TEXT DEFAULT NULL) ")

    corruption_helper("coursesprofs ")

    print(connect_server(host, port, ["get_detail", 10109]))


    restore_table("CREATE TABLE coursesprofs (courseid INTEGER DEFAULT NULL, profid INTEGER DEFAULT NULL) ")



    print(connect_server(host, port, ["get_detail", 10109]))


    corruption_helper("crosslistings ")

    print(connect_server(host, port, ["get_detail", 10109]))

    restore_table("CREATE TABLE crosslistings (courseid INTEGER DEFAULT NULL, dept TEXT DEFAULT NULL, coursenum TEXT DEFAULT NULL) ")

    corruption_helper("profs ")
    corruption_helper("coursesprofs ")

    print(connect_server(host, port, ["get_detail", 10109]))

    corruption_helper("crosslistings")

    print(connect_server(host, port, ["get_detail", 10109]))



    print(connect_server(host, port, ["get_detail", 10109]))


    restore_table("CREATE TABLE crosslistings (courseid INTEGER DEFAULT NULL, dept TEXT DEFAULT NULL, coursenum TEXT DEFAULT NULL) ")

    restore_table("CREATE TABLE profs (profid INTEGER DEFAULT NULL, profname TEXT DEFAULT NULL) ")
    restore_table("CREATE TABLE coursesprofs (courseid INTEGER DEFAULT NULL, profid INTEGER DEFAULT NULL) ")

    corruption_helper("profs ")
    restore_table("CREATE TABLE profs (profid INTEGER DEFAULT NULL) ")
    print(connect_server(host, port, ["get_detail", 10109]))

    corruption_helper("profs ")
    restore_table("CREATE TABLE profs (profid INTEGER DEFAULT NULL, profname TEXT DEFAULT NULL) ")

    corruption_helper("coursesprofs ")
    restore_table("CREATE TABLE coursesprofs (courseid INTEGER DEFAULT NULL) ")
    print(connect_server(host, port, ["get_detail", 10109]))

    corruption_helper("coursesprofs ")
    restore_table("CREATE TABLE coursesprofs (courseid INTEGER DEFAULT NULL, profid INTEGER DEFAULT NULL) ")

    corruption_helper("courses ")
    restore_table("CREATE TABLE courses (courseid INTEGER DEFAULT NULL, area TEXT DEFAULT NULL, title TEXT DEFAULT NULL) ")
    print(connect_server(host, port, ["get_detail", 10109]))

    corruption_helper("crosslistings ")
    restore_table(("CREATE TABLE crosslistings (courseid INTEGER DEFAULT NULL, dept TEXT DEFAULT NULL) "))

    print(connect_server(host, port, ["get_detail", 10109]))

    corruption_helper("coursesprofs ")
    restore_table("CREATE TABLE coursesprofs (courseid INTEGER DEFAULT NULL) ")

    print(connect_server(host, port, ["get_detail", 10109]))

    corruption_helper("coursesprofs ")
    restore_table("CREATE TABLE coursesprofs (courseid INTEGER DEFAULT NULL, profid INTEGER DEFAULT NULL) ")

    corruption_helper("coursesprofs ")
    corruption_helper("profs ")
    corruption_helper("crosslistings ")
    corruption_helper("courses ")

    print(connect_server(host, port, ["get_detail", 10109]))


    corruption_helper("classes ")

    print(connect_server(host, port, ["get_detail", 10109]))

    restore_table("CREATE TABLE classes (classid INTEGER DEFAULT NULL, courseid INTEGER DEFAULT NULL, days TEXT DEFAULT NULL, starttime TEXT DEFAULT NULL, endtime TEXT DEFAULT NULL, bldg TEXT DEFAULT NULL,  roomnum TEXT DEFAULT NULL) ")

    print(connect_server(host, port, ["get_detail", 10109]))

    os.system("rm -f reg.sqlite")
    print(connect_server(host, port, ["get_detail", 10109]))


    # Add more tests here.

if __name__ == '__main__':
    main()