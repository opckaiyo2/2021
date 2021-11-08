import cv2
import numpy as np

def nothing(x):
    pass
 
camera = cv2.VideoCapture(0)                # カメラCh.(ここでは0)を指定
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.createTrackbar('minH', 'image', 0, 255, nothing)
cv2.createTrackbar('maxH', 'image', 0, 255, nothing)
cv2.createTrackbar('minS', 'image', 0, 255, nothing)
cv2.createTrackbar('maxS', 'image', 0, 255, nothing)
cv2.createTrackbar('minV', 'image', 0, 255, nothing)
cv2.createTrackbar('maxV', 'image', 0, 255, nothing)
 
# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    ret, frame = camera.read()              # フレームを取得
    cv2.imshow('camera', frame)             # フレームを画面に表示

    #hsvLower = np.array([90,100,0])    # 抽出する色の下限(HSV)
    #hsvUpper = np.array([100,150,255])    # 抽出する色の上限(HSV)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # 画像をHSVに変換
    #hsv2 = cv2.blur(hsv,(40,40))
    #cv2.imshow('hsv2', hsv2)             # フレームを画面に表示
    
    minH = cv2.getTrackbarPos('minH', 'image')
    maxH = cv2.getTrackbarPos('maxH', 'image')
    minS = cv2.getTrackbarPos('minS', 'image')
    maxS = cv2.getTrackbarPos('maxS', 'image')
    minV = cv2.getTrackbarPos('minV', 'image')
    maxV = cv2.getTrackbarPos('maxV', 'image')
    
    hsv_mask = cv2.inRange(hsv, np.array([minH, minS, minV]), np.array([maxH, maxS, maxV]))    # HSVからマスクを作成
    #hsv_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([255, 255, 255]))    # HSVからマスクを作成
    #result = cv2.bitwise_and(frame, frame, mask=hsv_mask) # 元画像とマスクを合成
    #cv2.imshow('hsv', result)             # フレームを画面に表示     

    # 8  ^q ^b^m ^a   ^z   
    neiborhood8 = np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]],np.uint8)
    ######### 8  ^q ^b^m ^a      ^o ^g  ^p^f
    img_erosion = cv2.erode(hsv_mask,neiborhood8,iterations=20)
    #cv2.imshow('close', img_erosion)                 
    ######### 8  ^q ^b^m ^a  ^f     ^g  ^p^f
    img_dilation = cv2.dilate(img_erosion,neiborhood8,iterations=20)
    #cv2.imshow('open', img_dilation)          
    cv2.imshow('close', img_dilation)                 


    # キー操作があればwhileループを抜ける
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
        break
 
# 撮影用オブジェクトとウィンドウの解放
camera.release()
cv2.destroyAllWindows()
