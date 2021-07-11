# import the opencv library
import cv2

print("GPU Enabled: {}".format(cv2.cuda.getCudaEnabledDeviceCount()))

# Look for devices
arr = []
for index in range(0, 4):
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        arr.append(index)
    cap.release()

if len(arr) > 0:
    print("Device number {} , selecting first".format(arr))
    index = arr[0]  # select first
    # define a video capture object
    vid_cap = cv2.VideoCapture(0)

    while True:

        # Capture the video frame by frame
        ret, frame = vid_cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid_cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

else:
    print("No devices found")
