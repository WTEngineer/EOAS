from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Response, Depends, Query
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, send_from_directory
import cv2
import json
import os
import time
from datetime import datetime, date
import sqlite3
from main import FaceRecogSys
import base64
import numpy as np
from face_det import FaceDetector
from face_recog import FaceRecognizer
from mrz_reader import MRZReader
import math
import threading
import queue
from dotenv import load_dotenv
import subprocess

app = FastAPI()
face_detector = FaceDetector()
face_recognizer = FaceRecognizer()
mrz_reader = MRZReader()

STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resource')
camera_analytics_queue = queue.Queue()
current_camera_action = 'Unknown'

load_dotenv()

# Get the ServerAddress from the environment variables
server_address = os.getenv('ServerAddress')

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify the allowed origins as a list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# Initialize cameras
#WT_use video
# camera_1 = cv2.VideoCapture('./sample1.mp4')
# camera_2 = cv2.VideoCapture('./01.mp4')
camera_1 = cv2.VideoCapture(0)
camera_2 = cv2.VideoCapture(1)
person_register_list = []
connected_websockets = []

def get_user_register_list():
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_register_table")
    rows = cursor.fetchall()
    person_register_list = []
    conn.commit()
    for row in rows:
        face_bytes = row[5]

        # Save the image with the person's ID as the filename
        image_filename = f"{row[0]}.png"
        image_path = os.path.join(STATIC_ROOT, 'images', image_filename)
        # if not os.path.exists(image_path):
        face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, face_bytes)
        cv2.imwrite(image_path, face_img)
        
        # Construct the URL for the avatar
        avatar_url = f"http://{server_address}:8000/images/{image_filename}"

        face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, row[5])
        emb = FaceRecogSys.bytes_to_emb(FaceRecogSys, row[6])
        
        person = {
            'id': row[0],
            'name': row[1],
            'birth': row[2],
            'age': row[3],
            'status': row[4],
            'face': face_img,
            'emb': emb,
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

def get_user_register_list1():
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_register_table")
    rows = cursor.fetchall()
    person_register_list = []
    conn.commit()
    for row in rows:
        face_bytes = row[5]

        # Save the image with the person's ID as the filename
        image_filename = f"{row[0]}.png"
        image_path = os.path.join(STATIC_ROOT, 'images', image_filename)
        # if not os.path.exists(image_path):
        face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, face_bytes)
        cv2.imwrite(image_path, face_img)
        
        # Construct the URL for the avatar
        avatar_url = f"http://{server_address}:8000/images/{image_filename}"

        face_img = FaceRecogSys.bytes_to_image(FaceRecogSys, row[5])
        emb = FaceRecogSys.bytes_to_emb(FaceRecogSys, row[6])
        
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
    conn = sqlite3.connect('database/face_db.db')
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

def get_user_history_list(page: int, page_size: int, from_date: str = None, to_date: str = None):
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    offset = (page - 1) * page_size

    query = "SELECT * FROM person_history_table"
    params = []
    if from_date and to_date:
        query += " WHERE time BETWEEN ? AND ?"
        params.extend([from_date, to_date])
    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, offset])

    cursor.execute(query, params)
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
        avatar_url = f"http://{server_address}:8000/images/{image_filename}"
        
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
    if from_date and to_date:
        cursor.execute("SELECT COUNT(*) FROM person_history_table WHERE time BETWEEN ? AND ?", (from_date, to_date))
    else:
        cursor.execute("SELECT COUNT(*) FROM person_history_table")
    total_items = cursor.fetchone()[0]
    # conn.close()
    cursor.close()
    return person_history_list, total_items

def get_admin_history_list(page: int, page_size: int, from_date: str = None, to_date: str = None):
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    offset = (page - 1) * page_size

    query = "SELECT * FROM user_history_table"
    params = []
    if from_date and to_date:
        query += " WHERE time BETWEEN ? AND ?"
        params.extend([from_date, to_date])
    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, offset])

    cursor.execute(query, params)
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

    if from_date and to_date:
        cursor.execute("SELECT COUNT(*) FROM user_history_table WHERE time BETWEEN ? AND ?", (from_date, to_date))
    else:
        cursor.execute("SELECT COUNT(*) FROM user_history_table")
    total_items = cursor.fetchone()[0]
    # conn.close()
    cursor.close()
    return admin_history_list, total_items
    
