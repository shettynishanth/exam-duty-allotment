# Generated by Django 4.1.7 on 2023-05-29 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_remove_room_allotment_edate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room_allotment',
            name='examdate',
        ),
        migrations.RemoveField(
            model_name='room_allotment',
            name='examtime',
        ),
    ]
