# Generated by Django 4.1.7 on 2023-06-11 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_room_allotment_student_allot_rooms_room_cap_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room_allotment',
            old_name='student_allot',
            new_name='student_alloted',
        ),
    ]