def get_similarity(emb1, emb2):
    dot = np.sum(np.multiply(emb1, emb2), axis=0)
    norm = np.linalg.norm(emb1, axis=0) * np.linalg.norm(emb2, axis=0)
    similarity = min(1, max(-1, dot / norm))
    cosdist = min(0.5, np.arccos(similarity) / math.pi)
    pcnt = 0
    thr = 0.35
    if cosdist <= thr:
        pcnt = (0.2 / thr) * cosdist
    elif cosdist > thr and cosdist <= 0.5:
        pcnt = 5.33333 * cosdist - 1.66667
    pcnt = (1.0 - pcnt) * 100
    pcnt = min(100, pcnt)
    return pcnt

def is_matching(encodding1, encodding2):
    if encodding1 is None or encodding2 is None:
        return False
    else:
        sim = get_similarity(encodding1, encodding2)
        if sim > 75:
            return True
        else:
            return False

person_register_list = get_user_register_list()

def find_person(img, emb):
    person_data = []
    person_data.append(img)
    person_data.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    global current_camera_action
    data = ['Unknown' for x in range(0, 17)]
    data[5] = cv2.imread('icons/face_icon.png')
    data[6] = emb
    person_data.append(data)
    person_data.append("Unknown")
    if current_camera_action == "ComeIn":
        current_camera_action == "ComeOut"
        person_data[-1] == "ComeOut"
    else:
        current_camera_action == "Unknown"
        person_data[-1] = "Unknown"
    for i in range(0, len(person_register_list)):
        emb0 = person_register_list[i]['emb'] # face embbeding value

        if is_matching(emb0, emb):
            data = person_register_list[i]
            person_data[2] = data
            person_data[-1] = "ComeIn"
            current_camera_action = "ComeIn"
            break

    return person_data

def proc_detected_faces(faces):
    person_data = []
    for img in faces:
        inp_img = img.copy()
        inp_img = cv2.resize(inp_img, (600, 500))
        faces = face_recognizer.predict(inp_img)
        if len(faces) > 0:
            emb = faces[0].embedding
            person_data = find_person(img, emb)
    return person_data


def generate_frames(camera):
    while True:
        camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        success, frame = camera.read()
        if not success:
            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            continue
        else:
            img, faces = face_detector.detect(frame)
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            threading.Thread(target=process_camera_analytics, args=(faces,)).start()
            # cam_frame = img.copy()
            # cam_faces = faces.copy()
            # if len(proc_detected_faces(cam_faces)) > 0:
            #     camera_analytics_data = proc_detected_faces(cam_faces)
            #     print(proc_detected_faces(cam_faces))

def process_camera_analytics(faces):
    # Process detected faces
    analytics_data = proc_detected_faces(faces)
    if len(analytics_data) > 0:

        camera_analytics_queue.put(analytics_data)
        # print(analytics_data)

        # connected_websockets[-1].send_text("afdwfw")
        # for websocket in connected_websockets:
        #     # print(websocket)
        #     await websocket.send_json(json.dumps('dta'))

