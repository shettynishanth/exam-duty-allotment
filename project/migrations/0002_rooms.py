# Generated by Django 4.1.7 on 2023-04-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomno', models.CharField(max_length=100)),
                ('roomloc', models.CharField(max_length=30)),
                ('dept', models.CharField(max_length=40)),
            ],
        ),
    ]