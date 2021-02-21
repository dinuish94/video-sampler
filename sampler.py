import numpy as np
import cv2
import base64
import pickle
import datetime
import boto3
import os
import pytz
import json

kinesis_client = boto3.client("kinesis")
cap = cv2.VideoCapture(0)

# frame
frame_count = 0
capture_rate = 30

while(True):
    # reading from frame
    ret,frame = cap.read()

    if ret:

        if frame_count % capture_rate == 0:

            print ('Reading frame....')

            utc_dt = pytz.utc.localize(datetime.datetime.now())
            now_ts_utc = (utc_dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

            retval, buffer = cv2.imencode('.jpg', frame)
            data = {
                'Timestamp' : now_ts_utc,
                'Image' : base64.b64encode(buffer),
                'User' : 'test123'
            }
            jpg_as_text = base64.b64encode(json.dumps(data))

            #put encoded image in kinesis stream
            print("Sending image to Kinesis....")
            response = kinesis_client.put_record(
                StreamName="FrameInputStream",
                Data=jpg_as_text,
                PartitionKey="0"
            )
            print("Received response from kinesis {}".format(response))

        # increasing counter so that it will
        # show how many frames are created
        frame_count += 1
    else:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
