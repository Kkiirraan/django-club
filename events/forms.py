from django import forms
from  django.forms import ModelForm
from .models import Venue,Event


#creating form 
class VenueForm(ModelForm):
    class Meta:
        model=Venue
        fields=('name','address','zip_code','phone','email_address','venue_img') #fields="__all__"
        labels={
            'name':'',
            'address':'',
            'zip_code':'',
            'phone':'',
            'email_address':'',
            'venue_imag':'',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Venue name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip_code'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
                
        }
#creating form Admin
class EventFormAdmin(ModelForm):
    class Meta:
        model=Event
        fields=('name','event_date','venue','manager','description','attendees') #fields="__all__"
        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Venue',
            'manager':'Manager',
            'description':'',
            'attendees':'Attendees',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'event date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'venue'}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder':'manager'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'description'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-select','placeholder':'Attendees'}),
            
                
        }        
        
#user event form
class EventForm(ModelForm):
    class Meta:
        model=Event
        fields=('name','event_date','venue','description','attendees') #fields="__all__"
        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Venue',
            'description':'',
            'attendees':'Attendees',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'event date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'venue'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'description'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-select','placeholder':'Attendees'}),
            
                
        }           