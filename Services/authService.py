from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingLoginUser
import hashlib

table = "users"
columnTable = "username, email, password, full_name, phone_number, image, provider, is_verified, created_at"

def loginUserLocal(data):
    try:
        username = data.get('username')
        email = data.get('email')
        hash = hashingPassword(data.get('password'))
        cursor.execute(f"select username, email, password from {table} where (username = '{username}' or email = '{email}') and password = '{hash}' and is_verified = {True}")
        user = cursor.fetchone()
        return addingLoginUser(user)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
    
def loginUserOauth(data):
    try:
        username = data.get('username')
        email = data.get('email')
        hash = data.get('password')
        cursor.execute(f"select username, email, password from {table} where (username = '{username}' or email = '{email}') and password = '{hash}' and is_verified = {True}")
        user = cursor.fetchone()
        return addingLoginUser(user)
    except BaseException as e:
        print(e)
        conn.rollback()
        return 'Fail'
        
def hashingPassword(password):
    hash = hashlib.md5(password.encode())
    
    return hash.hexdigest()
