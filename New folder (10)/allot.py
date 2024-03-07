import math


def room_allotment():
    print("function")
    rooms = [101, 102, 104]
    room_capacity = [45,50,50]
    student_cap = [34,30]
    subject = ['hindi', "eng"]
    total_room_capacity=sum(room_capacity)
    max_value = max(room_capacity)
    min_value = min(room_capacity)
    avg_capacity = math.ceil((max_value+min_value)/2)
    total_student = sum(student_cap)
    total_rooms = math.ceil(total_student/avg_capacity)
    allotment = {}
    i = j = m = n = 0
    if total_room_capacity >= total_student:
        while ((i < total_rooms) and (j < (len(student_cap)))):
            while room_capacity[i] != 0 and student_cap[j] != 0:
                if room_capacity[i] == student_cap[j]:
                    allotment[m] = str(student_cap[j])+" " + \
                        str(rooms[n])+" "+subject[j]
                    m += 1
                # n+=1
                    room_capacity[i] = 0
                    student_cap[j] = 0
                elif room_capacity[i] > student_cap[j]:
                    allotment[m] = str(student_cap[j])+" " + \
                        str(rooms[n])+" "+subject[j]
                    room_capacity[i] -= student_cap[j]
                    student_cap[j] = 0
                    m += 1
                # n+=1
                else:
                    allotment[m] = str(room_capacity[i])+" " + \
                        str(rooms[n])+" "+subject[j]
                    student_cap[j] = student_cap[j]-room_capacity[i]
                    room_capacity[i] = 0
                    m += 1
                # n+=1
            if student_cap[j] == 0:
                j += 1
            if room_capacity[i] == 0:
                i += 1
                n += 1
        print(allotment)


room_allotment()
