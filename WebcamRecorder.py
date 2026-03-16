import cv2 as cv

# 컴퓨터에 달려있는 웹캠 사용
webcam = cv.VideoCapture(0)

# 모드를 위한 bool 변수 선언
isblacked = False   # 흑백
isrecording = False # 녹화
isnegative = False  # 보색화
ismirror = False    # 거울모드

frame_count = 0     # 프레임 수    
video_index = 0     # 여러 비디오 저장을 위한 인덱스 변수

video = cv.VideoWriter()

if webcam.isOpened():

    fps = webcam.get(cv.CAP_PROP_FPS)
    wait_msec = max(1, int(1000 / fps))

    while True:
        valid, img = webcam.read()
        if not valid:
            print("invalid")
            break

        # 빨간 원, 시간 출력을 위해 이미지 변수 구분
        display_img = img   # 화면 출력용 이미지변수
        record_img = img    # 녹화용 이미지변수

        
        if isblacked:   # 흑백모드일 때
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            display_img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
            record_img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
        
        if isnegative:  # 보색모드일 때
            display_img = 255-display_img
            record_img = 255-record_img

        if ismirror:    # 거울모드일 때
            display_img = cv.flip(display_img, 1)
            record_img = cv.flip(record_img, 1)

        if isrecording and not video.isOpened():    # 녹화 시작 시 비디오 파일 열기
            h, w, *_ = img.shape
            videoname = f'recorded video_{video_index}.avi'
            video.open(videoname, cv.VideoWriter_fourcc(*'XVID'), fps, (w, h), True)
            video_index +=1

        if isrecording: # 녹화모드일 때 텍스트, 빨강 원 출력
            elapsed = int(frame_count / fps)
            mm = elapsed // 60
            ss = elapsed % 60
            cv.circle(display_img, (30, 30), 10, (0, 0, 255), -1)
            cv.putText(display_img,f"REC {mm:02d}:{ss:02d}",(50, 36),cv.FONT_HERSHEY_SIMPLEX,fontScale = 0.8,color = (0, 0, 255),thickness=2)
            if video.isOpened():
                video.write(record_img)
                frame_count += 1

        cv.imshow('Webcam Player', display_img)

        key = cv.waitKey(wait_msec)
        if key == 27:               # ESC 입력시 비디오 저장 후 종료
            if isrecording:
                video.release()
            break

        elif key == ord('b'):       # b 입력시 흑백모드 전환
            if isblacked:
                isblacked = False
            else:
                isblacked = True

        elif key == ord(' '):       # 스페이스 입력시 녹화모드 전환
            if isrecording:
                isrecording = False
                video.release()
            else:
                isrecording = True
                frame_count = 0
                
        elif key == ord('n'):       # n 입력시 보색모드 전환
            if isnegative:
                isnegative = False
            else:
                isnegative = True

        elif key == ord('m'):       # m 입력시 거울모드 전환
            if ismirror:
                ismirror = False
            else:
                ismirror = True

    webcam.release()
    cv.destroyAllWindows()