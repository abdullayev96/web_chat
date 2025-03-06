# import itertools
#
#
# d= list(itertools.chain('abc', 'def'))
# print(d)

# d= list(filter(lambda x: x % 2 == 0, range(5)))
# print(d)


import threading
import time

def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        time.sleep(1)



def print_letters():
    for letter in 'abcde':
        print(f"Letter: {letter}")
        time.sleep(1)

# Creating threads
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

# Starting threads
t1.start()
t2.start()

# Joining threads to wait for them to finish
t1.join()
t2.join()

print("Done!")
