# Generated by Django 4.1.7 on 2023-06-12 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0032_alter_room_allotment_e_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room_allotment',
            name='e_date',
        ),
        migrations.RemoveField(
            model_name='time_table',
            name='exam_date',
        ),
    ]
