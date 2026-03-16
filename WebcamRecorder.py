import cv2 as cv

webcam = cv.VideoCapture(0)
isblacked = False
isrecording = False
isnegative = False
ismirror = False
frame_count = 0
video = cv.VideoWriter()

if webcam.isOpened():
    fps = webcam.get(cv.CAP_PROP_FPS)
    wait_msec = max(1, int(1000 / fps))

    while True:
        valid, img = webcam.read()
        if not valid:
            print("invalid")
            break

        display_img = img
        record_img = img
        
        if isblacked:
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            display_img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
            record_img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
        
        if isnegative:
            display_img = 255-display_img
            record_img = 255-record_img

        if ismirror:
            display_img = cv.flip(display_img, 1)
            record_img = cv.flip(record_img, 1)

        if isrecording:
            elapsed = int(frame_count / fps)
            mm = elapsed // 60
            ss = elapsed % 60
            cv.circle(display_img, (30, 30), 10, (0, 0, 255), -1)
            cv.putText(display_img,f"REC {mm:02d}:{ss:02d}",(50, 36),cv.FONT_HERSHEY_SIMPLEX,fontScale = 0.8,color = (0, 0, 255),thickness=2)

        cv.imshow('Webcam Player', display_img)

        if isrecording and not video.isOpened():
            h, w, *_ = img.shape
            video.open('recorded video.avi', cv.VideoWriter_fourcc(*'XVID'), fps, (w, h), True)

        if isrecording:
            video.write(record_img)
            frame_count += 1

        key = cv.waitKey(wait_msec)
        if key == 27:
            break
        elif key == ord('b'):
            if isblacked:
                isblacked = False
            else:
                isblacked = True
        elif key == ord('r'):
            if isrecording:
                isrecording = False
            else:
                isrecording = True
        elif key == ord('n'):
            if isnegative:
                isnegative = False
            else:
                isnegative = True
        elif key == ord('m'):
            if ismirror:
                ismirror = False
            else:
                ismirror = True

    webcam.release()
    video.release()
    cv.destroyAllWindows()