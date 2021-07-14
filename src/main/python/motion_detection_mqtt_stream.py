#!/usr/bin/env python3

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from secret import PATH_TO_CERT, PATH_TO_ROOT, PATH_TO_KEY, MQTT_PORT, MQTT_CLIENT_ID, MQTT_HOST, MQTT_RECEIVE_TOPIC, MQTT_NOTIFY_TOPIC
from mqtt_manager import MQTTManager
from flask import Flask, render_template, render_template_string, Response

app = Flask(__name__)
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

mqtt_manager = MQTTManager(cert_path=PATH_TO_CERT, key_path=PATH_TO_KEY,  root_path=PATH_TO_ROOT, port=MQTT_PORT, client_id=MQTT_CLIENT_ID,
                           server=MQTT_HOST)
try:
    mqtt_manager.connect()
except Exception as e:
    print('Cannot connect MQTT: ' + str(e))


vs = cv2.VideoCapture(0)

def gen():
    # initialize the first frame in the video stream
    referenceFrame = None
    time_sent = time.time()
    previous_notification_sent = time.time()
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        frame = frame[1]
        if frame is None:
            break
        # if the frame could not be grabbed, then we have reached the end of the video
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        # more than 5 sec set current frame as reference
        if time.time()-time_sent > 5:
            time_sent = time.time()
            referenceFrame = gray_frame
        # if the first frame is None, initialize it
        if referenceFrame is None:
            referenceFrame = gray_frame
            continue
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(referenceFrame, gray_frame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        text = "no detection"
        # loop over the contours
        for c in cnts:
            # if the contour area is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue
            # DETECTION
            if time.time() - previous_notification_sent > 5:
                # sent notify if enough time passed since the last one
                previous_notification_sent = time.time()
                msg = {"Notify": "Security breach detection"}
                mqtt_manager.send_msg(topic=MQTT_NOTIFY_TOPIC, msg=msg)
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Detected"
        # draw the text and timestamp on the frame
        cv2.putText(frame, "Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # show the frame and record if the user presses a key_path
        # stream frame
        cv2.imwrite('frame.jpg', frame)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('frame.jpg', 'rb').read() + b'\r\n')
        #cv2.imshow("Security Feed", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)

    # cleanup the camera and close any open windows
    vs.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0")  # exposes at the inner net the server with port default 5000
