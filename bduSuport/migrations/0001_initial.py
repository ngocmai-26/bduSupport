# Generated by Django 4.2.2 on 2024-06-28 08:46

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicLevels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationMethods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Majors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('industryCode', models.CharField(max_length=255)),
                ('targets', models.CharField(max_length=255)),
                ('combination', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('benchmark', models.CharField(max_length=255)),
                ('tuition', models.CharField(max_length=255)),
                ('trainingLocation', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.TextField()),
                ('type', models.IntegerField()),
                ('image', models.ImageField(default=None, upload_to='news/%Y/%m')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('score', models.FloatField()),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=255)),
                ('gender', models.IntegerField(default=0)),
                ('dateOfBirth', models.DateField()),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('highSchool', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('examGroup', models.CharField(max_length=255)),
                ('academicLevelId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bduSuport.academiclevels')),
                ('major', models.ManyToManyField(related_name='student', to='bduSuport.majors')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('trainingLocation', models.CharField(max_length=255)),
                ('tuition', models.CharField(max_length=255)),
                ('benchmark', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('image', models.ImageField(default=None, upload_to='notification/%Y/%m')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bduSuport.account')),
            ],
        ),
        migrations.CreateModel(
            name='AdmissionRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluationMethod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bduSuport.evaluationmethods')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bduSuport.students')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
    ]
