# Generated by Django 4.1.7 on 2023-06-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_alter_time_table_exam_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_allotment',
            name='e_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='time_table',
            name='exam_date',
            field=models.DateField(),
        ),
    ]
