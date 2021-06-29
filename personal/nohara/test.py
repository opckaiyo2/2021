import time
t1 = time.time()
total = 0
for k in range(1000000):
    total = total + k
print ("Total =", total)
t2 = time.time()
t = t2-t1
print("%.100f" % t)