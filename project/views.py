from django.shortcuts import render, HttpResponse, redirect
from project.models import rooms, staff, room_allotment, subject, time_table
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import math
from PIL import Image
import tempfile
from random import *
from django.contrib.auth import authenticate, get_user_model
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import subprocess
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import PyPDF2
from datetime import datetime
import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from pdf2image import convert_from_path
from django.contrib.sessions.models import Session
from django.contrib import messages


# from os.path import *
# Create your views here.
obj1 = ""
obj2 = ""


def loginUser(request):
    if request.method == "POST":
        # check if user is entered crt pass and username
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request,"invalid username or password")
            return render(request, 'login.html')
        # A backend authenticated the credentials
        # is_superuser = request.user.is_superuser
        if user.is_superuser:
            login(request, user)
            return redirect('/home')
        else:
            login(request, user)
            return redirect('/userhome')
    return render(request, 'login.html')


def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    staff_c = staff.objects.count()
    room_c = rooms.objects.count()
    cont = {
        'staff': staff_c,
        'room': room_c,
    }
    return render(request, 'adminhome.html', cont)


def room_management(request):
    room_numbers = rooms.objects.count()
    obj1 = room_allotment.objects.values_list('roomno')
    c = 0
    if len(obj1) > 0:
        c += 1
        for i in range(len(obj1)-1):
            if obj1[i] != obj1[i + 1]:
                c += 1
    available_value = room_numbers-c
    c = room_numbers-available_value
    cont = {
        'room': room_numbers,
        'allot': c,
        'avail': available_value,
    }
    return render(request, 'room_management.html', cont)


def staff_management(request):
    total_staff = staff.objects.count()
    obj1 = room_allotment.objects.values_list('staff_id')
    c = 0
    if len(obj1) > 0:
        c += 1
        for i in range(len(obj1)-1):
            if obj1[i] != obj1[i + 1]:
                c += 1
    available_value = total_staff-c
    print(c)
    cont = {
        'staff': total_staff,
        'allot': c,
        'avail': available_value,
    }
    return render(request, 'staff_management.html', cont)


def subject_management(request):
    return render(request, 'subject_management.html')


def exam_management(request):
    return render(request, 'exam_management.html')


def roomallot_management(request):
    return render(request, 'roomallot_manage.html')


def roomadd(request):
    if request.method == "POST":
        roomno = request.POST.get('roomno')
        roomloc = request.POST.get('roomname')
        roomdept = request.POST.get('dept')
        roomobj1 = rooms.objects.filter(roomno=roomno)
        if roomobj1.count() == 0:
            messages.success(request, "added successfully.")
            roomVar = rooms(roomno=roomno, roomloc=roomloc, dept=roomdept)
            roomVar.save()
        else:
            messages.error(request, "Room Number is already exists")
            return render(request, 'roomAdd.html')
    return render(request, 'roomAdd.html')


def roomedit(request):
    #  if request.method=="POST":
    roomno=request.POST.get('room_no')
    try:
            roomobj=rooms.objects.get(roomno=roomno)
    except Exception:
                # if roomobj is None:
                    messages.error(request, "Does not exists")
                    return render(request, 'roomedit.html')
    cont = {
                'st': roomobj
            }
    
    return render(request, 'roomedit.html', cont)


def roomupdate(request,roomno):
    if request.method == "POST":
        # roomno=request.POST.get('roomno')
        roomno=request.POST.get('roomno')
        roomloc=request.POST.get('roomname')
        roomdept=request.POST.get('dept')

        obj1 = rooms.objects.get(roomno=roomno)
        obj1.roomno = roomno
        obj1.roomloc = roomloc
        obj1.dept = roomdept
        messages.success(request, "Successfully updated")
    return redirect('roomdisplay')


def roomdelete(request,roomno):
    obj1 = rooms.objects.get(roomno=roomno)
    obj1.delete()
    messages.success(request,"Deleted successfully")
    return redirect('roomdisplay')


