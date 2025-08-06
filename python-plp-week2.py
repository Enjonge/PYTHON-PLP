my_list=[10,20,30,40]
print(my_list)
my_list.insert(1, 15)
print(my_list)
my_list.extend([50,60,70])
print(my_list)
my_list.remove(70)
print(my_list)
my_list.sort()
print(my_list)
if 30 in my_list:
    print(f"Index of 30: {my_list.index(30)}")
else:
    print("30 is not in the list.")