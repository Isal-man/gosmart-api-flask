from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingGrade
from Services.assignmentService import findAssignmentById
from Services.userService import findUserByIdentity
from Services.courseService import findCourseById

table = "grades"
column = "id, grade, created_at, user_id, assignment_id, course_id"

def findAllGrade():
    try:
        data = []
        cursor.execute(f"select {column} from {table}")
        datas = cursor.fetchall()
        for x in datas:
            print(x)
            data.append(addingGrade(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findAllByUser(user):
    try:
        data = []
        cursor.execute(f"select {column} from {table} where user_id = '{user}'")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingGrade(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'

def findAllByAssignment(aid):
    try:
        data = []
        cursor.execute(f"select {column} from {table} where assignment_id = '{aid}'")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingGrade(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findGradeById(id):
    try:
        cursor.execute(f"select {column} from {table} where id = '{id}'")
        data = cursor.fetchone()
        return addingGrade(data)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'    
    
def findGradeByUserAndAssignment(user, aid):
    try:
        cursor.execute(f"select {column} from {table} where user_id = '{user}' and assignment_id = '{aid}'")
        data = cursor.fetchone()
        return addingGrade(data)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def countByAssignment(aid):
    try:
        cursor.execute(f"select count(*) from {table} where assignment_id = '{aid}'")
        data = cursor.fetchone()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def insertGrade(data, teacher):
    try:
        id = data.get('id')
        grade = data.get('grade')
        createdAt = data.get('createdAt')
        userId = data.get('userId')
        assignmentId = data.get('assignmentId')
        courseId = data.get('courseId')
        
        userCheck = findUserByIdentity(userId)
        if userCheck == 'Fail':
            return 'User not found'

        assignmentCheck = findAssignmentById(assignmentId)
        if assignmentCheck == 'Fail':
            return 'Assignment not found'

        courseCheck = findCourseById(teacher, courseId)
        if courseCheck == 'Fail':
            return 'Course not found'
        
        cursor.execute(f"insert into {table} ({column}) values ('{id}'::uuid, {grade}, '{createdAt}', '{userId}', '{assignmentId}', '{courseId}')")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def updateGrade(data, teacher):
    try:
        id = data.get('id')
        grade = data.get('grade')
        userId = data.get('userId')
        assignmentId = data.get('assignmentId')
        courseId = data.get('courseId')
        
        userCheck = findUserByIdentity(userId)
        if userCheck == 'Fail':
            return 'User not found'

        assignmentCheck = findAssignmentById(assignmentId)
        if assignmentCheck == 'Fail':
            return 'Assignment not found'

        courseCheck = findCourseById(teacher, courseId)
        if courseCheck == 'Fail':
            return 'Course not found'
        
        cursor.execute(f"update {table} set grade = {grade}, user_id = '{userId}', assignment_id = '{assignmentId}', course_id = '{courseId}' where id = '{id}'")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'