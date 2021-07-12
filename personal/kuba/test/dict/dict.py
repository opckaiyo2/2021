if __name__ == "__main__":
    dict1 = {"rot0":0,"rot1":1,"rot2":2,"rot3":3}
    dict2 = {"rot0":4,"rot1":5,"rot2":6,"rot3":7}

    dict = {"dict1":dict1,"dict2":dict2}
    print(type(dict))
    print(dict["dict1"]["rot0"])