@app.get("/camera-analytics")
async def get_camera_analytics():
    if not camera_analytics_queue.empty():
        analytics_data = camera_analytics_queue.get()
        _, buffer1 = cv2.imencode('.jpg', analytics_data[0])
        image_bytes1 = buffer1.tobytes()
        image_base1 = base64.b64encode(image_bytes1).decode('utf-8')
        _, buffer2 = cv2.imencode('.jpg', analytics_data[2][5])
        image_bytes2 = buffer2.tobytes()
        image_base2 = base64.b64encode(image_bytes2).decode('utf-8')
        face_img = analytics_data[0]
        face_bytes = cv2.imencode('.jpg', face_img)[1].tobytes()
        time = analytics_data[1]
        details = analytics_data[2]

        name = details[1]
        gender = details[7]
        age = details[3]
        place = details[13]
        view = '0'
        action = analytics_data[-1]

        # ----  save person to db --------
        try:
            conn = sqlite3.connect('database/face_db.db')
            cursor = conn.cursor()
            sqlite_insert_blob_query = """ INSERT INTO person_history_table
                    (name, gender, age, time, place, view, action, photo) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

            # Convert data into tuple format
            data_tuple = (name, gender, age, time, place, view, action, face_bytes)

            cursor.execute(sqlite_insert_blob_query, data_tuple)
            id = cursor.lastrowid
            conn.commit()
            print("Add new person history successfully.")
        except sqlite3.Error as error:
            print("Failed to add new person history.", error)
        person = {
            'id': analytics_data[2][0],
            'name': analytics_data[2][1],
            'birth': analytics_data[2][2],
            'age': analytics_data[2][3],
            'status': analytics_data[2][4],
            'firstPhoto': image_base1,
            'secondPhoto': image_base2,
            'gender': analytics_data[2][7],
            'guesttype': analytics_data[2][8],
            'safetytype': analytics_data[2][9],
            'blocked': analytics_data[2][10],
            'whenfrom': analytics_data[2][11],
            'whento': analytics_data[2][12],
            'place': analytics_data[2][13],
            'reason': analytics_data[2][14],
            'type': analytics_data[2][15],
            'info': analytics_data[2][16],
            'action': analytics_data[-1],
        }
        return JSONResponse(content=person)
    return JSONResponse(content={"message": "No analytics data available"})

def calc_age(birth_str):
    try:
        b_year = int(birth_str.split('.')[2])
        b_month = int(birth_str.split('.')[1].replace('0', ''))
        b_day = int(birth_str.split('.')[0].replace('0', ''))
        birth_date = date(b_year, b_month, b_day)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    except ValueError:
        return None


def id_detector(camera):
     while True:
        camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        success, frame = camera.read()
        if not success:
            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            continue
        else:
            mrz = mrz_reader.read_mrz(frame)
            if mrz is not None:
                try:
                    birth_date = mrz['date_of_birth']
                    year = int(birth_date[:2])

                    # birth_date = mrz['date_of_birth']
                    # year = int(birth_date[:2])

                    today = datetime.today()
                    current_year = int(str(today.year)[2:])

                    if year > current_year:
                        birth_year = 1900 + year
                    else:
                        birth_year = 2000 + year

                    card_birth = birth_date[4:] + '.' + birth_date[2:4] + '.' + str(birth_year)
                    # expire_date = mrz['date_of_expire']
                    real_age = calc_age(card_birth)
                    card_firstname = mrz['first_name'].translate(spcial_char_map)
                    card_lastname = mrz['last_name'].translate(spcial_char_map)
                    return {
                        'name': card_firstname + ' ' +  card_lastname,
                        'birth': card_birth,
                        'age': real_age,
                    }

                except ValueError:
                    pass


@app.get("/id-analytics")
async def get_id_analytics():
    user_data = id_detector(camera_1)
    return JSONResponse(content=user_data)


# @app.websocket("/ws/camera-analytics")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     connected_websockets.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_json(json.dumps('data'));
#     except WebSocketDisconnect:
#         connected_websockets.remove(websocket)


@app.get("/stream1")
async def camera1_stream():
    return StreamingResponse(generate_frames(camera_1), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/stream1/available")
async def camera1_stream_available():
    return "ok"

@app.get("/stream2")
async def camera2_stream():
    return StreamingResponse(generate_frames(camera_2), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/stream2/available")
async def camera2_stream_available():
    return "ok"

# @app.get("/stream3/available")
# async def camera3_stream_available():
#     return "false"

# @app.get("/stream4/available")
# async def camera4_stream_available():
#     return "false"


def get_admin_by_id(id):
    conn = sqlite3.connect('database/face_db.db')
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
    conn = sqlite3.connect('database/face_db.db')
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
        avatar_url = f"http://{server_address}:8000/images/{image_filename}"
        
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

# Users

@app.get('/api/users/get-admin')
async def allAdmins():
    users = get_admin_register_list()
    return JSONResponse(content=users)

@app.get('/api/users/get-admin/{id}')
async def singleAdmin(id: int):
    user = get_admin_by_id(id)
    if user:
        return JSONResponse(content=user)
    raise HTTPException(status_code=404, detail="User not found")

@app.post('/api/users/add-admin')
async def addAdmin(request: Request):
    data = await request.json()
    name = data.get('name')
    usergroup = data.get('usergroup')
    password = data.get('password')
    creator = data.get('creator')
    phone = data.get('phone')
    blocked = data.get('blocked')
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_register_table (name, usergroup, password, creator, phone, blocked) VALUES (?, ?, ?, ?, ?, ?)", 
                   (name, usergroup, password, creator, phone, blocked))
    id = cursor.lastrowid
    user = get_admin_by_id(id)
    conn.commit()
    
    return JSONResponse(content=user, status_code=201)

@app.put('/api/users/edit-admin/{id}')
async def editAdmin(id: int, request: Request):
    data = await request.json()
    name = data.get('name')
    usergroup = data.get('usergroup')
    password = data.get('password')
    creator = data.get('creator')
    phone = data.get('phone')
    blocked = data.get('blocked')
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_register_table SET name = ?, usergroup = ?, password = ?, creator = ?, phone = ?, blocked = ? WHERE id = ?", 
                   (name, usergroup, password, creator, phone, blocked, id))
    
    user = get_admin_by_id(id)
    conn.commit()
    
    return JSONResponse(content=user)

@app.delete('/api/users/delete-admin/{id}')
async def deleteAdmin(id: int):
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_register_table WHERE id = ?", (id,))
    conn.commit()
    
    return JSONResponse(content={"status": "success", "message": "Admin deleted successfully"})

@app.get('/api/users/get-user')
async def allUsers():
    users = get_user_register_list1()
    return JSONResponse(content=users)

@app.get('/api/users/get-user/{id}')
async def singleUser(id: int):
    user = get_user_by_id(id)
    if user:
        return JSONResponse(content=user)
    raise HTTPException(status_code=404, detail="User not found")

@app.post('/api/users/add-user')
async def addUser(request: Request):
    data = await request.json()
    name = data.get('name')
    image_path = f"{name}.jpg"
    pdf_path = f"{name}.pdf"
    real_image_path = os.path.join(STATIC_ROOT, 'images', image_path)
    real_pdf_path = os.path.join(STATIC_ROOT, 'images', pdf_path)
    if os.path.exists('resource/images/result.jpg'):
        if os.path.exists(real_image_path):
            os.remove(real_image_path)
            os.remove(real_pdf_path)
        os.rename('resource/images/result.jpg', real_image_path)
        os.rename('resource/images/result.pdf', real_pdf_path)
    birth = data.get('birth')
    age = data.get('age')
    status = data.get('status')
    face = data.get('avatar')
    header, encoded = face.split(",", 1)
    decoded_face = base64.b64decode(encoded)
    face_data = FaceRecogSys.bytes_to_image(FaceRecogSys, decoded_face)
    res = face_recognizer.predict(face_data)

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
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    sqlite_insert_blob_query = """ INSERT INTO person_register_table
    (name, birth, age, status, photo, emb, gender, guesttype, safetytype, blocked, whenfrom, whento, place, reason, type, info) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    data_tuple = (name, birth, age, status, decoded_face, emb_bytes, gender, guesttype, safetytype, blocked, whenfrom, whento, place, reason, type, info)

    cursor.execute(sqlite_insert_blob_query, data_tuple)
    id = cursor.lastrowid
    user = get_user_by_id(id)
    conn.commit()
    
    return JSONResponse(content=user, status_code=201)

