# Generated by Django 3.0.2 on 2020-04-28 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allModels', '0004_parkingexit'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingexit',
            name='slot',
            field=models.CharField(default='', max_length=100),
        ),
    ]
