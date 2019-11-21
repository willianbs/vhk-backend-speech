import os
import urllib.request
from app import app
from flask import Flask, request, redirect, make_response, jsonify
from werkzeug.utils import secure_filename
import urllib.error
import re
import sys
import time
import pipes
import uuid

# Speak rating
import myspsolution as mysp

ALLOWED_EXTENSIONS = set(['mp4', 'webm'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cors_route(path, origin=('127.0.0.1'), **options):
    def inner(func):
        def wrapper(*args, **kwargs):
            if request.method == 'OPTIONS':
                response = make_response()
                response.headers.add(
                    "Access-Control-Allow-Origin", ', '.join(origin))
                response.headers.add(
                    'Access-Control-Allow-Headers', ', '.join(origin))
                response.headers.add(
                    'Access-Control-Allow-Methods', ', '.join(origin))
                return response
            else:
                result = func(*args, **kwargs)
            if 'Access-Control-Allow-Origin' not in result.headers:
                result.headers.add(
                    "Access-Control-Allow-Origin", ', '.join(origin))
            return result

        wrapper.__name__ = func.__name__

        if 'methods' in options:
            if 'OPTIONS' in options['methods']:
                return app.route(path, **options)(wrapper)
            else:
                options['methods'].append('OPTIONS')
            return app.route(path, **options)(wrapper)

        return wrapper

    return inner


@cors_route('/file-upload', methods=['POST'], origin=['*'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_name = uuid.uuid4().hex
        fName = new_name
        new_name = new_name + '.webm'
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        file.save(filePath)

        # convert video to audio
        try:
            file_name, file_extension = os.path.splitext(filePath)
            file_name = pipes.quote(file_name)
            # ffmpeg -i FILE.EXT -ar 44000 -acodec pcm_s16le DEST.EXT
            # video_to_wav = 'ffmpeg -hide_banner -nostats -loglevel 0 -i ' + file_name + file_extension + \
            #     ' -ar 44000 -acodec pcm_s16le -af lowpass=1000,highpass=200 ' + file_name + '.wav'
            video_to_wav = 'ffmpeg -hide_banner -nostats -loglevel 0 -i ' + file_name + file_extension + \
                ' -ar 44000 -acodec pcm_s16le ' + file_name + '.wav'
            # final_audio = 'lame ' + file + '.wav' + ' ' + file + '.mp3'
            os.system(video_to_wav)
            # os.system(final_audio)
            # file=pipes.quote(file)
            os.remove(file_name + file_extension)
            time.sleep(1)

            # Analyse audio
            # mysp.myspgend(fName, app.config['UPLOAD_FOLDER'])
            score = mysp.mysppron(fName, app.config['UPLOAD_FOLDER'])

            resp = jsonify(
                {'message': 'File successfully uploaded', 'file': filePath, 'result': score})
            resp.status_code = 201
        except OSError as err:
            # print(err.reason)
            resp = jsonify({'message': err.reason})
            resp.status_code = 500
        return resp
    else:
        resp = jsonify(
            {'message': 'Allowed file types are: mp4 or webm'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
