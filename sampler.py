import base64
import boto3
import cv2
import datetime
import json
import pytz

kinesis_client = boto3.client("kinesis", region_name='us-east-1')

def process_video(url, rate, stream, partition):
    # frame
    frame_count = 0
    capture_rate = 30

    cap = cv2.VideoCapture(url)

    while (True):

        # cframe = cap.get(cv2.CV_CAP_PROP_POS_FRAMES) # retrieves the current frame number
        # tframe = cap.get(cv2.CV_CAP_PROP_FRAME_COUNT) # get total frame count
        # fps = cap.get(cv2.CV_CAP_PROP_FPS)  #get the FPS of the videos
        #
        # print(cframe)
        # print(tframe)
        # print(fps)
        # time = cframe / fps

        # print(time)

        # reading from frame
        ret, frame = cap.read()

        if ret:

            if frame_count % capture_rate == 0:
                print('Reading frame....')

                utc_dt = pytz.utc.localize(datetime.datetime.now())
                now_ts_utc = (utc_dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

                retval, buffer = cv2.imencode('.jpg', frame)
                data = {
                    'Timestamp': now_ts_utc,
                    'Image': base64.b64encode(buffer),
                    'User': 'test123'
                }
                jpg_as_text = base64.b64encode(json.dumps(data))

                # put encoded image in kinesis stream
                print("Sending image to Kinesis....")
                response = kinesis_client.put_record(
                    StreamName=stream,
                    Data=jpg_as_text,
                    PartitionKey=partition
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
