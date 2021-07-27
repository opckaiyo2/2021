import select
import sys
import tty

def isInputData():
    return select.select([sys.stdin],[],[],0) == ([sys.stdin],[],[])

if __name__ == "__main__":

    tty.setcbreak(sys.stdin.fileno())

    while True:
        if isInputData():
            input_key = sys.stdin.read(3)
            print(input_key)

            print("input key : ",input_key)

            if input_key == "[A":
                print("koko")