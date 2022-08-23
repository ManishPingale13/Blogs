from django.db import models

# Create your models here.
class Contact(models.Model):
    serialNum= models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=50)
    phoneNum = models.CharField(max_length=13)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message from '+ self.name