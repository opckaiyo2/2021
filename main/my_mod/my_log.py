#coding: utf-8
import datetime
import ast
import os

def log_txt(ard_data):
    # logフォルダpath
    folder = "/home/pi/2021/main/log/"

    # logのフォルダ内のフォルダ名取得
    folders = os.listdir(folder)

    # 今日の日付フォルダがあるか確認なければ作成
    today = folder + str(datetime.datetime.now().strftime("%Y-%m-%d"))
    if not (str(datetime.datetime.now().strftime("%Y-%m-%d")) in folders):
        os.mkdir(today)

    # log作成時刻がファイル名のファイル作成
    filiname = today + "/" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt") 
    # 同じデータを書き込まないように前ループのデータ保管用変数
    old_ard_data = ""
    
    try:
        # オブジェクトの作成
        # with文は終了時に必要な処理を補完してくれる文 今回はfileを保存して終了をしてくれる
        with open(filiname, 'a') as f:
            while(True):
                # 同じデータを書き込もうとしてないかチェック
                if(old_ard_data != str(ard_data)):
                    # 改行
                    f.write(str(ard_data))
                    f.write("\n")
                old_ard_data = str(ard_data)

    except SyntaxError:
        pass

    except Exception as e:
        print("\n")
        print("my_log.py log_txt try error : ",e)
        print("\n")

if __name__ == "__main__":
    ard_data = {"time":88}
    log_txt(ard_data)