@app.put('/api/users/edit-user/{id}')
async def editUser(id: int, request: Request):
    data = await request.json()
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_register_table WHERE id = ?", (id,))
    row = cursor.fetchone()
    name = data.get('name')
    image_path = f"{name}.jpg"
    pdf_path = f"{name}.pdf"
    real_image_path = os.path.join(STATIC_ROOT, 'images', image_path)
    real_pdf_path = os.path.join(STATIC_ROOT, 'images', pdf_path)
    if os.path.exists('resource/images/result.jpg'):
        if os.path.exists(real_image_path):
            os.remove(real_image_path)
            os.remove(real_pdf_path)
        os.rename('resource/images/result.jpg', real_image_path)
        os.rename('resource/images/result.pdf', real_pdf_path)
    birth = data.get('birth')
    age = data.get('age')
    status = data.get('status')
    face = data.get('avatar')
    
    if isinstance(face, str) and 'http' in face:
        face_bytes = row[5]
        emb_bytes = row[6]
    else:
        header, encoded = face.split(",", 1)
        face_bytes = base64.b64decode(encoded)
        print(face_bytes)
        face_data = FaceRecogSys.bytes_to_image(FaceRecogSys, face_bytes)
        res = face_recognizer.predict(face_data)
        print(res)
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

    sqlite_insert_blob_query = """ UPDATE person_register_table SET
            name = ?, birth = ?, age = ?, status = ?, photo = ?, emb = ?, gender = ?, guesttype = ?, 
            safetytype = ?, blocked = ?, whenfrom = ?, whento = ?, place = ?, reason = ?, type = ?, info = ? 
            WHERE id = ?"""

    data_tuple = (name, birth, age, status, face_bytes, emb_bytes, gender, guesttype, safetytype, blocked,
                    whenfrom, whento, place, reason, type, info, id)

    cursor.execute(sqlite_insert_blob_query, data_tuple)
    user = get_user_by_id(id)
    conn.commit()
    
    return JSONResponse(content=user)

