import configparser

if __name__ == "__main__":
    INI_FILE = "C:\\Users\\user\\Documents\\vscode\\python\\2021_tast\\personal\\kuba\\test\\config\\config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    operation = inifile.getint("main", "operation")

    print(operation)