# Generated by Django 4.1.7 on 2023-06-22 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0040_rooms_id_staff_id_subject_id_alter_rooms_roomno_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room_allotment',
            old_name='sid',
            new_name='tid',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='id',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='id',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='id',
        ),
        migrations.AddField(
            model_name='staff',
            name='staff_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rooms',
            name='roomno',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]