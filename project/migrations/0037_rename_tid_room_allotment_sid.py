# Generated by Django 4.1.7 on 2023-06-16 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_alter_staff_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room_allotment',
            old_name='tid',
            new_name='sid',
        ),
    ]
