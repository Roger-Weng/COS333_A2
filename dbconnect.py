#-----------------------------------------------------------------------
# database.py
# Authors: Roger Weng, Vishva Ilavelan
#-----------------------------------------------------------------------


import sqlite3
import contextlib
import sys

#-----------------------------------------------------------------------
# URL for database file
DATABASE_URL = 'file:reg.sqlite?mode=ro'

# search for specific classes with certain constraints
def search(dept_input, num_input, area_input, title_input):

    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT classid, dept, "
                stmt_str += "coursenum, area, title "
                stmt_str += "FROM courses, crosslistings, classes "
                stmt_str += "WHERE classes.courseid = courses.courseid "
                stmt_str += "AND crosslistings.courseid "
                stmt_str += "= courses.courseid "
                stmt_str += "AND dept LIKE ? ESCAPE '\\' "
                stmt_str += "AND coursenum LIKE ? ESCAPE '\\' "
                stmt_str += "AND area LIKE ? ESCAPE '\\' "
                stmt_str += "AND title LIKE ? ESCAPE '\\' "

                # add more AND statements here for all fields
                stmt_str += "ORDER BY dept, coursenum, classid "
                cursor.execute(stmt_str, [f"%{dept_input}%",
                                          f"%{num_input}%",
                                          f"%{area_input}%",
                                          f"%{title_input}%"])
                table = cursor.fetchall()
                
                return_list = []
                return_list.append(True)

                classes_list = []
                
                for row in table:
                    classid, dept, coursenum, area, title = row

                    classDict = {"classid": classid, "dept": dept, 
                                 "coursenum": coursenum, 
                                 "area": area, "title": title}
                    classes_list.append(classDict)

                return_list.append(classes_list)
                return return_list

    except Exception as ex:
        return_list = []
        return_list.append(False)
        return_list.append(ex)

        print(sys.argv[0] + ":", ex, file=sys.stderr)
  
        return return_list





def get_class_details(classid_input): 

    try:
    
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:

                print("enter hit")
                stmt_str = "SELECT courseid, days, starttime, "
                stmt_str += "endtime, bldg, roomnum "
                stmt_str += "FROM classes WHERE classid = ? "

                cursor.execute(stmt_str, [classid_input])
                class_table = cursor.fetchall()

                row = class_table[0]
                course_id, days, start_time = row[0], row[1], row[2]
                end_time, bldg, room_num = row[3], row[4], row[5]

                stmt_str = "SELECT area, title, descrip, prereqs "
                stmt_str += "FROM courses WHERE courseid = ? "
                cursor.execute(stmt_str, [course_id])
                course_table = cursor.fetchall()

                row = course_table[0]
                area, title = row[0], row[1]
                descrip, prereqs = row[2], row[3]


                stmt_str = "SELECT dept, coursenum "
                stmt_str += "FROM crosslistings WHERE courseid = ? "
                stmt_str += "ORDER BY dept, coursenum "
                cursor.execute(stmt_str, [course_id])
                dept_table = cursor.fetchall()


                stmt_str = "SELECT profname "
                stmt_str += "FROM coursesprofs, profs "
                stmt_str += "WHERE courseid = ? "
                stmt_str += "AND profs.profid = coursesprofs.profid "
                stmt_str += "ORDER BY profname "
                cursor.execute(stmt_str, [course_id])
                prof_table = cursor.fetchall()
                print("hit")
                deptcoursenums_list = []
                for row in dept_table:
                    deptcoursenums_list.append([row[0], row[1]])

                profs_list = []
                for row in prof_table:
                    profs_list.append(row[0])



                classDict = {"courseid": course_id, "days": days, 
                             "starttime": start_time, 
                             "endtime": end_time, 
                             "bldg": bldg, "rommnum": room_num, 
                             "deptcoursenums": deptcoursenums_list, 
                             "area": area, "title": title, "descrip": descrip, 
                             "prereqs": prereqs, "profnames": profs_list}

                

                return_list = []
                return_list.append(True)
                return_list.append(classDict)

        
                return return_list

    except Exception as ex:
        return_list = []
        return_list.append(False)
        return_list.append(ex)

        print(sys.argv[0] + ":", ex, file=sys.stderr)
  
        return return_list



  

# get information of the class given classid
def get_class_table(classid_input, arg_zero):
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT courseid, days, starttime, "
                stmt_str += "endtime, bldg, roomnum "
                stmt_str += "FROM classes WHERE classid = ? "
                cursor.execute(stmt_str, [classid_input])
                table = cursor.fetchall()
                return table

    except Exception as ex:
        print(arg_zero + ":", ex, file=sys.stderr)
  

# get information for the course given courseid
def get_course_info(course_id, arg_zero):
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT area, title, descrip, prereqs "
                stmt_str += "FROM courses WHERE courseid = ? "
                cursor.execute(stmt_str, [course_id])
                table = cursor.fetchall()
                return table

    except Exception as ex:
        print(arg_zero + ":", ex, file=sys.stderr)

# get department and course number
def get_department_num(course_id, arg_zero):
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT dept, coursenum "
                stmt_str += "FROM crosslistings WHERE courseid = ? "
                stmt_str += "ORDER BY dept, coursenum "
                cursor.execute(stmt_str, [course_id])
                table = cursor.fetchall()
                return table

    except Exception as ex:
        print(arg_zero + ":", ex, file=sys.stderr)


# get professor name
def get_profs(course_id, arg_zero):
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT profname "
                stmt_str += "FROM coursesprofs, profs "
                stmt_str += "WHERE courseid = ? "
                stmt_str += "AND profs.profid = coursesprofs.profid "
                stmt_str += "ORDER BY profname "
                cursor.execute(stmt_str, [course_id])
                table = cursor.fetchall()
                return table

    except Exception as ex:
        print(arg_zero + ":", ex, file=sys.stderr)
