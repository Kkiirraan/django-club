from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegsiterUserForm

def login_user(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("There is an error in loggin in."))
            return redirect('login_user')
            
    else:    
      return render(request,'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("Successfully logged out "))
    return redirect('home')


def register(request):
    if request.method=="POST":
        form=RegsiterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("Succesfully Registerd"))
            return redirect('home')
    else:
        form=RegsiterUserForm()
            
    return render(request,'authenticate/register_user.html',{'form':form})