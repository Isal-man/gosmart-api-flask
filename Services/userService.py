from Configs.postgresqlConfig import conn, cursor
from Helpers.postgreHelpers import addingUserEmail
import hashlib

table = "users"
columnTable = "username, email, password, full_name, phone_number, image, provider, is_verified, created_at"

def findUserByIdentity(identity):
    try:
        cursor.execute(f"select {columnTable} from {table} where email = '{identity}' or username = '{identity}'")
        data = cursor.fetchone()
        return addingUserEmail(data)
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"

def registerUser(data):
    try:
        username = data['username']
        email = data['email']
        password = hashingPassword(data['password'])
        fullName = data['fullName']
        phoneNumber = data['phoneNumber']
        image = data['image']
        provider = data['provider']
        isVerified = data['isVerified']
        createdAt = data['createdAt']
        
        data['password'] = password
        
        cursor.execute(f"insert into {table} ({columnTable}) values ('{username}', '{email}', '{password}', '{fullName}', '{phoneNumber}', '{image}', '{provider}', '{isVerified}', '{createdAt}')")
        conn.commit()
        return data
    except BaseException as e:
        print(e)
        conn.rollback()
        return "Fail"
    
def verificationUser(email):
    data = findUserByIdentity(email)
    if data == 'Fail' or data.get('is_verified') == True:
        return 'Fail'
    
    cursor.execute(f"update {table} set is_verified = {True} where email = '{email}'")
    conn.commit()
    
    return "Success"
    
def hashingPassword(password):
    hash = hashlib.md5(password.encode())
    
    return hash.hexdigest()