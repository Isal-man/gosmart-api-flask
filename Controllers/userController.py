from flask import Blueprint, request
from Helpers.response import response
from Services.userService import registerUser, verificationUser
from Services.emailService import verification
from datetime import datetime

apiUser = Blueprint('user', __name__)

@apiUser.route('/register', methods=['POST'])
def register():
    try:
        req = {}
        if not request.json:
            return response(0, 400, 'Request body is required!'), 400
        if request.json.get('username'):
            req['username'] = request.json.get('username')
        if request.json.get('email'):
            req['email'] = request.json.get('email')
        if request.json.get('password'):
            req['password'] = request.json.get('password')
        if request.json.get('fullName'):
            req['fullName'] = request.json.get('fullName')
        if request.json.get('image'):
            req['image'] = request.json.get('image') or "https://storage.googleapis.com/gosmart-classroom.appspot.com/8380015.png"
        if request.json.get('phoneNumber'):
            req['phoneNumber'] = request.json.get('phoneNumber')
        
        req['provider'] = 'Local'
        req['isVerified'] = False
        req['createdAt'] = datetime.utcnow()
        
        data = registerUser(req)
        if data == 'Fail':
            return response(0, 500, 'Failed to register user'), 500

        send = verification(req.get('email'))
        if send == 'Fail':
            return response(0, 500, 'Failed send email verification'), 500
        
        return response(data, 200, 'Succes register user'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to register user'), 500
    
@apiUser.route('/verification')
def verifyUser():
    try:
        if len(request.args.get('email')) < 0:
            return response(0, 400, 'Email is required')
        
        email = request.args.get('email')
        
        verify = verificationUser(email)
        if verify == 'Fail':
            return response(0, 500, 'Failed for verification email or Your email has been verified'), 500
        
        return response(0, 200, 'Successfully verification your email'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed for verification email'), 500