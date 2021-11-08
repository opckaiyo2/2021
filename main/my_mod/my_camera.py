import cv2
import numpy as np
import sys
 
def cap_main(cap_flag,X,Y,S):
    try:
        camera = cv2.VideoCapture(0)                # カメラCh.(ここでは0)を指定
        cap_flag.value = 0
        
        # 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
        while True:
            ret, frame = camera.read()              # フレームを取得
            #cv2.imshow('camera', frame)             # フレームを画面に表示

            hsvLower = np.array([0, 90, 95])    # 抽出する色の下限(HSV)
            hsvUpper = np.array([20, 200, 200])    # 抽出する色の上限(HSV)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # 画像をHSVに変換
            hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)    # HSVからマスクを作成
            #result = cv2.bitwise_and(frame, frame, mask=hsv_mask) # 元画像とマスクを合成
            #cv2.imshow('hsv', result)             # フレームを画面に表示     

            # 8近傍
            neiborhood8 = np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]],np.uint8)
            #収縮
            img_erosion = cv2.erode(hsv_mask,neiborhood8,iterations=15)
            #cv2.imshow('close', img_erosion)                    
            #膨張
            img_dilation = cv2.dilate(img_erosion,neiborhood8,iterations=15)
            #cv2.imshow('open', img_dilation)           

            # ラベリング処理(詳細版)
            label = cv2.connectedComponentsWithStats(img_dilation)

            # オブジェクト情報を項目別に抽出
            n = label[0] - 1
            data = np.delete(label[2], 0, 0)
            center = np.delete(label[3], 0, 0)

            # ラベリング結果書き出し用に二値画像をカラー変換
            color_src = cv2.cvtColor(img_dilation, cv2.COLOR_GRAY2BGR)

            # オブジェクト情報を利用してラベリング結果を表示
            for i in range(n):
                # 各オブジェクトの外接矩形を赤枠で表示
                if data[i][4] >= 1000:

                    S.value = int(data[0][4])
                    X.value = int(center[0][0])
                    Y.value = int(center[0][1])
                    cap_flag.value = 1

                    x0 = data[i][0]
                    y0 = data[i][1]
                    x1 = data[i][0] + data[i][2]
                    y1 = data[i][1] + data[i][3]
                    cv2.rectangle(color_src, (x0, y0), (x1, y1), (0, 0, 255))

                    # 各オブジェクトのラベル番号・面積・中心座標を黄文字で表示
                    cv2.putText(color_src, "ID: " +str(i + 1), (x0, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
                    cv2.putText(color_src, "S: " +str(data[i][4]), (x0, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
                    cv2.putText(color_src, "X: " +str(int(center[i][0])), (x0, y1 + 45), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
                    cv2.putText(color_src, "Y: " +str(int(center[i][1])), (x0, y1 + 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

                    #cv2.imshow('label', color_src) 

            # キー操作があればwhileループを抜ける
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            k = cv2.waitKey(1) & 0xFF
            if k == 27:         # wait for ESC key to exit
                cv2.destroyAllWindows()
                break
        
        # 撮影用オブジェクトとウィンドウの解放
        camera.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print("my_camera.py cap_main try error : ",e)
        print("\n")

if __name__ == "__main__":
    cap_main(0)