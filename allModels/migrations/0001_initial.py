# Generated by Django 2.2 on 2020-04-26 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('category_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_category_related', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_category_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parking_slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('slot_name', models.CharField(blank=True, max_length=10, null=True)),
                ('slot_status', models.BooleanField(default=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_parking_slot_related', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_parking_slot_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('barcode_number', models.CharField(blank=True, max_length=60, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=60, null=True)),
                ('chessis_number', models.CharField(blank=True, max_length=60, null=True)),
                ('vehicle_model', models.CharField(blank=True, max_length=60, null=True)),
                ('variants', models.CharField(blank=True, max_length=60, null=True)),
                ('color', models.CharField(blank=True, max_length=60, null=True)),
                ('date', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_vehicledetail_related', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_vehicledetail_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('Barcode_no', models.CharField(blank=True, max_length=100, null=True)),
                ('owner_name', models.CharField(blank=True, max_length=100, null=True)),
                ('owner_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_model', models.CharField(max_length=100)),
                ('vehicle_no', models.CharField(max_length=100)),
                ('chessis_no', models.CharField(max_length=100)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('categoty_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allModels.Category')),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_uservehicle_related', to=settings.AUTH_USER_MODEL)),
                ('parking_slot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allModels.Parking_slot')),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_uservehicle_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParkingOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('exit_date', models.DateField()),
                ('exit_time', models.TimeField()),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_parkingout_related', to=settings.AUTH_USER_MODEL)),
                ('user_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allModels.UserVehicle')),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_parkingout_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParkingIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('entry_date', models.DateField()),
                ('entry_time', models.TimeField()),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_parkingin_related', to=settings.AUTH_USER_MODEL)),
                ('user_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allModels.UserVehicle')),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_parkingin_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_use_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('vehicle_no', models.CharField(max_length=100)),
                ('chessis_no', models.CharField(max_length=100)),
                ('vehicle_model', models.CharField(max_length=100)),
                ('variants', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('booking_date', models.DateTimeField()),
                ('booking_exit_date', models.DateTimeField()),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('barcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allModels.VehicleDetail')),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_allmodels_bookvehicle_related', to=settings.AUTH_USER_MODEL)),
                ('parking_slot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allModels.Parking_slot')),
                ('writer', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_allmodels_bookvehicle_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
