from django.db import models


class User(models.Model):
    emailid = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    group_id = models.IntegerField()

    def __str__(self):
        return self.username


class Queries(models.Model):
    q_id = models.AutoField(primary_key=True)
    mailid = models.CharField(db_column='MailID', max_length=40) 
    query = models.TextField(db_column='Query')  
    query_type = models.CharField(db_column='Query_type', max_length=50)  

class Profile(models.Model):
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    mailid = models.EmailField(db_column='MailID', primary_key=True)  # Field name made lowercase.
    regno = models.CharField(db_column='RegNo', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rollno = models.IntegerField(db_column='RollNo')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=40)  # Field name made lowercase.
    phno = models.BigIntegerField(db_column='Phno')  # Field name made lowercase.