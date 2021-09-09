from multiprocessing import Process, Manager
import time
from def_f import f

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