from flask import Blueprint, request
from Helpers.response import response
from Services.courseService import findAllCourses, findCourseById, findCourseAsTeacher, findCourseAsStudent, findCourseByCode, insertCourse, updateCourse, deleteCourse
from datetime import datetime
from flask_jwt_extended import jwt_required
import uuid

apiCourse = Blueprint('course', __name__)

@apiCourse.route('/<userId>')
@jwt_required()
def getAllCourses(userId):
    try:
        data = findAllCourses(userId)
        return response(data, 200, 'Success get all course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed get all course'), 500
    
@apiCourse.route('/<userId>/<id>')
@jwt_required()
def getCourseById(userId, id):
    try:
        data = findCourseById(userId, id)
        return response(data, 200, 'Success get course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed get course'), 500

@apiCourse.route('/code/<code>')
@jwt_required()
def getCourseByCode(code):
    try:
        data = findCourseByCode(code)
        return response(data, 200, 'Success get course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed get all course'), 500

@apiCourse.route('/teacher')
@jwt_required()
def getCourseAsTeacher():
    try:
        user = request.args('user')
        if user == None:
            return response(0, 400, 'Param user is required'), 400
        data = findCourseAsTeacher(user)
        return response(data, 200, 'Success get course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed get course'), 500

@apiCourse.route('/student')
@jwt_required()
def getCourseAsStudent():
    try:
        user = request.args('user')
        if user == None:
            return response(0, 400, 'Param user is required'), 400
        data = findCourseAsStudent(user)
        return response(data, 200, 'Success get course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed get course'), 500

@apiCourse.route('/create', methods=['POST'])
@jwt_required()
def addCourse():
    try:
        req = {}
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if request.json.get('name'):
            req['name'] = request.json.get('name')
        if request.json.get('schedule'):
            req['schedule'] = request.json.get('schedule')
        if request.json.get('theme'):
            req['theme'] = request.json.get('theme')
        if request.json.get('image'):
            req['image'] = request.json.get('image')
        if request.json.get('userId'):
            req['userId'] = request.json.get('userId')
        req['id'] = str(uuid.uuid4())
        req['createdAt'] = datetime.utcnow()
        req['isArchived'] = False
        
        data = insertCourse(req)
        
        if data == 'Fail':
            return response(0, 500, 'Failed to create course'), 500
        
        return response(data, 200, 'Success create course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to create course'), 500
    
@apiCourse.route('/update/<userId>/<id>', methods=['PUT'])
@jwt_required()
def updateCourseById(userId, id):
    try:
        req = {}
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if request.json.get('name'):
            req['name'] = request.json.get('name')
        if request.json.get('schedule'):
            req['schedule'] = request.json.get('schedule')
        if request.json.get('theme'):
            req['theme'] = request.json.get('theme')
        if request.json.get('image'):
            req['image'] = request.json.get('image')
        if request.json.get('userId'):
            req['userId'] = request.json.get('userId')
        
        data = findCourseById(userId, id)
        
        if data == 'Fail':
            return response(0, 404, 'Data not found'), 404
        
        req['isArchived'] = data.get('is_archived')
        update = updateCourse(req, id)
        if update == 'Fail':
            return response(0, 500, 'Failed to update course'), 500
        
        return response(update, 200, 'Success update course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to update course'), 500
    
@apiCourse.route('/delete/<userId>/<id>', methods=['DELETE'])
@jwt_required()
def deleteCourseById(userId, id):
    try:
        data = findCourseById(userId, id)
        if data == 'Fail':
            return response(0, 404, 'Data Not Found'), 404
        delete = deleteCourse(userId, id)
        if delete == 'Fail':
            return response(0, 500, 'Failed to delete course'), 500
        return response(0, 200, 'Success delete course'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to delete course'), 500
        