object2_list = [101,101,101,102,102,103,103,103]
staff_list = ["athul", "nihal","niru"]


length = len(object2_list)
new_staff = [None]*length

# for i in range(len(staff_list)):
#     new_staff[i] = staff_list
i = j = 0
while i < (len(object2_list)-1) and j < len(staff_list):
    if object2_list[i] == object2_list[i+1]:
        new_staff[i]=staff_list[j]
        new_staff[i+1] = staff_list[j]
    else:
        j+=1
    i+=1
print(object2_list)
print(new_staff)
