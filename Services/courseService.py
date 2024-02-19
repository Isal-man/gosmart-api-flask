from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingCourse
import uuid

tableCourse = "courses"
columnJoinCourse = "c.id, c.name, c.schedule, c.theme, c.image, c.is_archived, c.user_id, c.created_at"
columnCourse = "id, name, schedule, theme, image, is_archived, user_id, created_at"
tableEnrollment = "enrollments"
columnJoinEnrollment = "e.id, e.is_teacher, e.is_student, e.user_id, e.course_id"
columnEnrollment = "id, is_teacher, is_student, user_id, course_id"

def findAllCourses(userId):
    try:
        data = []
        cursor.execute(f"select {columnJoinCourse} from {tableCourse} c where c.user_id = '{userId}' and c.is_archived = {False}")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingCourse(x))
        return data
    except Exception as e:
        print(e)
        conn.rollback()
        return "Fail"
    
def findCourseById(userId, id):
    try:
        cursor.execute(f"select {columnJoinCourse} from {tableCourse} c where c.user_id = '{userId}' and c.id = '{id}' and c.is_archived = {False}")
        data = cursor.fetchone()
        return addingCourse(data)   
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"
    
def findCourseByCode(code):
    try:
        cursor.execute(f"select {columnJoinCourse} from {tableCourse} c where c.id::varchar like '%{code}%' and c.is_archived = {False}")
        data = cursor.fetchone()
        return addingCourse(data)   
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"
    
def findCourseAsTeacher(user):
    try:
        data = []
        cursor.execute(f"select {columnJoinCourse} from {tableCourse} c join {tableEnrollment} e on c.course_id = e.course_id where e.user_id = {user} and e.is_teacher = {True} ")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingCourse(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findCourseAsStudent(user):
    try:
        data = []
        cursor.execute(f"select {columnJoinCourse} from {tableCourse} c join {tableEnrollment} e on c.course_id = e.course_id where e.user_id = {user} and e.is_student = {True} ")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingCourse(x))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def insertCourse(data):
    try:
        id = data['id']
        name = data['name']
        schedule = data['schedule']
        theme = data['theme']
        image = data['image']
        isArchived = data['isArchived']
        userId = data['userId']
        createdAt = data['createdAt']
        enrollmentId = str(uuid.uuid4())
        cursor.execute(f"insert into {tableCourse} ({columnCourse}) values ('{id}'::uuid, '{name}', '{schedule}', '{theme}', '{image}', '{isArchived}', '{userId}', '{createdAt}')")
        cursor.execute(f"insert into {tableEnrollment} ({columnEnrollment}) values ('{enrollmentId}'::uuid, {True}, {False}, '{userId}', '{id}'::uuid)")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"
    
def updateCourse(data, id):
    try:
        name = data['name']
        schedule = data['schedule']
        theme = data['theme']
        image = data['image']
        isArchived = data['isArchived']
        userId = data['userId']
        cursor.execute(f"update {tableCourse} set name = '{name}', schedule = '{schedule}', theme = '{theme}', image = '{image}', is_archived = {isArchived}, user_id = '{userId}' where id = '{id}'")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"
    
def deleteCourse(userId, id):
    try:
        cursor.execute(f"delete from {tableCourse} where id = '{id}' and user_id = '{userId}'")
        cursor.execute(f"delete from {tableEnrollment} where course_id = '{id}'")
        conn.commit()
        return "Success"
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"