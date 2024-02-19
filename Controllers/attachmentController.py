from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from Services.attachmentService import findAllAttachment, findAttachmentByAssignmentAndStatus, findAttachmentById, findAttachmentsByAssignmentAndUser, uploadAttachment, deleteAttachment
from Helpers.response import response
from datetime import datetime
from uuid import uuid4

apiAttachment = Blueprint('attachment', __name__)

@apiAttachment.route('/')
@jwt_required()
def getAll():
    try:
        data = findAllAttachment()
        if data == 'Fail':
            return response(0, 500, 'Failed to get all attachment'), 500
        return response(data, 200, 'Success to get all attachment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500
    
@apiAttachment.route('/<id>')
@jwt_required()
def getById(id):
    try:
        data = findAttachmentById(id)
        if data == 'Fail':
            return response(0, 500, 'Failed to get attachment'), 500
        return response(data, 200, 'Success to get attachment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500

@apiAttachment.route('/assignment/<aid>')
@jwt_required()
def getByAssignmentAndStatus(aid):
    try:
       status = "is_teacher" if request.args.get('status') == 'teacher' else "is_student"
       user = request.args.get('user')
       data = findAttachmentByAssignmentAndStatus(aid, status) if status != None else findAttachmentsByAssignmentAndUser(aid, user)
       if data == 'Fail':
           return response(0, 500, 'Failed to get data attachment'), 500
       return response(data, 200, 'Success to get attachment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500

@apiAttachment.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    try:
        req = {
            'isFromTeacher': False,
            'isFromStudent': False
        }
        status = request.args.get('status')
        if status == None:
            return response(0, 400, 'Param status is required'), 400
        if status == 'teacher':
            req['isFromTeacher'] = True
        if status == 'student':
            req['isFromStudent'] = True
        if not request.json:
            return response(0, 400, 'Request body is required'), 400
        if request.json.get('name'):
            req['name'] = request.json.get('name')
        if request.json.get('url'):
            req['url'] = request.json.get('url')
        if request.json.get('type'):
            req['type'] = request.json.get('type')
        if request.json.get('enrollmentId'):
            req['enrollmentId'] = request.json.get('enrollmentId')
        if request.json.get('assignmentId'):
            req['assignmentId'] = request.json.get('assignmentId')
        if request.json.get('user'):
            req['user'] = request.json.get('user')
            
        req['id'] = str(uuid4())
        req['createdAt'] = datetime.utcnow()
        
        upload = uploadAttachment(req)
        if upload == 'Fail':
            return response(0, 500, 'Failed to upload attachment'), 500
        
        return response(upload, 200, 'Success to upload attachment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500

@apiAttachment.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        data = findAttachmentById(id)
        if data == 'Fail':
            return response(0, 404, 'Data not found'), 404
        delete = deleteAttachment(id)
        if delete == 'Fail':
            return response(0, 500, 'Failed to delete attachment'), 500
        
        return response(delete, 200, 'Success to delete attachment'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Internal server error'), 500