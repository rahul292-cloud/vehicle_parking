# Generated by Django 3.0.2 on 2020-04-18 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allModels', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uservehicle',
            old_name='categoty',
            new_name='categoty_name',
        ),
    ]