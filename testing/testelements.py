list1 = [1, 2, 3, 4, 5]
list2 = [6, 7, 8, 9, 10]

list3 = list(zip(list1, list2))
print(list3)
print(list3.index((4, 9)))