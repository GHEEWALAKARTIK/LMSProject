from django.db import models

# Create your models here.

class User(models.Model):
    UID = models.IntegerField(auto_created=True,primary_key=True)
    Name = models.CharField(max_length=50)
    Role = models.CharField(max_length=8)
    Password = models.CharField(max_length=20, null=True)
    Total_Leave = models.IntegerField(default=0)
    Created_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'User'


class Leave(models.Model):
    LID = models.IntegerField(auto_created=True,primary_key=True)
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    Start_Date = models.DateField()
    End_Date = models.DateField()
    Description = models.TextField()
    Leave_Status = models.BooleanField(default=False)
    Seen_By_Manager = models.BooleanField(default=False)
    Created_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Leave'