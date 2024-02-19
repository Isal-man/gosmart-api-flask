from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingEnrollment

table = "enrollments"
column = "id, created_at, is_student, is_teacher, user_id, course_id"

def findAll():
    try:
        data = []
        cursor.execute(f"select {column} from {table}")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingEnrollment(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findAllParticipant(cid):
    try:
        data = []
        cursor.execute(f"select {column} from {table} where course_id = '{cid}'")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingEnrollment(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findEnrollmentById(id):
    try:
        cursor.execute(f"select {column} from {table} where id = '{id}'")
        data = cursor.fetchone()
        return addingEnrollment(data)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findUserHasEnroll(user):
    try:
        cursor.execute(f"select {column} from {table} where user_id = '{user}'")
        data = cursor.fetchone()
        if data != None:
            return True
        return False
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def joinCourseAsStudent(data):
    try:
        id = data.get('id')    
        createdAt = data.get('createdAt')    
        userId = data.get('userId')    
        courseId = data.get('courseId')
        
        cursor.execute(f"insert into {table} ({column}) values ('{id}'::uuid, '{createdAt}', {True}, {False}, '{userId}', '{courseId}')")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def deleteStudent(uid, cid):
    try:
        cursor.execute(f"delete from {table} where user_id = '{uid}' and course_id = '{cid}'")
        conn.commit()
        return 'Success'
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'