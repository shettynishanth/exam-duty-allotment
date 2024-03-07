# Generated by Django 4.1.7 on 2023-05-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_alter_room_allotment_edate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room_allotment',
            name='edate',
        ),
        migrations.RemoveField(
            model_name='room_allotment',
            name='etime',
        ),
        migrations.AddField(
            model_name='room_allotment',
            name='tid',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='time_table',
            name='sid',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='time_table',
            name='tid',
            field=models.CharField(max_length=15),
        ),
    ]
