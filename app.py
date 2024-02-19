import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from Controllers.courseController import apiCourse
from Controllers.userController import apiUser
from Controllers.authController import apiAuth
from Controllers.oauth2Controller import apiOauth
from Controllers.firebaseController import apiFirebase
from Controllers.assignmentController import apiAssignment
from Controllers.enrollmentController import apiEnrollment
from Controllers.attachmentController import apiAttachment
from Controllers.gradeController import apiGrade
from flask_jwt_extended import JWTManager
from Services.userService import findUserByIdentity
from datetime import timedelta

app = Flask(__name__)
CORS(app)
JWTManager(app)

login = LoginManager(app)

@login.user_loader
def loadUser(email):
    return findUserByIdentity(email)

app.debug = True
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=3)
app.config['OAUTH2_PROVIDERS'] = {
    'google': {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'authorize_url': os.getenv('GOOGLE_AUTHORIZE_URL'),
        'token_url': os.getenv('GOOGLE_TOKEN_URL'),
        'userInfo': {
            'url': os.getenv('GOOGLE_USER_INFO'),
            'email': lambda json: json['email']
        },
        'scopes': [os.getenv('GOOGLE_SCOPES')]
    },
    'github': {
        'client_id': os.getenv('GITHUB_CLIENT_ID'),
        'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
        'authorize_url': os.getenv('GITHUB_AUTHORIZE_URL'),
        'token_url': os.getenv('GITHUB_TOKEN_URL'),
        'userInfo': {
            'url': os.getenv('GITHUB_USER_INFO'),
            'email': lambda json: json[0]['email']
        },
        'scopes': [os.getenv('GITHUB_SCOPES')]
    }
}

app.register_blueprint(apiCourse, url_prefix = '/api/v1/course')
app.register_blueprint(apiUser, url_prefix='/api/v1/user')
app.register_blueprint(apiAuth, url_prefix='/api/v1/auth')
app.register_blueprint(apiOauth, url_prefix='/api/v1/oauth')
app.register_blueprint(apiFirebase, url_prefix='/api/v1/firebase')
app.register_blueprint(apiAssignment, url_prefix='/api/v1/assignment')
app.register_blueprint(apiEnrollment, url_prefix='/api/v1/enrollment')
app.register_blueprint(apiAttachment, url_prefix='/api/v1/attachment')
app.register_blueprint(apiGrade, url_prefix='/api/v1/grade')

@app.route("/test")
def test():
    return "<h1>Gosmart Classroom With Python-Flask</h1>"

def main(port):
    os.environ["APP_PORT"] = str(port)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get("APP_PORT"))