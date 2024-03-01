import argparse
import sys
import PyQt5.QtGui
import PyQt5.QtWidgets
import socket
import pickle



def input_helper():
    parser = argparse.ArgumentParser(
        description="Server for the registrar application")
    parser.add_argument('host', help="the host on which the server is running")
    parser.add_argument('port', type=int, help="the port at which the server is listening")
    args = parser.parse_args()

    return args 
  


def create_pushbutton():
    submit_button = PyQt5.QtWidgets.QPushButton("Submit:")
    return submit_button
    

def create_list_widget():
    listwidget = PyQt5.QtWidgets.QListWidget()
    listwidget.setFont(PyQt5.QtGui.QFont("Courier New", 10))
    return listwidget
    
    


def create_labels(): 
    dept_label = PyQt5.QtWidgets.QLabel("Dept:")
    dept_label.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)
    dept_label.setAutoFillBackground(True)
    dept_palette = dept_label.palette()
    dept_palette.setColor(
        dept_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)



    number_label = PyQt5.QtWidgets.QLabel("Number:")
    number_label.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)
    number_label.setAutoFillBackground(True)
    number_palette = number_label.palette()
    number_palette.setColor(
        number_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)


    
    area_label = PyQt5.QtWidgets.QLabel("Area:")
    area_label.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)
    area_label.setAutoFillBackground(True)
    area_palette = area_label.palette()
    area_palette.setColor(
        area_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)



    title_label = PyQt5.QtWidgets.QLabel("Title:")
    title_label.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)
    title_label.setAutoFillBackground(True)
    title_palette = title_label.palette()
    title_palette.setColor(
        title_label.backgroundRole(),  PyQt5.QtCore.Qt.gray) 

    
    return (dept_label, number_label, area_label, title_label)
   
    
def create_lineedits():
    dept_lineedit = PyQt5.QtWidgets.QLineEdit()
    title_lineedit = PyQt5.QtWidgets.QLineEdit()
    area_lineedit = PyQt5.QtWidgets.QLineEdit()
    number_lineedit = PyQt5.QtWidgets.QLineEdit()
    return (dept_lineedit, number_lineedit, area_lineedit, title_lineedit)
  
  
def create_control_frame(labels, lineedits, submitbutton):
    control_frame_layout = PyQt5.QtWidgets.QGridLayout()
    control_frame_layout.addWidget(labels[0], 0, 0)
    control_frame_layout.addWidget(labels[1], 1, 0)
    control_frame_layout.addWidget(labels[2], 2, 0)
    control_frame_layout.addWidget(labels[3], 3, 0)

    control_frame_layout.addWidget(lineedits[0], 0, 1)
    control_frame_layout.addWidget(lineedits[1], 1, 1)
    control_frame_layout.addWidget(lineedits[2], 2, 1)
    control_frame_layout.addWidget(lineedits[3], 3, 1)

    control_frame_layout.addWidget(submitbutton, 0, 3, 4, 1)

    
    
    control_frame = PyQt5.QtWidgets.QFrame()
    control_frame.setLayout(control_frame_layout)
    return control_frame

def create_class_list_frame(list_widget):
    list_frame_layout = PyQt5.QtWidgets.QGridLayout()
    list_frame_layout.setContentsMargins(0, 0, 0, 0)
    list_frame_layout.addWidget(list_widget, 0, 0)
    list_frame = PyQt5.QtWidgets.QFrame()
    list_frame.setLayout(list_frame_layout)
    return list_frame



def create_central_frame(control_frame, list_frame):
    central_frame_layout = PyQt5.QtWidgets.QGridLayout()
    central_frame_layout.addWidget(control_frame, 0, 0) 
    central_frame_layout.addWidget(list_frame, 1, 0)    
    central_frame = PyQt5.QtWidgets.QFrame()
    central_frame_layout.setContentsMargins(0, 0, 0, 0)
    central_frame_layout.setSpacing(0)
    central_frame.setLayout(central_frame_layout)
    return central_frame
    

