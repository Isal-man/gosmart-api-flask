from flask import Blueprint, current_app, request, redirect, url_for, session
from flask_login import current_user
from flask_jwt_extended import create_access_token, create_refresh_token
from Helpers.response import response
from Services.userService import findUserByIdentity, registerUser
from Services.authService import loginUserOauth
from urllib.parse import urlencode
from datetime import datetime
from random_username.generate import generate_username
import secrets
import requests

apiOauth = Blueprint('oauth', __name__)

@apiOauth.route('/authorize/<provider>')
def oauthLogin(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('test'))
    
    providerData = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if providerData is None:
        return response(0, 404, 'Provider not found'), 400
    
    session['oauth2_state'] = secrets.token_urlsafe(16)
    
    qs = urlencode({
        'client_id': providerData['client_id'],
        'redirect_uri': url_for('oauth.oauthCallback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(providerData['scopes']),
        'state': session['oauth2_state']
    })
    
    return redirect(providerData['authorize_url'] + '?' + qs)

@apiOauth.route('/callback/<provider>')
def oauthCallback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('test'))
    
    providerData = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if providerData is None:
        return response(0, 404, 'Provider not found'), 400
    
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                print(f'{k}: {v}')
        return redirect(url_for('test'))
    
    if request.args['state'] != session.get('oauth2_state'):
        return response(0, 401, 'Please login to your account first!'), 401
    
    if 'code' not in request.args:
        return response(0, 401, 'Please login to your account first!'), 401
    
    res = requests.post(providerData['token_url'], data={
        'client_id': providerData['client_id'],
        'client_secret': providerData['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth.oauthCallback', provider=provider, _external=True)
    }, headers={'Accept': 'application/json'})
    
    if res.status_code != 200:
        return response(0, 401, 'Please login to your account first!'), 401
    
    accessToken = res.json().get('access_token')

    if not accessToken:
        return response(0, 401, 'Please login to your account first!'), 401
    
    res = requests.get(providerData['userInfo']['url'], headers={
         'Authorization': 'Bearer ' + accessToken,
         'Accept': 'application/json'
    })
    
    if res.status_code != 200:
        return response(0, 401, 'Please login to your account first!'), 401
    
    email = providerData['userInfo']['email'](res.json())
    
    randomName = generate_username(1)[0]
    
    user = findUserByIdentity(email)
    if user == 'Fail':
        data = {
            "username": randomName,
            "email": email,
            "password": provider + "@123",
            "fullName": randomName,
            "phoneNumber": None,
            "image": "https://storage.googleapis.com/gosmart-classroom.appspot.com/8380015.png",
            "provider": provider,
            "isVerified": True,
            "createdAt": datetime.utcnow()
        }
        
        register = registerUser(data)
        
        if register == 'Fail':
            return response(0, 500, 'Failed to register account'), 500
        
        user = findUserByIdentity(email)
    
    req = {
        'username': user.get('username'),
        'email': user.get('email'),
        'password': user.get('password')
    }
    
    login = loginUserOauth(req)
    if login == 'Fail':
        return response(0, 500, 'Failed to login'), 500
    accessToken = create_access_token(identity=login)
    refreshToken = create_refresh_token(identity=login)
        
    data = {
            'access-token': accessToken,
            'refresh-token': refreshToken,
            'username': req.get('username'),
            'email': req.get('email')
        }
        
    return response(data, 200, 'Successfully to login'), 200