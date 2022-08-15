# Generated by Django 4.0 on 2021-12-12 17:05

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
                ('location_sub_type', models.CharField(choices=[('ENTR', 'Entrance'), ('EXIT', 'Exit')], max_length=4)),
                ('is_active', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField(default='127.0.0.1')),
                ('connected_dev', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TimeTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_time', models.DateTimeField(auto_now=True)),
                ('event_date', models.DateField(auto_now=True)),
                ('event_photo', models.ImageField(upload_to='')),
                ('event_type', models.CharField(choices=[('S_ENTR', 'Success Entrance'), ('S_EXIT', 'Success Exit'), ('F_ENTR', 'Failed Entrance'), ('F_EXIT', 'Failed Exit')], max_length=6)),
                ('event_photo_encodings', models.JSONField(default=dict)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='TAS.device')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='TAS.user')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('max_users', models.IntegerField(default=0)),
                ('staff', models.JSONField(null=True)),
                ('department_head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TAS.user')),
            ],
        ),
    ]