def response(data, status, message):
    desc = ""
    
    if status == 200:
        desc = "OK"
    elif status == 201:
        desc = "Created"
    elif status == 400:
        desc = "Bad Request"
    elif status == 401:
        desc = "Unauthorized"
    elif status == 403:
        desc = "Forbidden"
    elif status == 404:
        desc = "Not Found"
    elif status == 409:
        desc = "Conflict"
    elif status == 500:
        desc = "Internal Server Error"
        
    res = {
        "status": status,
        "desc": desc,
        "message": message,
        "data": data
    }
    
    return res