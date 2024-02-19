from Configs.firebaseConfig import bucket
from flask import make_response

def uploadImage(filename, type, image):
    try:
        if filename == None and image == None and type == None:
            return 'Fail'
        blob = bucket.blob(filename)
        blob.content_type = type
        blob.upload_from_file(image)
        return "Success"
    except BaseException as e:
        print(e)
        return "Fail"
    
def uploadVideo(filename, type, video):
    try:
        if filename == None and video == None and type == None:
            return 'Fail'
        blob = bucket.blob(filename)
        blob.content_type = type
        blob.upload_from_file(video)
        return "Success"
    except BaseException as e:
        print(e)
        return "Fail"
    
def uploadFile(filename, type, file):
    try:
        if filename == None and file == None and type == None:
            return 'Fail'
        blob = bucket.blob(filename)
        blob.content_type = type
        blob.upload_from_file(file)
        return "Success"
    except BaseException as e:
        print(e)
        return "Fail"
    
def download(path):
    try:
        if path == None:
            return 'Fail'
        blob = bucket.blob(path)
        downloadUrl = blob.download_as_string()
        response = make_response(downloadUrl)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename={path}'
        return response
    except BaseException as e:
        print(e)
        return "Fail"
    
# def deleteImage(path):
#     try:
#         if path == None:
#             return 'Fail'
#         pathCloud = "images"
#         storage.child(pathCloud).delete(path)
#     except BaseException as e:
#         print(e)
#         return "Fail"
    
# def deleteVideo(path):
#     try:
#         if path == None:
#             return 'Fail'
#         pathCloud = "videos"
#         storage.child(pathCloud).delete(path)
#     except BaseException as e:
#         print(e)
#         return "Fail"
    
# def deleteFile(path):
#     try:
#         if path == None:
#             return 'Fail'
#         pathCloud = "files"
#         storage.child(pathCloud).delete(path)
#     except BaseException as e:
#         print(e)
#         return "Fail"