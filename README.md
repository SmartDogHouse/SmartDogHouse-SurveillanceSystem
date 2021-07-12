# SmartDogHouse-SurveillanceSystem
Software for surveillance. Uses OpenCV for capturing video, running Object-Detection, sending MQTT message for anomalies, streaming video.

![smart doghouse logo](./src/main/python/output/dogs_S.png "Smart DogHouse Logo")

## Install OpenCV
```bash
sudo apt-get install python3-opencv
```

test with
```bash
import cv2
```
## Install ffmpeg
```bash
sudo apt install ffmpeg
```

if you are using VirtualBox add usb device :
devices -> usb -> settings -> add -> select your camera.

test it with ffmplay
```bash
ffmplay /dev/video0
```
## Install gstreamer

```bash
sudo apt-get install python3-gi
sudo apt-get install gir1.2-gst-rtsp-server-1.0
http://lifestyletransfer.com/how-to-install-gstreamer-on-ubuntu/
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-dev gstreamer1.0-tools gstreamer1.0-doc
sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good 
sudo apt-get install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly 
sudo apt-get install gstreamer1.0-libav
sudo apt-get install gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```
check if it's working
```bash
gst-launch-1.0 videotestsrc ! autovideosink
```


The library is compiled without QT support in function 'displayOverlay
```bash
pip install open
```
