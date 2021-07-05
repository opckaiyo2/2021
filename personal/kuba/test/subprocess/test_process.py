from multiprocessing import Process, Manager
import time

def f(d):
    d_data = 0
    while(True):
        d['1'] = d_data
        d_data += 1

def auto(d):
    while(True):
        print(d)
        time.sleep(1)

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()

        p = Process(target=f, args=(d,))
        p.start()

        auto(d)