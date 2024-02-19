from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingAssignment

table = 'assignments'
column = 'id, name, post_date, created_at, is_material, is_task, is_announcment, course_id'

def findAllAssignment():
    try:
        data = []
        cursor.execute(f"select {column}, due_date from {table}")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingAssignment(x, False))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findAssignmentByCourse(cid):
    try:
        data = []
        cursor.execute(f"select {column}, due_date from {table} where course_id = '{cid}'")
        datas = cursor.fetchall()
        for x in datas:
            data.append(addingAssignment(x, False))
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def findAssignmentById(id):
    try:
        cursor.execute(f"select {column}, due_date, description from {table} where id = '{id}'")
        data = cursor.fetchone()
        print('data :', data)
        return addingAssignment(data, True)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def insertAssignment(data):
    try:
        id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        dueDate = data.get('dueDate')
        postDate = data.get('postDate')
        createdAt = data.get('createdAt')
        isMaterial = data.get('isMaterial')
        isAnnouncment = data.get('isAnnouncment')
        isTask = data.get('isTask')
        courseId = data.get('courseId')
        cursor.execute(f"insert into {table} ({column}, description {',due_Date' if dueDate != None else ''}) values ('{id}'::uuid, '{name}', '{postDate}', '{createdAt}', {isMaterial}, {isTask}, {isAnnouncment}, '{courseId}', '{description}' {f',{dueDate}' if dueDate != None else ''})")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def updateAssignment(data, id):
    try:
        name = data.get('name')
        description = data.get('description')
        dueDate = data.get('dueDate')
        postDate = data.get('postDate')
        isMaterial = data.get('isMaterial')
        isAnnouncment = data.get('isAnnouncment')
        isTask = data.get('isTask')
        courseId = data.get('courseId')
        cursor.execute(f"update {table} set name = '{name}', {f"description = '{description}'," if description != None else ''} post_date = '{postDate}', {f"due_date = '{dueDate}'," if dueDate != None else ''} is_material = {isMaterial}, is_task = {isTask}, is_announcment = {isAnnouncment}, course_id = '{courseId}' where id = '{id}'")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def deleteAssignment(id):
    try:
        cursor.execute(f"delete from {table} where id = '{id}'")
        conn.commit()
        return 'Success'
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
        