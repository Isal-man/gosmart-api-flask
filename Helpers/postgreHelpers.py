def addingCourse(data):
    tamp = {
        'id': data[0],
        'name': data[1],
        'schedule': data[2],
        'theme': data[3],
        'image': data[4],
        'is_archived': data[5],
        'user_id': data[6]
    }
    
    return tamp

def addingUserEmail(data):
    tamp = {
        'username': data[0],
        'email': data[1],
        'password': data[2],
        'full_name': data[3],
        'phone_number': data[4],
        'image': data[5],
        'provider': data[6],
        'is_verified': data[7],
        'created_at': data[8]
    }
    
    return tamp

def addingLoginUser(data):
    tamp = {
        'username': data[0],
        'email': data[1],
        'password': data[2]
    }
    
    return tamp

def addingAssignment(data, isDescription):
    tamp = {
        'id': data[0],
        'name': data[1],
        'postDate': data[2],
        'createdAt': data[3],
        'isMaterial': data[4],
        'isTask': data[5],
        'isAnnouncment': data[6],
        'course_id': data[7],
        'dueDate': data[8]
    }
    if isDescription == True:
        tamp['description'] = data[9]
    
    return tamp

def addingEnrollment(data):
    tamp = {
        'id': data[0],
        'isStudent': data[2],
        'isTeacher': data[3],
        'userId': data[4],
        'courseId': data[5]
    }
    
    return tamp

def addingAttachment(data):
    tamp = {
        'id': data[0],
        'name': data[1],
        'url': data[2],
        'type': data[3],
        'createdAt': data[4],
        'isFromTeacher': data[5],
        'isFromStudent': data[6],
        'enrollmentId': data[7],
        'assignmentId': data[8]
    }
    
    return tamp

def addingGrade(data):
    tamp = {
        'id': data[0],
        'grade': data[1],
        'createdAt': data[2],
        'userId': data[3],
        'assignmentId': data[4],
        'courseId': data[5]
    }
    
    return tamp