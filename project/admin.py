from django.contrib import admin
from project.models import subject,rooms,staff,room_allotment
# Register your models here.
admin.site.register(subject)
admin.site.register(rooms)
admin.site.register(staff)
admin.site.register(room_allotment)
