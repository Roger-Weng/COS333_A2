import argparse
import sys
import PyQt5.QtGui



def input_helper():
    parser = argparse.ArgumentParser(
        description="Server for the registrar application")
    parser.add_argument('host', help="the host on which the server is running")
    parser.add_argument('port', type=int, help="the port at which the server is listening")
    args = parser.parse_args()

    return args 



def create_labels(): 
    dept_label = PyQt5.QtWidgets.QLabel("Dept")
    dept_label.setAutoFillBackground(True)
    dept_palette = dept_label.palette()
    dept_palette.setColor(
        dept_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)



    number_label = PyQt5.QtWidgets.QLabel("Number")
    number_label.setAutoFillBackground(True)
    number_palette = number_label.palette()
    number_palette.setColor(
        number_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)


    
    area_label = PyQt5.QtWidgets.QLabel("Area")
    area_label.setAutoFillBackground(True)
    area_palette = area_label.palette()
    area_palette.setColor(
        area_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)



    title_label = PyQt5.QtWidgets.QLabel("Title")
    title_label.setAutoFillBackground(True)
    title_palette = title_label.palette()
    title_palette.setColor(
        title_label.backgroundRole(),  PyQt5.QtCore.Qt.gray)



    return (dept_label, number_label, area_label, title_label)
    
    
    


    
    
    
    
def create_lineedits():
    red_lineedit = PyQt5.QtWidgets.QLineEdit('0')
    green_lineedit = PyQt5.QtWidgets.QLineEdit('0')
    blue_lineedit = PyQt5.QtWidgets.QLineEdit('0')
    return (red_lineedit, green_lineedit, blue_lineedit)
  
  
def create_control_frame(labels, lineedits):
    control_frame_layout = PyQt5.QtWidgets.QGridLayout()
    control_frame_layout.addWidget(labels[0], 0, 0)
    control_frame_layout.addWidget(labels[1], 1, 0)
    control_frame_layout.addWidget(labels[2], 2, 0)
    control_frame_layout.addWidget(labels[3], 3, 0)

    control_frame_layout.addWidget(lineedits[0], 0, 0)
    control_frame_layout.addWidget(lineedits[1], 1, 0)
    control_frame_layout.addWidget(lineedits[2], 2, 0)
    control_frame_layout.addWidget(lineedits[3], 3, 0)

    
    
    control_frame = PyQt5.QtWidgets.QFrame()
    control_frame.setLayout(control_frame_layout)
    return control_frame




def create_central_frame(control_frame):
    central_frame_layout = PyQt5.QtWidgets.QGridLayout()
    central_frame_layout.addWidget(control_frame, 0, 0)   
    central_frame = PyQt5.QtWidgets.QFrame()
    central_frame.setLayout(central_frame_layout)
    return central_frame
    

def create_window(central_frame):

    window = PyQt5.QtWidgets.QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(central_frame)
    screen_size = PyQt5.QtWidgets.QDesktopWidget().screenGeometry()
    window.resize(screen_size.width()//2, screen_size.height()//2)
    return window


def main(): 
    args = input_helper() 
    
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    
    # Create and lay out widgets.
    labels = create_labels()
    lineedits = create_lineedits()
    
    control_frame = create_control_frame(labels, lineedits)
    central_frame = create_central_frame(control_frame)
    window = create_window(central_frame)
    
    
    window.show()
    sys.exit(app.exec_())
    
    

if __name__ == '__main__':
    main()