@app.delete('/api/users/delete-user/{id}')
async def deleteUser(id: int):
    conn = sqlite3.connect('database/face_db.db')
    cursor = conn.cursor()
    sqlite_insert_blob_query = """ DELETE from person_register_table WHERE id=?"""

    cursor.execute(sqlite_insert_blob_query, (id,))
    conn.commit()
    
    return JSONResponse(content={"status": "success", "message": "User deleted successfully"})

@app.get('/api/users/admin-history')
async def adminHistory(
    page: int = Query(1, alias="page"),
    page_size: int = Query(10, alias="pageSize"),
    from_date: str = Query(None, alias="from"),
    to_date: str = Query(None, alias="to")
):
    history, total_items = get_admin_history_list(page, page_size, from_date, to_date)
    return JSONResponse(
        content={
            "result": history,
            "pagination": {
                "totalItems": total_items,
                "pageSize": page_size,
                "page": page,
                "totalPages": (total_items + page_size - 1) // page_size,
            }
        }
    )

@app.get('/api/users/user-history')
def user_history(
    page: int = Query(1, alias="page"),
    page_size: int = Query(10, alias="pageSize"),
    from_date: str = Query(None, alias="from"),
    to_date: str = Query(None, alias="to")
):
    history, total_items = get_user_history_list(page, page_size, from_date, to_date)
    return JSONResponse(
        content={
            "result": history,
            "pagination": {
                "totalItems": total_items,
                "pageSize": page_size,
                "page": page,
                "totalPages": (total_items + page_size - 1) // page_size,
            }
        }
    )

# Auth

@app.post('/api/auth/login')
async def login(request: Request, response: Response):
    try:
        login_data = await request.json()
        username = login_data.get('username')
        password = login_data.get('password')

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")
        conn = sqlite3.connect('database/face_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_register_table WHERE name=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.commit()

        if user:
            conn = sqlite3.connect('database/face_db.db')
            cursor = conn.cursor()
            name = user[1]
            action = 'Log in'
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = ''

            # ----  save person to db --------
            try:
                sqlite_insert_blob_query = """ INSERT INTO user_history_table
                                (name, action, time, content) 
                                VALUES (?, ?, ?, ?)"""

                # Convert data into tuple format
                data_tuple = (name, action, time, content)
                print(data_tuple)

                cursor.execute(sqlite_insert_blob_query, data_tuple)
                conn.commit()
                print("Add new person history successfully.")

            except sqlite3.Error as error:
                print("Failed to add new person history.", error)

            response.set_cookie(key="account", value=json.dumps({"username": username}), httponly=True, max_age=3600)
            return JSONResponse(content={"message": "Login successful", "user": {"id": user[0], "name": user[1], "usergroup": user[2], "password": user[3], "creator": user[4], "phone": user[5], 'blocked': user[6], 'permission': 'admin'}})
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/auth/logout')
async def logout(response: Response):
    response.delete_cookie(key="account")
    return JSONResponse(content={"status": "success", "message": "Logged out successfully."})

@app.post('/api/signature')
async def signature(request: Request):
    signature_data = await request.json()
    data = signature_data.get('data')
    
    header, encoded = data.split(",", 1)
    data = base64.b64decode(encoded)

    FaceRecogSys.sign_capture_btn_clicked_with_image(FaceRecogSys, data)
    return JSONResponse(content={"data": f"http://{server_address}:8000/images/result.jpg"})

@app.get('/images/{filename}')
async def serve_image(filename: str):
    file_path = os.path.join(STATIC_ROOT, 'images', filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
        #return FileResponse(file_path, headers={'Cache-Control': 'public, max-age=31536000', 'Last-Modified': time.ctime(os.path.getmtime(file_path))})
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    # Start the first script
    first_script_process = subprocess.Popen(['python', 'app.py'])

    import uvicorn
    uvicorn.run(app, host=server_address, port=8000)

    first_script_process.wait()
    
