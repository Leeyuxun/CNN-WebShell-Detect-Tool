# Generated by Django 3.2 on 2021-05-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='authorityMonitorLog',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('authorityFilename', models.CharField(max_length=128)),
                ('event', models.CharField(max_length=128)),
                ('detectTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'authorityMonitorLog',
            },
        ),
        migrations.CreateModel(
            name='loginRecord',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('userID', models.IntegerField()),
                ('loginTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'loginRecord',
            },
        ),
        migrations.CreateModel(
            name='sensitiveFileMonitorLog',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('sensitiveFilename', models.CharField(max_length=128)),
                ('event', models.CharField(max_length=128)),
                ('detectTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sensitiveFileMonitorLog',
            },
        ),
        migrations.CreateModel(
            name='session',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('sessionID', models.CharField(max_length=32)),
                ('sessionValue', models.CharField(max_length=128)),
                ('createTime', models.FloatField()),
            ],
            options={
                'db_table': 'session',
            },
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('passwd', models.CharField(max_length=32)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'userInfo',
            },
        ),
        migrations.CreateModel(
            name='webshellDetectResult',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=128)),
                ('detectResult', models.CharField(max_length=128)),
                ('detectTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'webshellDetectResult',
            },
        ),
        migrations.CreateModel(
            name='webshellMonitorLog',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('filePath', models.CharField(max_length=256)),
                ('detectResult', models.CharField(max_length=128)),
                ('detectTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'webshellMonitorLog',
            },
        ),
    ]