def roomdisplay(request):
    rd = rooms.objects.all()
    rdis = {
        "roomdis": rd
    }

    return render(request, 'roomdisplay.html', rdis)


# def pricing(request):
#     if request.method=="POST":
#         name=request.POST.get('name')
#         passw=request.POST.get('password')
#         formVar=table1(name=name,password=passw)
#         formVar.save()
#     return render(request,'pricing.html')


def home(request):
    if request.user.is_anonymous:
        return redirect('/login')
    staff_c = staff.objects.count()
    room_c = rooms.objects.count()
    cont = {
        'staff': staff_c,
        'room': room_c,
    }
    return render(request, 'adminhome.html', cont)


def teacheradd(request):

    if request.method == "POST":
        sid=request.POST.get('staff_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        add = request.POST.get('phone')
        dept = request.POST.get('department')
        username = request.POST.get('username')
        passwrd = request.POST.get('password')
        cpas=request.POST.get('cpassword')

        if passwrd != cpas:
            print("hello")
            messages.error(request,"password not mathced")
            return render(request, 'teacherAdd.html')
        else:
            try:

                teacherobj1 = staff.objects.filter(username=username)
                if teacherobj1.count() == 0:
                    user = User.objects.create_user(
                    username=username, email=email, password=passwrd)
                    teacherVar = staff(staff_id=sid,name=name, email=email, phone=add,department=dept, username=username, passwrd=passwrd)
                    teacherVar.save()
                    messages.success(request,"successfully added")
                else:
                    messages.error(request,"username already exists")
            except Exception:
                messages.error(request,"Username already have")
    return render(request, 'teacherAdd.html')


def teacherupdate(request, staff_id):
    if request.method == "POST":
        obj1 = staff.objects.get(staff_id=staff_id)
        obj1.name = request.POST.get('name')
        obj1.email = request.POST.get('email')
        obj1.phone = request.POST.get('phone')
        obj1.department = request.POST.get('department')
        tuname = request.POST.get('username')
        obj1.username = tuname
        passwrd = request.POST.get('password')
        obj1.passwrd = passwrd
        obj1.save()
        User = get_user_model()
        user1 = User.objects.get(username=tuname)
        user1.set_password(passwrd)
        user1.save()
        messages.success(request, "Successfully updated")
    return redirect('teacherdisplay')


def teacherdelete(request, staff_id):
    obj1 = staff.objects.get(staff_id=staff_id)
    user = User.objects.get(username=obj1.username)
    user.delete()
    obj1.delete()
    messages.success(request,"Deleted successfully")
    return redirect('teacherdisplay')


def teacheredit(request):
    #  if request.method=="POST":
    try:
        teacherobj = staff.objects.get(staff_id=request.POST.get('staff_id'))   
    except Exception:
        print("eroer")
        messages.error(request, "Does not exists")
        return render(request, 'teacheredit.html')
    cont = {
        'sts': teacherobj
    }
    return render(request, 'teacheredit.html', cont)


def teacherdisplay(request):
    td = staff.objects.all()
    tdis = {
        "teacherdir": td
    }
    # print("teacher display")

    return render(request, 'teacherdisplay.html', tdis)

# subject management


def subjectadd(request):
    if request.method == "POST":
        subid = request.POST.get('subid')
        subcode = request.POST.get('subcode')
        subname = request.POST.get('subname')
        stream = request.POST.get('stream')
        subobj = subject.objects.filter(subcode=subcode)
        subobj1=subject.objects.filter(subid=subid)
        if subobj.count() == 0 or subobj1.count() == 0:
            subVar = subject(subid=subid, subcode=subcode,subname=subname, stream=stream)
            subVar.save()
            messages.success(request, "added successfully.")
        else:
            messages.error(request, "subject code or id is already exists")
            return render(request, 'subjectadd.html')
    return render(request, 'subjectadd.html')


def subjectedit(request):
    try:
            subobj = subject.objects.get(subid=request.POST.get('subid'))
    except Exception:
            messages.error(request, "Does not exists")
            return render(request, 'subjectedit.html')
    data = {
        'st': subobj
    }
    return render(request, 'subjectedit.html', data)


def subjectupdate(request, subid):
    if request.method == "POST":
        # roomno=request.POST.get('roomno')
        obj1 = subject.objects.get(subid=subid)
        obj1.subid = request.POST.get('subid')
        obj1.subcode = request.POST.get('subcode')
        obj1.subname = request.POST.get('subname')
        obj1.stream = request.POST.get('stream')
        obj1.save()
        messages.success(request, "Successfully updated")
    return redirect('subjectdisplay')


def subjectdelete(request, subid):
    obj1 = subject.objects.get(subid=subid)
    obj1.delete()
    messages.success(request,"Deleted successfully")
    return redirect('subjectdisplay')


def subjectdisplay(request):
    rd = subject.objects.all()
    rdis = {
        "subdis": rd
    }
    return render(request, 'subjectdisplay.html', rdis)


def timetableinsertion(request):
    if request.method == "POST":
        # return
    # time_table.objects.all().delete()
        try:
            # print("yesesss3ws")
            rows = request.POST.get('hide')
            rows = int(rows)
            # print(rows)
            for i in range(rows):
                tid = request.POST.get(f"cell({str(i)}1)")
                sid = request.POST.get(f"cell({str(i)}2)")
                exam_date = request.POST.get(f"cell({str(i)}3)")
                exam_time = request.POST.get(f"cell({str(i)}4)")
                exam_type = request.POST.get(f"cell({str(i)}5)")
                stu_cap = request.POST.get(f"cell({str(i)}6)")
                # print("no value found",stu_cap)
                my_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
                examvar = time_table(tid=tid, sid=sid,date_time=exam_time, exam_type=exam_type, exam_date=my_date,sub_student=stu_cap)
                examvar.save()
            messages.success(request,"Added successfully")
        # #     # return render(request, 'exam_management.html')
        except Exception:
            print("errror occured")
            messages.error(request,"Please fill the form correctly")
            return render(request, 'exam_management.html')
    return render(request, 'exam_management.html')


    


def autoinsert(request):
    return render(request, 'autoinsertion.html')


def pdf_to_text(request):
    # Handle file upload
    uploaded_file = request.FILES.get('pdftext')
    
    # pdf_file = request.FILES['pdf_file']
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''.join(
        pdf_reader.pages[page].extract_text()
        for page in range(len(pdf_reader.pages))
    )
    return render(request, 'autoinsertion.html', {'text': text})


def manualinsert(request):
    subid_list = list(subject.objects.values_list('subid'))
    sub_obj=str(subid_list)
    sub_obj=sub_obj.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
    subid_list=list(sub_obj.split(" "))
    # print(subid_list)
    # print(list(subid_list))
    return render(request, 'manualinsertion.html',{'sub_list':subid_list})


def autoseat(request):  # sourcery skip:

    final_list1 = []
    final_list2 = []
    final_list3 = []
    final_list4 = []
    exam_data_list = time_table.objects.values_list('exam_date')
    exam_data_list = sorted(list(exam_data_list))
    # print("lsit",exam_data_list)
    new_list = []
    e_date = []
    try:
        if len(exam_data_list) != 0:
            count = 1
            new_list.append(exam_data_list[0])
            for i in range(len(exam_data_list)-1):
                if exam_data_list[i] != exam_data_list[i+1]:
                    new_list.append(exam_data_list[i+1])
                    count += 1
        else:
            count = 0
        date_format = "%Y,%m,%d"
        # print(new_list)
        for new in new_list:
            new = str(new)
            # print(new)
            new = new.replace('(datetime.date(','').replace(')','').replace('),)', '').replace(' ', '').replace('(','')
            new = new.rstrip(new[-1])
            # print("list",new)
            d = datetime.strptime(new, date_format).date()
            # new=d
            print(new)
            alloted_list = time_table.objects.filter(exam_date=d)
            room_list = list(rooms.objects.values_list('roomno'))
            staff_list = list(staff.objects.values_list('staff_id'))
            shuffle(staff_list)
            shuffle(room_list)
            subid_list = []
            sub_stu_cap = []
            for allot in alloted_list:
                subid_list.append(allot.tid)
                sub_stu_cap.append(allot.sub_student)
                print(allot.sub_student)
            objstr1 = str(room_list)
            objstr2 = str(staff_list)
            objstr3 = str(subid_list)
            objstr4 = str(sub_stu_cap)
        # print(objstr2)

            objstr2 = objstr2.replace('[', '').replace(']', '').replace(
            ')', '').replace('(', '').replace("'", "")
        # print(objstr2)
            objstr1 = objstr1.replace('[', '').replace(']', '').replace(
            '(', '').replace(')', '').replace(',', '').replace("'", '')
            objstr3 = objstr3.replace('[', '').replace(']', '').replace(
            ')', '').replace('(', '').replace("'", "").replace(',,', '')
            objstr4 = objstr4.replace('[', '').replace(']', '').replace(
            ')', '').replace('(', '').replace("'", "")

            room_list = list(objstr1.split(" "))
            subid_list = list(objstr3.split(" "))
        # objstr3 = str(subid_list)
        # print("staff",objstr3)
            _extracted_from_autoseat_29(subid_list)
            staff_list = list(objstr2.split(",,"))
        # print(staff_list)
            _extracted_from_autoseat_29(staff_list)
        # print("ksdf",staff_list)
            sub_stu_cap = _extracted_from_autoseat_39(objstr4)
            room_cap_list = [None] * len(room_list)
        # print(room_list)
            for i in range(len(room_list)):
                room_cap_list[i] = 50

        # print("cap list",room_cap_list)
            total_room_capacity = sum(room_cap_list)
            total_student = sum(sub_stu_cap)
        # print(total_student)
            total_rooms = math.ceil(total_student/50)

            i = j = 0    #

            if total_room_capacity >= total_student:
                new_staff = []
                object3_list = []  # subject id
                object2_list = []  # room list
                object1_list = []  # subject student

                while ((i < total_rooms) and (j < (len(sub_stu_cap)))):
                    e_date.append(new)
                    while room_cap_list[i] != 0 and sub_stu_cap[j] != 0:
                        if room_cap_list[i] == sub_stu_cap[j]:
                        # print("equal")
                            object1_list.append(sub_stu_cap[j])
                            object3_list.append(subid_list[j])
                            object2_list.append(room_list[i])
                            new_staff.append(staff_list[i])
                            total_student -= sub_stu_cap[j]
                            room_cap_list[i] = 0
                            sub_stu_cap[j] = 0
                        elif room_cap_list[i] > sub_stu_cap[j]:
                            object1_list.append(sub_stu_cap[j])
                            object3_list.append(subid_list[j])
                            object2_list.append(room_list[i])
                            new_staff.append(staff_list[i])
                            total_student -= sub_stu_cap[j]
                            room_cap_list[i] -= sub_stu_cap[j]
                            sub_stu_cap[j] = 0
                        else:
                            object1_list.append(50)
                            object3_list.append(subid_list[j])
                            object2_list.append(room_list[i])
                            new_staff.append(staff_list[i])
                            total_student -= sub_stu_cap[j]
                            sub_stu_cap[j] = sub_stu_cap[j]-room_cap_list[i]
                            room_cap_list[i] = 0
                # if total_student == 0:
                #     object2_list.append(room_list[i])
                #     new_staff.append(staff_list[i])
                    if sub_stu_cap[j] == 0:
                        j += 1
                    if room_cap_list[i] == 0:
                        i += 1
                    # n += 1

            else:
                messages.error(request,"total room capacity should greate than student capacity")
                return render(request,"roomallot_manage.html")

            final_list1.extend(object1_list)
            final_list2.extend(object2_list)
            final_list4.extend(new_staff)
            final_list3.extend(object3_list)



        for x in range(len(final_list3)-1):
            obbstr = str(final_list3[x])
            obbstr = obbstr.replace(",", '')
            final_list3[x] = int(obbstr)
        final_list3[-1] = int(final_list3[-1])
    # print(final_list3)
        print(e_date)
        cont = {
        'object1_list': final_list1,
        'object2_list': final_list2,
        'object3_list': final_list3,
        'object4_list': final_list4,
        'object5_list': e_date,
        }
    except Exception:
        messages.error(request,"Please check the staff and room info")
        return render(request,"roomallot_manage.html")
    return render(request, 'seat_allot.html', cont)


# TODO Rename this here and in `autoseat`
def _extracted_from_autoseat_102(object2_list, staff_list):
    length = len(object2_list)
    result = [None]*length
    i = j = 0
    while i < (len(object2_list)-1) and j < len(staff_list):
        if object2_list[i] == object2_list[i+1]:
            result[i] = staff_list[j]
            result[i+1] = staff_list[j]
        else:
            j += 1
        i += 1
    # print(result)
    return result


# TODO Rename this here and in `autoseat`
def _extracted_from_autoseat_39(arg0):
    result = list(arg0.split(","))
    _extracted_from_autoseat_29(result)
    result = list(map(int, result))

    return result


# TODO Rename this here and in `autoseat`
def _extracted_from_autoseat_29(arg0):
    subid_listsam = str(arg0[-1])
    subid_listsam = subid_listsam.replace(',', '')
    arg0[-1] = subid_listsam




def addallotment(request):
    if request.method == 'POST':
        room_allotment.objects.all().delete()
        student_allot = request.POST.getlist('xobj')
        room_no = request.POST.getlist('yobj')
        sid = request.POST.getlist('zobj')
        staff_list = request.POST.getlist('wobj')
        date_list = request.POST.getlist('aobj')
        date_format = "%Y,%m,%d"
        objstr1 = str(student_allot)
        objstr3 = str(sid)
        objstr2 = str(staff_list)
        objstr4 = str(room_no)
        objstr5 = str(date_list)
        objstr2 = objstr2.replace('[', '').replace(
            ']', '').replace("'", "").replace('"', '')
        objstr1 = objstr1.replace('[', '').replace(
            ']', '').replace("'", "").replace('"', '')
        objstr3 = objstr3.replace('[', '').replace(
            ']', '').replace("'", "").replace('"', '').replace(" ", '')
        objstr4 = objstr4.replace('[', '').replace(
            ']', '').replace("'", "").replace('"', '')
        objstr5 = objstr5.replace('[', '').replace(
            ']', '').replace("'", "").replace('"', '')
        obj1 = list(objstr1.split(","))
        obj2 = list(objstr2.split(","))
        obj4 = list(objstr4.split(","))
        obj3 = list(objstr3.split(","))
        obj5 = list(objstr5.split(" "))
        student_allot = list(obj1)
        staff_list = list(obj2)
        sid = list(map(int, obj3))
        room_no = list(map(int, obj4))

        zipped = zip(room_no, staff_list, sid, student_allot, obj5)
        for w, x, y, z, a in zipped:
            rno = f'{w}'
            tname = f'{x}'
            tid = '%d' % y
            z = int(z)
            sallot = '%d' % z
            a = list(a)
            a[-1] = ""
            a = ''.join(a)
            date_obj = datetime.strptime(a, date_format).date()
            objauto = room_allotment(
                roomno=rno, staff_id=tname, tid=tid, student_alloted=sallot, room_exam_date=date_obj)
            objauto.save()
        messages.success(request,"room alloted successfully")
    return render(request, 'seat_allot.html')


def manualseat(request):
    obj1 = list(rooms.objects.values_list('roomno'))
    num=rooms.objects.count()
    objstr1 = ""
    objstr1 = str(obj1)
    objstr1 = objstr1.replace('[', '').replace(']', '').replace(
        '(', '').replace(')', '').replace(',', '').replace("'", '')
    obj1 = list(objstr1.split(" "))

    if request.method == "POST":
       
        try:
            room_allotment.objects.all().delete()
            rows = request.POST.get('hide')
            rows = int(rows)
            i=0
            while i < rows:
                for x in obj1:
                    rno = request.POST.get(f"cell({str(i)}1)")
                    tname = request.POST.get(f"cell({str(i)}2)")
                    sid = request.POST.get(f"cell({str(i)}3)")
                    s_cap=request.POST.get(f"cell({str(i)}4)")
                    date1=request.POST.get(f"cell({str(i)}5)")
                    print(tname)
                    my_date = datetime.strptime(date1, '%Y-%m-%d').date()
                    objmanual = room_allotment(roomno=rno, staff_id=tname, tid=sid,student_alloted=s_cap,room_exam_date=date1)
                    objmanual.save()
                i+=1
            messages.success(request,"room alloted successfully")
            return render(request,'manual_seat.html')
        except Exception:
            messages.error(request,"Please fill the information correctly")
            return render(request,"manual_seat.html")
    return render(request, 'manual_seat.html', {'len1': obj1})


def viewall(request):
    roomobj = room_allotment.objects.all()
    rd = {
        'roomobj1': roomobj
    }
    return render(request, 'status.html', rd)


def logoutUser(request):
    logout(request)
    return redirect('/login')


# users
def userhome(request):
    try:
        resultobj = staff.objects.get(username=request.user)
        resultobj2 = room_allotment.objects.get(staff_id=resultobj.staff_id)
        if resultobj2 is not None:
            # resultobj2 = list(resultobj2)
            resultobj3 = time_table.objects.get(tid=resultobj2.tid)
            resultobj4 = subject.objects.get(subid=resultobj3.sid)
            data = {
            'roomno': resultobj2.roomno,
            'date': resultobj3.exam_date,
            'time': resultobj3.date_time,
            'dep': resultobj4.stream,
            'subname': resultobj4.subname,
        }
    except Exception:
            data = {
            'roomno': "-",
            'date':"-",
            'time': "-",
            'dep': "-",
            'subname': "-",
        }
    return render(request, 'userpagehome.html', data)


def profile(request):
    profileobj = staff.objects.get(username=request.user)
    # viewmyduty=room_allotment.objects.get(teachername=profileobj.name)
    cont = {
        'profileobj': profileobj,
        # 'viewmyduty':viewmyduty,
    }
    return render(request, 'profile.html', cont)


def profilesaved(request, staff_id):
    if request.method == "POST":
        userobj = staff.objects.get(staff_id=staff_id)
        userobj.name = request.POST.get('tname')
        userobj.email = request.POST.get('temail')
        userobj.phone = request.POST.get('tphone')
        userobj.department = request.POST.get('tdept')
        userobj.save()
        messages.success(request,"profile updated successfully")
    return redirect("profile")


def changepassword(request):  # sourcery skip: extract-method
    if request.method != "POST":
        return render(request, 'changepass.html')
    User = get_user_model()
    username = request.user.username
    user1 = User.objects.get(username=username)
    new_password = request.POST.get('newpass')
    cpass=request.POST.get('cpass')
    # hashed_password = make_password(new_password)
    if new_password == cpass:
        user1.set_password(new_password)
    # print(hashed_password)
        user1.save()
        obj1 = staff.objects.get(username=username)
        obj1.passwrd = new_password
        obj1.save()
        messages.success(request,"passwod updated successfully")
        logout(request)
        return render(request,'login.html')
    else:
        messages.error(request,'password not matched')
    # print(obj1)
    # print(obj1.passwrd)
    # print(username)
    # print(new_password)
    # print('reset successfully')
        return render(request,'changepass.html')