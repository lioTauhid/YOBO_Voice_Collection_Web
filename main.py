import uuid
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import base64
import os

from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
WEB_APP_DIR = 'templates'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<path:name>')
def return_web_file(name):
    """Helper function to render static web page"""
    dataList = str(name).split('/')
    DIR_NAME = WEB_APP_DIR

    if len(dataList) > 1:
        for i in range(0, len(dataList) - 1):
            DIR_NAME += '/' + dataList[i]

    return send_from_directory(DIR_NAME, dataList[-1])


@app.route('/audio', methods=['POST'])
def uploadAudioFile():
    data = request.get_json(force=True)["audioFile"]
    wav_file = open(f"audio-files/{uuid.uuid4().hex}.wav", "wb")
    decode_string = base64.b64decode(data)
    wav_file.write(decode_string)
    resp = jsonify({'message': 'File successfully uploaded'})
    resp.status_code = 200
    return resp


@app.route('/audio', methods=['GET'])
def allAudioFiles():
    fileNames = os.listdir("audio-files")
    resp = jsonify({"messageFilenames": fileNames})
    resp.status_code = 200
    return resp


@app.route('/play/<path:filename>')
def play_file(filename):
    return send_from_directory('audio-files/', filename)


@app.route('/totalFiles')
def totalFiles():
    filesCount = len(os.listdir("audio-files"))
    print(filesCount)
    return jsonify({'totalFiles': filesCount})


@app.route('/saveUser', methods=['POST'])
def saveUser():
    data = request.get_json(force=True)
    user = User(data['userName'], data['email'], data['phone'], 'no address')
    db.session.add(user)
    db.session.commit()
    return jsonify({'info': 'user saved'})


@app.route('/users', methods=['GET'])
def getUsers():
    dataList = User.query.all()
    userList = []
    for user in dataList:
        userList.append({
            'userName': user.name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
        })
    return jsonify(userList)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('userName', db.String(100))
    email = db.Column('email', db.String(50))
    phone = db.Column('phone', db.String(50))
    address = db.Column('address', db.String(200))

    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("failed email validation")
        return address

    # @validates('address')
    # def validate_address(self, key, address):
    #     if len(address) < 4:
    #         raise ValueError("failed address validation")
    #     return address

    @validates('name')
    def validate_name(self, key, address):
        if len(address) < 2:
            raise ValueError("failed userName validation")
        return address


if __name__ == "__main__":
    app.run()
