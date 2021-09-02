import ast

if __name__ == "__main__":
    string_data = "{'time':3755,'x':186.688,'y':-0.500,'z':170.938,'watertmp':0.0,'depth':-10.0,'thr0':25.000,'thr1':NAN,'thr2':25.000,'thr3':25.000,'thr4':25.000,'thr5':25.000,'cur0':0.1,'cur1':0.1,'cur2':0.1,'cel0':0.1,'cel1':1.3,'cel2':2.0,'cel3':2.6,'cel4':2.8,'cel5':2.9,'rot0':0,'rot1':0,'rot2':0,'rot3':0,'sys':1,'Gyro':3,'Accel':1,'Mag':0,'endtime':3765}"

    print(type(string_data))

    dict_data = ast.literal_eval(string_data)

    print(dict_data)