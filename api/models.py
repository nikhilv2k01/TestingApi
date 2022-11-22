from django.db import models

# Create your models here.


class Register(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "register"
