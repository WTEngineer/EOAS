from bottle import Bottle, request, response, HTTPResponse, HTTPError, static_file
import json
from truckpad.bottle.cors import CorsPlugin, enable_cors
from decimal import Decimal
import time
import math
import os
import sqlite3
from main import FaceRecogSys
import cv2
import base64
import numpy as np

app = Bottle()



conn = sqlite3.connect('database/face_db.db')
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

def get_user_register_list():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_register_table")
    rows = cursor.fetchall()
    conn.commit()
    person_register_list = []
    for row in rows:
        face_bytes = row[5]

        # Save the image with the person's ID as the filename
        image_filename = f"{row[0]}.png"
        image_path = os.path.join(STATIC_ROOT, 'images', image_filename)
        if not os.path.exists(image_path):
            face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, face_bytes)
            cv2.imwrite(image_path, face_img)
        
        # Construct the URL for the avatar
        avatar_url = f"http://localhost:8000/images/{image_filename}"
        
        person = {
            'id': row[0],
            'name': row[1],
            'birth': row[2],
            'age': row[3],
            'status': row[4],
            'gender': row[7],
            'guesttype': row[8],
            'safetytype': row[9],
            'blocked': row[10],
            'whenfrom': row[11],
            'whento': row[12],
            'place': row[13],
            'reason': row[14],
            'type': row[15],
            'info': row[16],
            'avatar': avatar_url
        }
        person_register_list.append(person)
    return person_register_list

def get_admin_register_list():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_register_table")
    rows = cursor.fetchall()
    conn.commit()
    
    user_register_list = []
    for row in rows:
        temp = {
            'id': row[0],
            'name': row[1],
            'usergroup': row[2],
            'password': row[3],
            'creator': row[4],
            'phone': row[5],
            'blocked': row[6]
        }
        user_register_list.append(temp)
    return user_register_list

def get_user_history_list():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_history_table")
    rows = cursor.fetchall()
    conn.commit()
    person_history_list = []
    for row in rows:
        face_bytes = row[8]
        
        # Save the image with the person's ID as the filename
        image_filename = f"{row[0]}.png"
        image_path = os.path.join(STATIC_ROOT, 'images', image_filename)
        if not os.path.exists(image_path):
            print('not exist')
            face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, face_bytes)
            cv2.imwrite(image_path, face_img)
        
        # Construct the URL for the avatar
        avatar_url = f"http://localhost:8000/images/{image_filename}"
        
        person = {
            'id': row[0],
            'name': row[1],
            'gender': row[2],
            'age': row[3],
            'time': row[4],
            'place': row[5],
            'view': row[6],
            'action': row[7],
            'avatar': avatar_url
        }
        person_history_list.append(person)
    return person_history_list

def get_admin_history_list():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_history_table")
    rows = cursor.fetchall()
    conn.commit()

    admin_history_list = []
    for row in rows:
        temp = {
            'id': row[0],
            'name': row[1],
            'action': row[2],
            'time': row[3],
            'content': row[4],
        }

        admin_history_list.append(temp)
    return admin_history_list

def get_admin_by_id(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_register_table WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'usergroup': row[2],
            'password': row[3],
            'creator': row[4],
            'phone': row[5],
            'blocked': row[6]
        }
    return None

def get_user_by_id(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_register_table WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        face_bytes = row[5]

        # Save the image with the person's ID as the filename
        image_filename = f"{row[0]}.png"
        image_path = os.path.join(STATIC_ROOT, 'images', image_filename)
        if not os.path.exists(image_path):
            face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, face_bytes)
            cv2.imwrite(image_path, face_img)
        
        # Construct the URL for the avatar
        avatar_url = f"http://localhost:8000/images/{image_filename}"
        
        return {
            'id': row[0],
            'name': row[1],
            'birth': row[2],
            'age': row[3],
            'status': row[4],
            'gender': row[7],
            'guesttype': row[8],
            'safetytype': row[9],
            'blocked': row[10],
            'whenfrom': row[11],
            'whento': row[12],
            'place': row[13],
            'reason': row[14],
            'type': row[15],
            'info': row[16],
            'avatar': avatar_url
        }
    return None


# Api endpoints


# users
@enable_cors
@app.get('/api/users/get-admin')
def allAdmins():
    
    users = get_admin_register_list()
    
    return json.dumps(users)

@enable_cors
@app.get('/api/users/get-admin/<id>')
def singleAdmin(id):
    user = get_admin_by_id(id)
    
    if user:
        response.content_type = 'application/json'
        return json.dumps(user)
    response.status = 404
    return {"status": "error", "message": "User not found"}

