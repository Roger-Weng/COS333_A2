import argparse
import sys
import PyQt5.QtGui
import PyQt5.QtWidgets



def input_helper():
    parser = argparse.ArgumentParser(
        description="Server for the registrar application")
    parser.add_argument('host', help="the host on which the server is running")
    parser.add_argument('port', type=int, help="the port at which the server is listening")
    args = parser.parse_args()

    return args 



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
    
    
    

def create_pushbutton():
    submit_button = PyQt5.QtWidgets.QPushButton("Submit:")
    return submit_button
    

def create_list_widget():
    listwidget = PyQt5.QtWidgets.QListWidget()
    return listwidget
    
    
    
def create_lineedits():
    dept_lineedit = PyQt5.QtWidgets.QLineEdit()
    title_lineedit = PyQt5.QtWidgets.QLineEdit()
    area_lineedit = PyQt5.QtWidgets.QLineEdit()
    number_lineedit = PyQt5.QtWidgets.QLineEdit()
    return (dept_lineedit, title_lineedit, area_lineedit, number_lineedit)
  
  
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
    central_frame.setLayout(central_frame_layout)
    return central_frame
    

def create_window(central_frame):

    window = PyQt5.QtWidgets.QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(central_frame)
    screen_size = PyQt5.QtWidgets.QDesktopWidget().screenGeometry()
    window.resize(screen_size.width()//2, screen_size.height()//2)
    return window


def handle_line_edits(lineedits):
    print(lineedits[0].text())
    print(lineedits[1].text())
    print(lineedits[2].text())
    print(lineedits[3].text())

def handle_push_button(lineedits):
    print(lineedits[0].text())
    print(lineedits[1].text())
    print(lineedits[2].text())
    print(lineedits[3].text())


def main(): 
    args = input_helper() 
    
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
    


    def helper_line_edits():
        handle_line_edits(lineedits)
    for lineedit in lineedits: 
        lineedit.returnPressed.connect(helper_line_edits)

    def helper_push_button():
        handle_push_button(lineedits)
    submitbutton.clicked.connect(helper_push_button)

    
    
    window.show()
    sys.exit(app.exec_())
    
    

if __name__ == '__main__':
    main()