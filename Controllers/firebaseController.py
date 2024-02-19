from flask import Blueprint, request
from Helpers.response import response
from Services.firebaseService import uploadImage, download
from flask_jwt_extended import jwt_required
import os

apiFirebase = Blueprint('firebase', __name__)

@apiFirebase.route('/upload/<type>', methods=['POST'])
@jwt_required()
def upload(type):  
    try: 
        upload = ""
        if type == None:
            return response(0, 400, 'Type is required!'), 400
        if type == 'image':
            file = request.files['image']
        if type == 'video':
            file = request.files['video']
        if type == 'file':
            file = request.files['file']

        contentType = file.content_type
        filename = file.filename
        url = "https://storage.googleapis.com/" + os.getenv('FIREBASE_BUCKET') + "/" + filename
        upload = uploadImage(filename,contentType,file)

        if upload == 'Fail':
            return response(0, 400, f'Failed to upload {type}'), 400

        res = {
            'filename': filename,
            'url': url,
            'type': contentType
        }

        return response(res, 200, f'Successfully upload {type}'), 200
    except BaseException as e:
        print(e)
        return response(0, 500, f'Failed to upload {type}'), 500
@apiFirebase.route('/download')
@jwt_required()
def download():
    url = ""
    
    if request.args.get('url') == None:
        return response(0, 400, 'Type is required!'), 400
    
    url = download(request.args.get('url'))
        
    return url