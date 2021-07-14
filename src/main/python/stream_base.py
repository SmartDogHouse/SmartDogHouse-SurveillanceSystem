import cv2
from flask import Flask, render_template, render_template_string, Response

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

def gen():    
    while True:
        ret, image = video_capture.read()
        cv2.imwrite('frame.jpg', image)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('frame.jpg', 'rb').read() + b'\r\n')
    video_capture.release()


@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')
    # da stringa: return render_template_string('''<html></html>''')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0")  # exposes at the inner net the server with port default 5000