def create_window(central_frame):

    window = PyQt5.QtWidgets.QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(central_frame)
    screen_size = PyQt5.QtWidgets.QDesktopWidget().screenGeometry()
    window.resize(screen_size.width()//2, screen_size.height()//2)
    return window


def handle_form_submit(lineedits, list_widget, host, port):

    

    dept_input  = lineedits[0].text()
    number_input = lineedits[1].text()
    area_input = lineedits[2].text()
    title_input = lineedits[3].text()

    communication_list = ["get_overviews", {'dept': dept_input, 
                                            "coursenum": number_input, "area": area_input,
                                            "title": title_input}]
 
    try:
        with socket.socket() as sock:
            sock.connect((host, port))
            flo = sock.makefile(mode='wb')
            pickle.dump(communication_list, flo)
            flo.flush()

            flo = sock.makefile(mode = 'rb')
            search_results = pickle.load(flo)
            search_status = search_results[0]
            results_list = search_results[1]

            

            if (search_status):
                row = 0
                list_widget.clear()
                for class_dict in results_list:
                    entry = '%5s %3s %4s %3s %-40s' % (class_dict["classid"], class_dict["dept"], 
                    class_dict["coursenum"], class_dict["area"], class_dict["title"])
                    list_widget.insertItem(row, entry)
                    row += 1
                list_widget.setCurrentRow(0)            
            else: 
                print("error")

    except Exception as ex: 
        print(ex, file=sys.stderr)

def handle_list_clicked(list_widget, host, port, window):
    class_entry = list_widget.currentItem().text()
    classid = int(class_entry[0:5])

    communication_list = ["get_detail", classid]

    try:
        with socket.socket() as sock:
            sock.connect((host, port))
            flo = sock.makefile(mode='wb')
            pickle.dump(communication_list, flo)
            flo.flush()

            flo = sock.makefile(mode = 'rb')
            search_results = pickle.load(flo)
            search_status = search_results[0]
            class_dict = search_results[1]

            

            if (search_status):
                display_string = "Course Id: " + str(class_dict["courseid"]) + "\n\n"
                display_string += "Days: " + class_dict["days"] + "\n"
                display_string += "Start time: " + class_dict["starttime"] + "\n"
                display_string += "End time: " + class_dict["endtime"] + "\n"
                display_string += "Building: " + class_dict["bldg"] + "\n"
                display_string += "Room: " + class_dict["roomnum"] + "\n\n"

                dept_nums_list = class_dict["deptcoursenums"]
                for pair in dept_nums_list:
                    display_string += "Dept and Number: " + pair[0] + " " + pair[1] + "\n"
                display_string += "\n"
                display_string += "Area: " + class_dict["area"] + "\n\n"
                display_string += "Title: " + class_dict["title"] + "\n\n"
                display_string += "Description: " + class_dict["descrip"] + "\n\n"
                display_string += "Prerequisites: " + class_dict["prereqs"] + "\n\n"
                profs = class_dict["profnames"]
                for professor in profs:
                    display_string += "Professor: " + professor + "\n"
                PyQt5.QtWidgets.QMessageBox.information(
                window, "My title", display_string)
               
            else: 
                print("error")

    except Exception as ex: 
        print(ex, file=sys.stderr)
   

def main(): 
    args = input_helper() 
    host = args.host
    port = args.port
    
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    
    # Create and lay out widgets.
    labels = create_labels()
    lineedits = create_lineedits()
    submitbutton = create_pushbutton()
    
    control_frame = create_control_frame(labels, lineedits, submitbutton)
   
    list_widget = create_list_widget()
    list_frame = create_class_list_frame(list_widget)
    central_frame = create_central_frame(control_frame, list_frame)
    window = create_window(central_frame)

    handle_form_submit(lineedits, list_widget, host, port)
    


    def helper_line_edits():
        handle_form_submit(lineedits, list_widget, host, port)
    for lineedit in lineedits: 
        lineedit.returnPressed.connect(helper_line_edits)

    def helper_push_button():
        handle_form_submit(lineedits, list_widget, host, port)
    submitbutton.clicked.connect(helper_push_button)

    def helper_list_clicked():
        handle_list_clicked(list_widget, host, port, window)
    list_widget.itemActivated.connect(helper_list_clicked)    
    
    
    
    window.show()
    sys.exit(app.exec_())
    
    

if __name__ == '__main__':
    main()