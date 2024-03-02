#!/usr/bin/env python

#-----------------------------------------------------------------------
# testreg.py
# Author: Roger Weng, Vishva Ilavelan
#-----------------------------------------------------------------------

import os
import sys
import sqlite3
import contextlib
import socket
import pickle


DATABASE_URL = 'file:reg.sqlite?mode=rw'

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def exec_command(program, args):
    print_flush('---------------------------------------------')
    command = 'python ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

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
            print("hit")
            return search_results
          
     except Exception as ex: 
            print(ex)





def main():

    

    print("yo")

    host = sys.argv[1]
    port = sys.argv[2]

    print(connect_server(host, port, ['get_overviews', {'dept':'COS', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'COS', 'coursenum':'2', 'area':'qr', 'title':'intro'}]))

    # Add more tests here.
    
    # Boundary and Coverage Testing
    
    # test given by class


    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'333', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'COS', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'b', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'Qr', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'intro'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'science'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'c%S'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'c_S'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'c\%S'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'cos', 'coursenum':'3', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'"Independent Study"'}]))
    
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'"Independent Study "'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'"Independent Study  "'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'" Independent Study"'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'"  Independent Study"'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'=-c'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'-casjej3rigjwjregpw3trgjq3ejigj3qrjgirgjq3riogjkkm3prjgiqfjdgqrkgjqreigjpweqrjgqperjgpiqerjgqiwrepgipeqrgjfmvpqriemgfpqkermgrg'}]))




 



    

    # boundary cases

    # test injection attack

    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':"junk' OR 'x'='x"}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':"junk' OR 'x'='x", 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':"junk' OR 'x'='x", 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':"junk' OR 'x'='x", 'coursenum':'', 'area':'', 'title':''}]))
  
    # testing on small inputs
    





    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':' ', 'coursenum':' ', 'area':' ', 'title':' '}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'S', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'c', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'p'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'0', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'m', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'""', 'coursenum':'"', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'"', 'title':''}]))
   
   

    # testing where all flags are used with input

    print(connect_server(host, port, ['get_overviews', {'dept':'e', 'coursenum':'21', 'area':'sa', 'title':'the'}]))

  
    # test each search parameter / flag individually
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'systems'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'qr', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'phy', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'104', 'area':'', 'title':''}]))
   

    # test with unusual parameters
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'-'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'""&;'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'&'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'?'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'%%%%"____-%%%%__"'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'%_%_%_%%%%%%___%%_%__%'}]))
    
    print(connect_server(host, port, ['get_overviews', {'dept':'%', 'coursenum':'_', 'area':'', 'title':''}]))

 


    # testing multiple command lines arguments with multiple 
   #  of the same type of command line type
  


    # full search
    print(connect_server(host, port, ['get_overviews', {'dept':'FRS', 'coursenum':'178', 'area':'SA', 'title':'Modern Financial Markets'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'WWS', 'coursenum':'556b', 'area':'', 'title':'Topics in International Relations: International Justice'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'ORF', 'coursenum':'527', 'area':'', 'title':'Stochastic Calculus and Finance'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'MAT', 'coursenum':'203', 'area':'QR', 'title':'Advanced Multivariable Calculus'}]))
  


    # test corner cases associated with escaping
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'\\casf\\l\\jkwefj \\eere'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'\\""'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'t\h\e'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'t\\h\\e'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'t\\\h\\\e'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'t\\\\h\\\\e"'}]))

    print(connect_server(host, port, ['get_overviews', {'dept':'COS', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'1', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'QR', 'title':''}]))

    
    print(connect_server(host, port, ['get_overviews', {'dept':'c', 'coursenum':'2', 'area':'h', 'title':'h'}]))
    
    # one each
    print(connect_server(host, port, ['get_overviews', {'dept':'MAT', 'coursenum':'', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'10', 'area':'', 'title':''}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'-'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'a', 'coursenum':'', 'area':'', 'title':'t'}]))
    print(connect_server(host, port, ['get_overviews', {'dept':'his', 'coursenum':'0', 'area':'', 'title':'roman'}]))
    
     


       
    

    # test database corruption 

    # drop courses table
    corruption_helper("courses ")

    # test how responds to missing table
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'QR', 'title':''}]))
    

    # restore table but with a missing coloumn. 
    restore_table("CREATE TABLE courses (courseid INTEGER DEFAULT NULL, area TEXT DEFAULT NULL, descrip TEXT DEFAULT NULL, prereqs TEXT DEFAULT NULL) ")

    # test response to a missing coloumn
    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':'the'}]))


    # test response to another dropped table 

    corruption_helper("crosslistings ")

    print(connect_server(host, port, ['get_overviews', {'dept':'cos', 'coursenum':'', 'area':'', 'title':''}]))

    # test response with a missing coloumn
    restore_table("CREATE TABLE crosslistings (courseid INTEGER DEFAULT NULL, coursenum TEXT DEFAULT NULL) ")

    print(connect_server(host, port, ['get_overviews', {'dept':'phy', 'coursenum':'', 'area':'', 'title':''}]))



    corruption_helper("classes ")

    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'SA', 'title':''}]))


    restore_table("CREATE TABLE classes (classid INTEGER DEFAULT NULL, courseid INTEGER DEFAULT NULL, days TEXT DEFAULT NULL, starttime TEXT DEFAULT NULL, endtime TEXT DEFAULT NULL) ")

    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'SA', 'title':''}]))

    corruption_helper("classes ")
    corruption_helper("crosslistings ")
 

    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':''}]))

    corruption_helper("profs ")
    corruption_helper("coursesprofs ")
    corruption_helper("courses ")

    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':''}]))
  

    os.system("rm -f reg.sqlite")

    print(connect_server(host, port, ['get_overviews', {'dept':'', 'coursenum':'', 'area':'', 'title':''}]))

    os.system("cp /u/cos333/Asgt1Solution/reg.sqlite .")

    

   
    
    

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()