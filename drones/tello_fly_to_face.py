from djitellopy import Tello
import cv2
import sys
import numpy as np
import time

def initializeDrone() -> Tello:
    drone = Tello()
    print("connecting")
    drone.connect()
    print("connected")
    
    drone.for_back_velocity = 0
    drone.left_right_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.speed = 0
    
    print(drone.get_battery())
    drone.streamoff()
    drone.streamon()
    return drone

def getFrame(drone, width = 360, heigh = 240):
    frame = drone.get_frame_read()
    return cv2.resize(frame.frame,(width,heigh))


def findFace(frame):
    cascadePath = "resources/haarcascade_frontalface_default.xml"
    cascadeClassifier = cv2.CascadeClassifier(cascadePath)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascadeClassifier.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(30, 30)
    )

    facesAres = []
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        facesAres.append((x, y, w, h))
    
    return frame, facesAres

def main() -> int:
    drone = initializeDrone()

    current = drone.get_barometer()
    drone.get_frame_read

    max_height = current + 200
    img = getFrame(drone, 720, 360)
    
    time.sleep(3)
    drone.takeoff()
    print("took off")
    while drone.get_barometer() < max_height:
        x_speed = 0 # drone.get_acceleration_x()
        y_speed = 0 # drone.get_acceleration_y()
        print("x_speed: " + str(x_speed) + " y_speed: " + str(y_speed))

        img_orig = getFrame(drone, 720, 360)
        (img, area) = findFace(img_orig)
        print(area)
        
        if len(area) == 0:
            drone.send_rc_control(-x_speed, -y_speed, 40, 0)
            time.sleep(0.5)
            cv2.imshow('Image',img)
            continue

        (x, y, w, h) = area[0]
        if x < 200:
            drone.send_rc_control(-x_speed, -y_speed, 40, 0)
            time.sleep(0.5)
            cv2.imshow('Image',img)
            continue
        
        cv2.imwrite("my_face_org.jpg", img_orig)
        cv2.imwrite("my_face.jpg", img)
        time.sleep(2)
        break

    cv2.destroyAllWindows()
    drone.land()


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit