from django.db import models
from django.contrib.auth.models import User
from datetime import date  
    
# Create your models here.
class Venue(models.Model):
    name=models.CharField('Venue name',max_length=200)
    address=models.CharField(max_length=300)
    zip_code=models.CharField('Zip code',max_length=15)
    phone=models.CharField('Contact phone',max_length=25,blank=True)
    web=models.URLField('website address')
    email_address=models.EmailField('Email address',max_length=50,blank=True)
    owner=models.IntegerField('Venue owner',blank=False,default=1)
    venue_img=models.ImageField(null=True,blank=True,upload_to="images/")
    def __str__(self):
        return self.name
    
class MyClubUser(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField('Email field',max_length=100) 
    
    def __str__(self):
        return self.first_name + " " +self.last_name   
    
    
class Event(models.Model):
    name=models.CharField('Event name',max_length=120)
    event_date=models.DateTimeField('Event date')
    # venue=models.CharField(max_length=60)
    venue=models.ForeignKey(Venue,blank=True,null=True,on_delete=models.CASCADE)
    manager=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    description=models.TextField(blank=True )
    attendees=models.ManyToManyField(MyClubUser,blank=True)
    approved=models.BooleanField('Approved',default=False)
    def __str__(self):
        return self.name
   
    @property
    def Days_till(self):
        today=date.today()
        days_till=self.event_date.date()-today
        days_till_strip=str(days_till).split(",",1)[0]
        return days_till_strip
    @property
    def is_past(self):
        today=date.today()
        if self.event_date.date() > today:
            thing="past"
        else:
            thing="future"
        return thing        