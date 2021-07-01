import datetime

def log_txt(ard_data, gps_data):
    # log作成時刻がファイル名のファイル作成
    filiname = "/home/pi/2021/main/log" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt") 
    # 同じデータを書き込まないように前ループのデータ保管用変数
    old_ard_data = ""
    
    try:
        # オブジェクトの作成
        # with文は終了時に必要な処理を補完してくれる文 今回はfileを保存して終了をしてくれる
        with open(filiname, 'a') as f:
            while(True):
                # 同じデータを書き込もうとしてないかチェック
                if(old_ard_data != ard_data):
                    # gpsとセンサデータを統合
                    ard_data["lat"] = gps_data["lat"]
                    ard_data["lng"] = gps_data["lng"]
                    ard_data["alt"] = gps_data["alt"]
                    # 改行
                    f.write(ard_data,"\n")

    except Exception as e:
        print("\n")
        print("my_log.py log_txt try error : ",e)
        print("\n")

if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))