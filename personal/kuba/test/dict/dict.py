import ast

def dic(data):
    data["time"] = 0

if __name__ == "__main__":
    dict_data = {"time":1000,"test1":2000,"test2":3000}

    dic(dict_data)
    print(dict_data)