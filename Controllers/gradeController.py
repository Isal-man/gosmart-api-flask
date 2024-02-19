from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from Services.gradeService import findAllGrade, findAllByUser, findAllByAssignment, findGradeById, findGradeByUserAndAssignment, insertGrade, updateGrade
from Helpers.response import response
from datetime import datetime
from uuid import uuid4

apiGrade = Blueprint('grade', __name__)

@apiGrade.route('/')
@jwt_required()
def getAll():
    try:
        data = findAllGrade()
        if data == 'Fail':
            return response(0, 500, 'Failed to get all grade'), 500
        return response(data, 200, 'Success to get all grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error')
    
@apiGrade.route('/user/<user>')
@jwt_required()
def getAllByUser(user):
    try:
        data = findAllByUser(user)
        if data == 'Fail':
            return response(0, 500, 'Failed to get all grade'), 500
        return response(data, 200, 'Success to get all grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error')
    
@apiGrade.route('/assignment/<assignment>')
@jwt_required()
def getAllByAssignment(assignment):
    try:
        data = findAllByAssignment(assignment)
        if data == 'Fail':
            return response(0, 500, 'Failed to get all grade'), 500
        return response(data, 200, 'Success to get all grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error')
    
@apiGrade.route('/<id>')
@jwt_required()
def getById(id):
    try:
        data = findGradeById(id)
        if data == 'Fail':
            return response(0, 500, 'Failed to get grade'), 500
        return response(data, 200, 'Success to get grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error')
    
@apiGrade.route('/<user>/<assignment>')
@jwt_required()
def getByUserAndAssignment(user, assignment):
    try:
        data = findGradeByUserAndAssignment(user, assignment)
        if data == 'Fail':
            return response(0, 500, 'Failed to get all grade'), 500
        return response(data, 200, 'Success to get all grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error')
    
@apiGrade.route('/create', methods=['POST'])
@jwt_required()
def insert():
    try:
        req = {}
        teacher = request.args.get('teacher')
        if teacher == None:
            return response(0, 400, 'Param teacher is required'), 400
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        print(request.json.get('grade'), 'grade')
        print(request.json.get('userId'), 'user')
        print(request.json.get('assignmentId'), 'assignment')
        print(request.json.get('courseId'), 'course')
        if request.json.get('grade'):
            req['grade'] = request.json.get('grade')
        if request.json.get('userId'):
            req['userId'] = request.json.get('userId')
        if request.json.get('assignmentId'):
            req['assignmentId'] = request.json.get('assignmentId')
        if request.json.get('courseId'):
            req['courseId'] = request.json.get('courseId')
        
        req['id'] = str(uuid4())
        print(req.get('id'))
        req['createdAt'] = datetime.utcnow()
        
        insert = insertGrade(req, teacher)
        print(insert)
        if insert == 'Fail':
            return response(0, 500, 'Failed to insert grade'), 500
        
        return response(insert, 200, 'Success to insert grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500
    
@apiGrade.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    try:
        req = {}
        teacher = request.args.get('teacher')
        if teacher == None:
            return response(0, 400, 'Param teacher is required'), 400
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if request.json.get('grade'):
            req['grade'] = request.json.get('grade')
        if request.json.get('userId'):
            req['userId'] = request.json.get('userId')
        if request.json.get('assignmentId'):
            req['assignmentId'] = request.json.get('assignmentId')
        if request.json.get('courseId'):
            req['courseId'] = request.json.get('courseId')
        
        req['id'] = id
        
        update = updateGrade(req, teacher)
        if update == 'Fail':
            return response(0, 500, 'Failed to update grade'), 500
        
        return response(update, 200, 'Success to update grade'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500