@enable_cors
@app.post('/api/users/add-admin')
def addAdmin():
    data = request.json
    name = data.get('name')
    usergroup = data.get('usergroup')
    password = data.get('password')
    creator = data.get('creator')
    phone = data.get('phone')
    blocked = data.get('blocked')
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_register_table (name, usergroup, password, creator, phone, blocked) VALUES (?, ?, ?, ?, ?, ?)", 
                   (name, usergroup, password, creator, phone, blocked))
    id = cursor.lastrowid
    user = get_admin_by_id(id)
    conn.commit()
    
    
    response.status = 201
    return json.dumps(user)

@enable_cors
@app.put('/api/users/edit-admin/<id>')
def editAdmin(id):
    data = request.json
    name = data.get('name')
    usergroup = data.get('usergroup')
    password = data.get('password')
    creator = data.get('creator')
    phone = data.get('phone')
    blocked = data.get('blocked')
    
    # if not all([name, usergroup, password, creator, phone, blocked is not None]):
    #     response.status = 400
    #     return {"status": "error", "message": "Missing user data"}
    
    cursor = conn.cursor()
    cursor.execute("UPDATE user_register_table SET name = ?, usergroup = ?, password = ?, creator = ?, phone = ?, blocked = ? WHERE id = ?", 
                   (name, usergroup, password, creator, phone, blocked, id))
    
    user = get_admin_by_id(id)
    conn.commit()
    
    return json.dumps(user)

