from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingAttachment
from Services.assignmentService import findAssignmentById
from Services.userService import findUserByIdentity
from Services.enrollmentService import findEnrollmentById

table = "attachments"
column = "id, name, url, type, created_at, is_from_teacher, is_from_student, enrollment_id, assignment_id"

def findAllAttachment():
    try:
        data = []
        cursor.execute(f"select {column} from {table}")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingAttachment(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    

def findAttachmentByAssignmentAndStatus(aid, status):
    try:
        data = []
        cursor.execute(f"select at.* from {table} at left join assignments a on a.id = at.assignment_id left join enrollments en on en.id = at.enrollment_id where at.assignment_id = '{aid}' and en.{status} = {True}")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingAttachment(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findAttachmentsByAssignmentAndUser(aid, user):
    try:
        data = []
        cursor.execute(f"select at.* from {table} at left join assignments a on a.id = at.assignment_id left join enrollments en on en.id = at.enrollment_id where at.assignment_id = '{aid}' and en.user_id = '{user}'")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingAttachment(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findAttachmentById(id):
    try:
        cursor.execute(f"select {column} from {table} where id = '{id}'")
        data = cursor.fetchone()
        return addingAttachment(data)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def uploadAttachment(data):
    id = data.get('id')
    name = data.get('name')
    url = data.get('url')
    type = data.get('type')
    createdAt = data.get('createdAt')
    isFromTeacher = data.get('isFromTeacher')
    isFromStudent = data.get('isFromStudent')
    enrollmentId = data.get('enrollmentId')
    assignmentId = data.get('assignmentId')
    user = data.get('user')
    
    userCheck = findUserByIdentity(user)
    if userCheck == 'Fail':
        return 'User not found'
    
    assignmentCheck = findAssignmentById(assignmentId)
    if assignmentCheck == 'Fail':
        return 'Assignment not found'
    
    enrollmentCheck = findEnrollmentById(enrollmentId)
    if enrollmentCheck == 'Fail':
        return 'Enrollment not found'
    
    cursor.execute(f"insert into {table} ({column}) values ('{id}'::uuid, '{name}', '{url}', '{type}', '{createdAt}', {isFromTeacher}, {isFromStudent}, '{enrollmentId}', '{assignmentId}')")
    conn.commit()
    
    return data
    
def deleteAttachment(id):
    try:
        cursor.execute(f"delete from {table} where id = '{id}'")
        conn.commit()
        return "Success"
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'