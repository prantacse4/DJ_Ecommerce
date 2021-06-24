from django.db import models

# Create your models here.


class Settings(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField( max_length=200)
    keywords = models.CharField( max_length=200)
    description = models.TextField()
    address = models.CharField( max_length=200)
    phone = models.IntegerField()
    fax = models.CharField(blank=True, max_length=200)
    email=models.EmailField(blank=True, null=True, max_length=254)
    smtpserver = models.CharField( max_length=200)
    smtpemail=models.EmailField(blank=True, null=True, max_length=254)
    smptpassword = models.CharField(blank=True, max_length=200)
    smptport = models.CharField(blank=True, max_length=200)
    icon = models.ImageField(upload_to='icon/', blank=True)
    facebook = models.CharField(blank=True, max_length=200)
    instagram = models.CharField(blank=True, max_length=200)
    address = models.TextField()
    contact = models.TextField()
    reference = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def imageurl(self):
        if self.icon:
            return self.icon.url
        else:
            return ""


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default='New')
    ip = models.CharField(max_length=200, blank=True)
    Note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name