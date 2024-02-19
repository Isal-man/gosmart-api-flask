from flask import Blueprint, request
from Helpers.response import response
from Services.assignmentService import findAllAssignment, findAssignmentById, findAssignmentByCourse, insertAssignment, updateAssignment, deleteAssignment
from datetime import datetime
from flask_jwt_extended import jwt_required
import uuid

apiAssignment = Blueprint('assignment', __name__)

@apiAssignment.route('/')
@jwt_required()
def getAllAssignment():
    try:
        data = findAllAssignment()
        if data == 'Fail':
            return response(0, 500, 'Failed to get assignments'), 500
        return response(data, 200, 'Success to get assignments'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to get assignments'), 500
    
@apiAssignment.route('/course/<course>')
@jwt_required()
def getAssignmentByCourse(course):
    try:
        data = findAssignmentByCourse(course)
        if data == 'Fail':
            return response(0, 500, f'Failed to get assignments by courseId = {course}'), 500
        return response(data, 200, f'Success to get assignments by courseId = {course}'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, f'Failed to get assignments by courseId = {course}'), 500
    
@apiAssignment.route('/<id>')
@jwt_required()
def getAssignmentById(id):
    try:
        data = findAssignmentById(id)
        if data == 'Fail':
            return response(0, 500, f'Failed to get assignments by ID = {id}'), 500
        return response(data, 200, f'Success to get assignments by ID = {id}'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, f'Failed to get assignments by ID = {id}'), 500
    
@apiAssignment.route('/create', methods=['POST'])
@jwt_required()
def createAssignment():
    try:
        req = {
            'isMaterial': False,
            'isTask': False,
            'isAnnouncment': False
        }
        type = request.args.get('type')
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if type == None:
            return response(0, 400, 'Param type is required'), 400
        if request.json.get('name'):
            req['name'] = request.json.get('name')
        if request.json.get('description'):
            req['description'] = request.json.get('description')
        if request.json.get('dueDate'):
            req['dueDate'] = request.json.get('dueDate')
        if request.json.get('courseId'):
            req['courseId'] = request.json.get('courseId')
        if type == 'material':
            req['isMaterial'] = True
        if type == 'task':
            req['isTask'] = True
        if type == 'announcment':
            req['isAnnouncment'] = True
        
        req['id'] = str(uuid.uuid4())
        req['postDate'] = datetime.utcnow()
        req['createdAt'] = datetime.utcnow()
        
        create = insertAssignment(req)
        
        if create == 'Fail':
            return response(0, 500, 'Failed to insert assignment'), 500
        
        return response(create, 200, 'Success to insert assignment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to insert assignment'), 500
    
@apiAssignment.route('/update/<id>', methods=['PUT'])
@jwt_required()
def updateAssignmentById(id):
    try:
        req = {}
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if request.json.get('name'):
            req['name'] = request.json.get('name')
        if request.json.get('description'):
            req['description'] = request.json.get('description')
        if request.json.get('dueDate'):
            req['dueDate'] = request.json.get('dueDate')
        if request.json.get('courseId'):
            req['courseId'] = request.json.get('courseId')
        req['postDate'] = datetime.utcnow()
        
        data = findAssignmentById(id)
        if data == 'Fail':
            return response(0, 404, 'Data not found'), 404
        
        req['isMaterial'] = data.get('isMaterial')
        req['isAnnouncment'] = data.get('isAnnouncment')
        req['isTask'] = data.get('isTask')
        
        update = updateAssignment(req, id)
        
        if update == 'Fail':
            return response(0, 500, 'Failed to insert assignment'), 500
        
        return response(update, 200, 'Success to insert assignment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to insert assignment'), 500
    
@apiAssignment.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def deleteAssignmentById(id):
    try:
        data = findAssignmentById(id)
        if data == 'Fail':
            return response(0, 404, 'Data not found'), 404
        delete = deleteAssignment(id)
        if delete == 'Fail':
            return response(0, 500, 'Failed to delete assignment'), 500
        return response(0, 200, 'Success to delete assignment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to delete assignment'), 500