@enable_cors
@app.delete('/api/users/delete-admin/<id>')
def deleteAdmin(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_register_table WHERE id = ?", (id,))
    conn.commit()
    
    
    return {"status": "success", "message": "Admin deleted successfully"}

@enable_cors
@app.get('/api/users/get-user')
def allUsers():
    
    users = get_user_register_list()
    
    return json.dumps(users)

@enable_cors
@app.get('/api/users/get-user/<id>')
def singleUser(id):
    user = get_user_by_id(id)
    
    if user:
        response.content_type = 'application/json'
        return json.dumps(user)
    response.status = 404
    return {"status": "error", "message": "User not found"}

@enable_cors
@app.post('/api/users/add-user')
def addUser():
    data = request.json
    name = data.get('name')
    birth = data.get('birth')
    age = data.get('age')
    status = data.get('status')
    face = data.get('avatar')
    face_bytes = cv2.imencode('.jpg', face)[1].tobytes()
    res = FaceRecogSys.face_recognizer.predict(face)
    emb = res[0].embedding
    emb_bytes = emb.tobytes()

    if status == "Not Allow":
        gender = None
        guesttype = None
        safetytype = None
        blocked = None
        whenfrom = None
        whento = None
        place = None
        reason = None
        type = None
        info = None
    else:
        gender = data.get('gender')
        guesttype = data.get('guesttype')
        safetytype = data.get('safetytype')
        blocked = data.get('blocked')
        whenfrom = data.get('whenfrom')
        whento = data.get('whento')
        place = data.get('place')
        reason = data.get('reason')
        type = data.get('type')
        info = data.get('info')
    # ----  save person to db --------
    try:
        cursor = conn.cursor()
        sqlite_insert_blob_query = """ INSERT INTO person_register_table
        (name, birth, age, status, photo, emb, gender, guesttype, safetytype, blocked, whenfrom, whento, place, reason, type, info) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        # Convert data into tuple format
        data_tuple = (name, birth, age, status, face_bytes, emb_bytes, gender, guesttype, safetytype, blocked, whenfrom, whento, place, reason, type, info)

        cursor.execute(sqlite_insert_blob_query, data_tuple)
        id = cursor.lastrowid
        user = get_user_by_id(id)
        conn.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()
        if user:
            response.content_type = 'application/json'
            return json.dumps(user)

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

@enable_cors
@app.put('/api/users/edit-user/<id>')
def editUser(id):
    data = request.json
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_register_table WHERE id = ?", (id,))
    row = cursor.fetchone()
    name = data.get('name')
    birth = data.get('birth')
    age = data.get('age')
    status = data.get('status')
    face = data.get('avatar')
    
    if isinstance(face, str) and 'http' in face:
        face_bytes = row[5]
        emb_bytes = row[6]
    else:
        face_bytes = cv2.imencode('.jpg', face)[1].tobytes()
        res = FaceRecogSys.face_recognizer.predict(face)
        emb = res[0].embedding
        emb_bytes = emb.tobytes()

    if status == "Not Allow":
        gender = None
        guesttype = None
        safetytype = None
        blocked = None
        whenfrom = None
        whento = None
        place = None
        reason = None
        type = None
        info = None
    else:
        gender = data.get('gender')
        guesttype = data.get('guesttype')
        safetytype = data.get('safetytype')
        blocked = data.get('blocked')
        whenfrom = data.get('whenfrom')
        whento = data.get('whento')
        place = data.get('place')
        reason = data.get('reason')
        type = data.get('type')
        info = data.get('info')
    # ----  save person to db --------
    try:
        cursor = conn.cursor()
        sqlite_insert_blob_query = """ UPDATE person_register_table SET
                name = ?, birth = ?, age = ?, status = ?, photo = ?, emb = ?, gender = ?, guesttype = ?, 
                safetytype = ?, blocked = ?, whenfrom = ?, whento = ?, place = ?, reason = ?, type = ?, info = ? 
                WHERE id = ?"""

        # Convert data into tuple format
        data_tuple = (name, birth, age, status, face_bytes, emb_bytes, gender, guesttype, safetytype, blocked,
                        whenfrom, whento, place, reason, type, info, id)

        cursor.execute(sqlite_insert_blob_query, data_tuple)
        user = get_user_by_id(id)
        conn.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()
        if user:
            response.content_type = 'application/json'
            return json.dumps(user)

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

@enable_cors
@app.delete('/api/users/delete-user/<id>')
def deleteUser(id):
    cursor = conn.cursor()
    sqlite_insert_blob_query = """ DELETE from person_register_table WHERE id=?"""

    cursor.execute(sqlite_insert_blob_query, (id, ))
    conn.commit()
    print("Delete one registered person successfully.")
    cursor.close()
    
    return {"status": "success", "message": "User deleted successfully"}


@enable_cors
@app.get('/api/users/admin-history')
def adminHistory():
    
    history = get_admin_history_list()
    
    return json.dumps(history)

@enable_cors
@app.get('/api/users/user-history')
def userHistory():
    
    history = get_user_history_list()
    
    return json.dumps(history)



# auth
@enable_cors
@app.post('/api/auth/login')
def login():
    try:
        login_data = request.json
        username = login_data.get('username')
        password = login_data.get('password')

        if not username or not password:
            response.status = 400
            return json.dumps({"error": "Username and password are required"})

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_register_table WHERE name=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.commit()

        if user:
            response.set_cookie("account", json.dumps({"username": username}), secret='my_secret_key', max_age=3600)
            response.content_type = 'application/json'
            return json.dumps({"message": "Login successful", "user": {"id": user[0], "name": user[1], "usergroup": user[2], "password": user[3], "creator": user[4], "phone": user[5], 'blocked': user[6], 'permission': 'admin'}})
        else:
            response.status = 401
            return json.dumps({"error": "Invalid username or password"})
    except Exception as e:
        response.status = 500
        return json.dumps({"error": str(e)})

@enable_cors
@app.post('/api/auth/logout')
def logout():
    response.delete_cookie("account")
    return {"status": "success", "message": "Logged out successfully."}

@enable_cors
@app.post('/api/signature')
def signature():
    # try:
    signature_data = request.json
    data = signature_data.get('data')
    
    print('received')
    header, encoded = data.split(",", 1)
    data = base64.b64decode(encoded)

    FaceRecogSys.sign_capture_btn_clicked_with_image(FaceRecogSys, data)
    return json.dumps({"data": "http://localhost:8000/images/result.jpg"})

    # except Exception as e:
    #     response.status = 500
    #     return json.dumps({"error": str(e)})

@app.route('/images/<filename>')
@enable_cors
def serve_image(filename):
    file_path = os.path.join(STATIC_ROOT, 'images', filename)
    if os.path.exists(file_path):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        response.headers['Last-Modified'] = time.ctime(os.path.getmtime(file_path))
        return static_file(filename, root=os.path.join(STATIC_ROOT, 'images'))
    else:
        response.status = 404
        return "File not found."

def generate_frames1():
    # Video capture object
    cap1 = cv2.VideoCapture('./01.mp4')  # 0 for default camera
    while True:
        # Read the camera frame
        success, frame = cap1.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Concatenate frame bytes with appropriate headers for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap1.release()

def generate_frames2():
    # Video capture object
    cap2 = cv2.VideoCapture(0)  # 0 for default camera
    while True:
        # Read the camera frame
        success, frame = cap2.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Concatenate frame bytes with appropriate headers for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap2.release()

@app.route('/stream1')
def stream1():
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    return generate_frames1()

@app.route('/stream2')
def stream2():
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    return generate_frames2()