# Generated by Django 3.2.21 on 2023-09-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_queries_query_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.TextField(db_column='Name')),
                ('mailid', models.CharField(db_column='MailID', max_length=40, primary_key=True, serialize=False)),
                ('regno', models.CharField(blank=True, db_column='RegNo', max_length=7, null=True)),
                ('rollno', models.IntegerField(db_column='RollNo')),
                ('year', models.IntegerField(db_column='Year')),
                ('department', models.CharField(db_column='Department', max_length=40)),
                ('phno', models.BigIntegerField(db_column='Phno')),
            ],
        ),
    ]