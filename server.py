from flask import Flask, request, jsonify
from sampler import process_video
import json
import base64
import boto3
import cv2
import datetime
import json
import pytz

app = Flask(__name__)

@app.route('/process', methods = ['POST'])
def process():
    request_data = request.get_json()
    try:
        url = request_data['url']
        rate = request_data['rate']
        kinesis_stream = request_data['stream']
        partition = request_data['partition']
        process_video(url, rate, kinesis_stream, partition)
        return 'Success'
    except KeyError:
        errMsg = "url, rate, stream, partition must be defined"
        print(errMsg)
        return errMsg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
