import argparse
import socket
import pickle
import os
import sys
import dbconnect

def escape_special_characters(string):
    return string.replace('_', '\\_').replace('%', '\\%')

def handle_get_details(query_object):
    classid = query_object.get[1]
    return_obj = dbconnect.get_class_details(classid)
    return return_obj

def handle_get_overviews(query_object):
    

    dept_name = escape_special_characters(query_object.get["dept"]
                                          if query_object.get["dept"]
                                          is not None else "")
    num_value = escape_special_characters(query_object.get["coursenum"]
                                          if query_object.get["coursenum"]
                                          is not None else "")
    area_name = escape_special_characters(query_object.get["area"]
                                          if query_object.get["area"]
                                          is not None else "")
    title_name = escape_special_characters(query_object.get["title"]
                                           if query_object.get["title"]
                                           is not None else "")

    return_obj = dbconnect.search(dept_name, num_value, area_name, title_name)    

    return return_obj
  



def input_helper():
    parser = argparse.ArgumentParser(
        description="Server for the registrar application")
    parser.add_argument('port', type=int, help="the port at which the server should listen")
    args = parser.parse_args()

    return args.port    
    

def main():
    try:
        port  = input_helper()
        server_sock = socket.socket()
        print('Opened server socket')
        if os.name != 'nt':
            server_sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        print("Bound server socket to port")
        server_sock.listen()
        print("Listening")

        while True:
            try:
                sock, _ = server_sock.accept()
        
                with sock:
                    print("Accepted connection, opened socket")
                    flo = sock.makefile(mode = 'rb')
                    query_object = pickle.load(flo)
                    print("Recieved command:", query_object[0])

                    if query_object == 'get_overviews':
                        return_obj = handle_get_overviews(query_object)
                        print(return_obj)

                    if query_object == 'get_details': 
                        return_obj = handle_get_details(query_object)

                    flo = sock.makefile(mode='wb')
                    pickle.dump(return_obj, flo)
                    flo.flush()

            except Exception as ex:
                print(ex, file = sys.stderr)
       
    except Exception as ex:
        # error in initializing server, can kill hte program
        print(ex, file = sys.stderr)
        sys.exit(1)
        

if __name__ == '__main__':
    main()