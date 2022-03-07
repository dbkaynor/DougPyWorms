import pprint
import random
from inputs import devices
for device in devices:
    print(device)

pp = pprint.PrettyPrinter(indent=4)

shifted = -1

list1 = [["apple", "banana", "grape", "cherry", "melon", 'tree', 'weed', 'flower', "hay"],
         ["gold", "iron", "hydrogen", "tin", "helium", "arsenic", "lead", "argon", "oxygen"]]
list1[0].sort()
list1[1].sort()
print('a0: ', list1[0])
print('a1: ', list1[1])

i = 0
while i < len(list1):
    # -1 means random  print("i: ", i)shift amount, 0  no shifting, 1 or more is a shift value
    # print(list1[i])
    if shifted == -1:
        count = random.randint(0, len(list1[i]) - 1)
        count = 6
        x = 0
        while x < count:
            list1[i].append(list1[i].pop(0))   # left shift
            # list1[i].insert(0, list1[i].pop())  # right shift
            x += 1
    elif shifted == 0:
        pass
    else:
        count = 0
        while count < shifted:
            count += 1
            print("Count: ", count)
            list1[i].append(list1[i].pop(count))
    i += 1

print('b0: ', list1[0])
print('b1: ', list1[1])
