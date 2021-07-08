import configparser

if __name__ == "__main__":
    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE)

    operation = inifile.getint("main", "operation")

    print(operation)