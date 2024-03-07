from django.db import models

# Create your models here.
class rooms(models.Model):
    # id=models.AutoField()
    roomno=models.IntegerField(primary_key=True)
    roomloc=models.CharField(max_length=12)
    dept=models.CharField(max_length=20)
    def __str__(self):
        return self.roomno
    
class staff(models.Model):
    # id=models.AutoField()
    staff_id=models.CharField(primary_key=True,max_length=20)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=12)
    phone=models.CharField(max_length=10)
    department=models.CharField(max_length=12)
    username=models.CharField(max_length=12)
    passwrd= models.CharField(max_length=12)
    def __str__(self):
        return self.name
    
class subject(models.Model):
    # id=models.AutoField()
    subid=models.IntegerField(primary_key=True)
    subcode=models.CharField(max_length=10)
    subname=models.CharField(max_length=20,null=True)
    stream=models.CharField(max_length=20)
    # sub_student=models.CharField(max_length=10)
    def __str__(self):
        return self.subname

    
class time_table(models.Model):
    tid=models.CharField(max_length=10,primary_key=True)
    sid=models.CharField(max_length=11)
    date_time = models.CharField(max_length=20)
    exam_type=models.CharField(max_length=20)
    exam_date = models.DateField()
    sub_student=models.IntegerField()
    # def formatted_date(self):
    #     return self.exam_date.strftime("%b %d, %Y")
    

class room_allotment(models.Model):
    roomno=models.IntegerField()
    staff_id=models.CharField(max_length=20)
    tid=models.CharField(max_length=12,default=None)
    student_alloted=models.IntegerField()
    room_exam_date=models.DateField()
    def __str__(self):
        return self.teachername
    # def formatted_date(self):
    #     return self.edate.strftime("%b %d, %Y")
    
    