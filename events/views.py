from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event,Venue
from .forms import VenueForm,EventForm,EventFormAdmin
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
import csv
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#pagination
from django.core.paginator import Paginator




#craeting a pdf file
def venue_pdf(request):
    #create bytestream buffer
    buf=io.BytesIO()
    #creating a canvas
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    #create a text object
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    
    venues=Venue.objects.all()
    lines=[]
    for venue in venues:
       lines.append(venue.name)
       lines.append(venue.address)    
       lines.append(venue.zip_code)    
       lines.append(venue.phone) 
       lines.append(venue.web)    
       lines.append(venue.email_address)      
       lines.append("")    
           
    
    for line in lines:
        textob.textLine(line)
        
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf,as_attachment=True,filename='venue.pdf')    

#creating a csv file
def venue_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachments; filename=venues.csv'
    # create csv writer
    writer=csv.writer(response) 
    venues=Venue.objects.all()
    #adding column heading 
    writer.writerow(['venue name','address','zip code','phone','web address','email'])
    
    
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,])
    return response

#creating a text file
def venue_text(request):
    response=HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachments; filename=venues.txt'
    #writing lines
    # lines=["this is 1st line\n"
    #        ,"this is line two"]
    #write to textfile
    #designate the model
    venues=Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n')
    response.writelines(lines)
    return response

def search_venue(request):
    if request.method=='POST':
        searched=request.POST.get('searched',)
        venues=Venue.objects.filter(name__contains=searched)
        print(venues)
        return render(request,'events/search_venues.html',{'searched':searched,'venues':venues})
    else:
        return render(request,'events/search_venues.html',{})
        
def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    name="kiran"
    print(month)
    month = month.capitalize()
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)
    #create calender
    cal=HTMLCalendar().formatmonth(year,month_number)
    #create datetime
    now=datetime.now()
    current_year=now.year
    #crrry the events date
    event_list=Event.objects.filter(event_date__year=year,event_date__month=month_number)
    #current time
    time=now.strftime('%I:%M:%p')
    # time=now.strftime('%I:%M:%S:%p')
    
    
    return render(request,'events/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "current_year":current_year,
        "time":time,
        "event_list":event_list,
        })


def all_events(request):
    event_list=Event.objects.all().order_by('-event_date')
    
    return render(request,"events/event_list.html",{"event_list":event_list})

def add_venue(request):
    submitted=False
    if request.method=='POST':
        form=VenueForm(request.POST,request.FILES)
        if form.is_valid():
            venue=form.save(commit=False)
            venue.owner=request.user.id #logged in user
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted=True
        return render(request,'events/add_venue.html',{'form':form,'submitted':submitted})
    
def list_venue(request):
    # venue_list=Venue.objects.all().order_by('name','address')
    venue_list=Venue.objects.all()
    #pagination for list venue
    p=Paginator(Venue.objects.all(),2)
    page=request.GET.get('page')
    venues=p.get_page(page)
    nums="a" * venues.paginator.num_pages
    
    return render(request,'events/venues.html',{'venue_list':venue_list,'venues':venues,'nums':nums})    

def show_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue_owner=User.objects.get(pk=venue.owner)
    return render(request,'events/show_venues.html',{'venue':venue,'venue_owner':venue_owner}) 

def update_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    form=VenueForm(request.POST or None,request.FILES or None,instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venue')
    return render(request,'events/update_venue.html',{'venue':venue,'form':form}) 
     
def add_event(request):
    submitted=False
    if request.method=='POST':
        if request.user.is_superuser:
             form=EventFormAdmin(request.POST)
             if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form=EventForm(request.POST)     
            if form.is_valid():
                event=form.save(commit=False)
                event.manager=request.user #logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
            
    else:
        #without going to the page
        if request.user.is_superuser:
            form=EventFormAdmin
        else:    
            form=EventForm()
        if 'submitted' in request.GET:
            submitted=True
        return render(request,'events/add_event.html',{'form':form,'submitted':submitted})    
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})

def update_event(request,event_id):
    event=Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form=EventFormAdmin(request.POST or None,instance=event)
    else:    
        form=EventForm(request.POST or None,instance=event)
    if form.is_valid():
        form.save()
        return redirect('list')
    return render(request,'events/update_event.html',{'events':event,'form':form,'hi':"hi"})

def delete_event(request,event_id):
    event=Event.objects.get(pk=event_id)
    if request.user==event.manager:
        event.delete()
        messages.success(request,("Event deleted successfully"))
        return redirect('list')
    else:
        messages.success(request,("You cannot delete Event"))
        return redirect('list')
        
def delete_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venue')

def my_events(request):
        if request.user.is_authenticated:
            me=request.user.id
            print(me)
            events=Event.objects.filter(attendees=me)
            print(events)
            return render(request,"events/my_events.html",{'events':events})
        else:
            messages.success(request,("You cant acces it"))
            return redirect('home')
        

def search_events(request):
    if request.method=='POST':
        searched=request.POST.get('searched',)
        events=Event.objects.filter(name__contains=searched)#(description__contains==searched) kodukkuvanel ddescriptionil ulla pole search cheyyum
        print(events)
        return render(request,'events/search_events.html',{'searched':searched,'events':events})
    else:
        return render(request,'events/search_events.html',{})        
    
def admin_approval(request):
    event_list=Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method=="POST":
            id_list=request.POST.getlist('boxes')
            # print(id_list)
            #uncheck all events
            event_list.update(approved=False)
            #update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request,("Approved successfully."))
            return redirect('list')  
        else:
           return render(request,'events/admin_approval.html',{'event_list':event_list})    
               
    else:
        messages.success(request,("You cannot access this page."))
        return redirect('home')
    return render(request,'events/admin_approval.html',{})    