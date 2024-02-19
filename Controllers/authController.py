from flask import request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from Services.authService import loginUserLocal
from Helpers.response import response

apiAuth = Blueprint('auth', __name__)

@apiAuth.route('/login', methods=['POST'])
def login():
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
        
        user = loginUserLocal(req)
        if user == 'Fail':
            return response(0, 500, 'Failed to login'), 500
        accessToken = create_access_token(identity=user)
        refreshToken = create_refresh_token(identity=user)
        
        data = {
            'access-token': accessToken,
            'refresh-token': refreshToken,
            'username': user.get('username'),
            'email': user.get('email')
        }
        
        return response(data, 200, 'Successfully to login'), 200
        
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to login'), 500
    
@apiAuth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refreshToken():
    try:
        identity = get_jwt_identity()
        accessToken = create_access_token(identity=identity)
        return response(accessToken, 200, 'Successfully refresh token'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, 'Failed to refresh token'), 500
        