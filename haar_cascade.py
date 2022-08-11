import cv2 as cv
from TrackerClass import *

if __name__ == "__main__":
    path = "haarcascade_frontalface_default.xml"
    detector = cv.CascadeClassifier(path)

    object_tracker = Tracker()

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)
        gray = cv.GaussianBlur(gray, (3, 3), -1)

        # results: (x,y,w,h): x, y: top left corner; w, h: width, height
        results = detector.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=5,
            minSize=(30, 30), flags=cv.CASCADE_SCALE_IMAGE)

        if len(results) != 0:
            center_list = []
            for x, y, w, h in results:
                center = (x + w // 2, y + h // 2)
                center_list.append(center)
                frame = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            centerofobjects = object_tracker.update_centers(center_list)
            # print(centerofobjects)
            # print(Tracker.sNumofObjects)
            object_tracker.draw_centers(frame)

        # Display the resulting frame
        cv.imshow('frame', frame)

        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
