import uuid
from flask import Flask, jsonify, request, render_template, send_from_directory
import base64
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


##################################################################################

@app.route('/')
def home():
    return render_template('index.html')


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


####################################################################################
if __name__ == "__main__":
    app.run()
