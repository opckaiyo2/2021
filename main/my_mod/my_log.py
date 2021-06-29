import datetime

def log_txt(ard_data, gps_data):
    filiname = "/home/pi/2021/main/log" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt") 
    old_ard_data = ""
    
    try:
        with open(filiname, 'a') as f:
            while(True):
                if(old_ard_data != ard_data):
                    ard_data["lat"] = gps_data["lat"]
                    ard_data["lng"] = gps_data["lng"]
                    ard_data["alt"] = gps_data["alt"]
                    f.write(ard_data,"\n")

    except Exception as e:
        print("\n")
        print("my_log.py log_txt try error : ",e)
        print("\n")

if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))