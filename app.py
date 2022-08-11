from models.database import Database
from models.student import Student

from flask_cors import CORS
from flask import Flask, render_template, request
import socketio

Database.instance()

sio = socketio.Server(async_mode='threading')
app = Flask(__name__)
CORS(app)

app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

student_service = Student()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student/')
def get_students():
    students = student_service.get_all()
    return render_template('student.html', students = students)

@app.route('/bus/')
def get_bus():
    return render_template('bus.html')

@app.route('/student/check-code/', methods=['PUT'])
def check_code():
    code = request.json['code']
    sio.emit('code', code, broadcast=True)
    found_student = student_service.find_by_code(code)
    if found_student:
        student_service.update_status(found_student)
    response = True if found_student else False
    return { 'exist': response }

@app.route('/student/', methods=['POST'])
def new_student():
    message = { 'message': 'Todos los campos de entrada son obligatorios'}
    try:
        content = request.form
        code = request.form['code']
        fullname = request.form['fullname']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if code and fullname and latitude and longitude:            
            if student_service.exist_with_code(code):
                message = { 'message': 'El código ya se encuentra registrado'}
            else:
                student_service.create_student(int(code), fullname, float(latitude), float(longitude))
                message = { 'message': 'Estudiante registrado!'}
    except:
        pass
    students = student_service.get_all()
    return render_template('student.html', message = message, students = students)

@app.route('/bus/position/', methods=['PUT'])
def update_position():
    position = request.json['position']
    data = position.split(',')
    latitude = float(data[1])/100
    latitude = int(latitude) + ((latitude % 1) * 100) / 60
    if data[2] == 'S':
        latitude = latitude * -1
    longitude = float(data[3])/100
    longitude = int(longitude) + ((longitude % 1) * 100) / 60
    if data[4] == 'W':
        longitude = longitude * -1
    sio.emit('position', {'lat': latitude, 'lng': longitude })
    return {'message': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')