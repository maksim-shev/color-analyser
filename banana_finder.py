import cv2
import sys
import glob
import time
import threading
import numpy as np


def bananasFinder():
    for img in glob.glob("src/*.jpg"):
        faceCascade = cv2.CascadeClassifier('banana_classifier.xml')

        # Capture frame-by-frame
        frame = cv2.imread(img)
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            continue
        kernel = np.ones((9, 9), np.uint8)
        closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #cv2.rectangle(closing, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_color = frame[y:y + h, x:x + w]
            print("[INFO] Object found. Saving locally.")
            cv2.imshow('Video', frame)
            cv2.waitKey(50)
            cv2.imwrite('bananas\\'+str(w) + str(h) +
                        '_bananas.jpg', roi_color)
        # Display the resulting frame
        cv2.destroyAllWindows()
    


if __name__ == "__main__":
    bananasFinder()
