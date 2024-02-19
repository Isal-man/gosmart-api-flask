from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from Services.enrollmentService import findAll, findAllParticipant, findEnrollmentById, findUserHasEnroll, joinCourseAsStudent, deleteStudent
from Helpers.response import response
from datetime import datetime
from uuid import uuid4

apiEnrollment = Blueprint('enrollment', __name__)

@apiEnrollment.route('/')
@jwt_required()
def getAll():
    try:
        data = findAll()
        if data == 'Fail':
            return response(0, 500, 'Failed to get all enrollment'), 500
        return response(data, 200, 'Success to get all enrollment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to get all enrollment'), 500
    
@apiEnrollment.route('/participant')
@jwt_required()
def getAllParticipant():
    try:
        cid = request.args.get('cid')
        if cid == None:
            return response(0, 400, 'Param cid is required'), 400
        data = findAllParticipant(cid)
        if data == 'Fail':
            return response(0, 500, 'Failed to get all participant'), 500
        return response(data, 200, 'Success to get all participant'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500
    
@apiEnrollment.route('/<id>')
@jwt_required()
def getById(id):
    try:
        data = findEnrollmentById(id)
        if data == 'Fail':
            return response(0, 500, 'Failed to get enrollment'), 500
        return response(data, 200, 'Success to get enrollment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500

@apiEnrollment.route('/join', methods=['POST'])
@jwt_required()
def joinCourse():
    try:
        req = {}
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if request.json.get('userId'):
            req['userId'] = request.json.get('userId')
        if request.json.get('courseId'):
            req['courseId'] = request.json.get('courseId')
        
        check = findUserHasEnroll(req.get('userId'))
        if check == 'Fail':
            return response(0, 500, 'Failed to get user enrollment status'), 500
        if check == True:
            return response(0, 400, 'User has been enrolled'), 400
        
        req['id'] = str(uuid4())
        req['createdAt'] = datetime.utcnow()
        
        join = joinCourseAsStudent(req)
        if join == 'Fail':
            return response(0, 500, 'User failed to join course'), 500
        
        return response(join, 200, "User success to join course"), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500
    
@apiEnrollment.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        data = findEnrollmentById(id)
        if data == 'Fail':
            return response(0, 404, 'Data not found'), 404
        if request.args.get('cid') == None:
            return response(0, 400, 'Param cid is required'), 400
        if request.args.get('uid') == None:
            return response(0, 400, 'Param uid is required'), 400
        cid = request.args.get('cid')
        uid = request.args.get('uid')
        delete = deleteStudent(uid, cid)
        if delete == 'Fail':
            return response(0, 500, 'Failed to delete student'), 400
        
        return response(delete, 200, 'Success to delete student'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500