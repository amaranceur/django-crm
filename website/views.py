from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from . import forms # Import messages framework# Create your views here.
from .models import Record
def home(req): 
    records = Record.objects.all()
    if req.method=="POST":
        username= req.POST['username']
        password=req.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(req,user)
            messages.success(req,"you have been log in")
            return redirect('home')
        else:
            messages.error(req,"you have mistaken") 
            return redirect('home')   
    return render(req,'website/home.html',{'records':records})

def logout_user(req):
    logout(req)
    messages.success(req,'You have been logged out')
    return redirect('home')
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists.")
        elif password1 != password2:
            messages.error(request, "Passwords don't match.")
        else:
            try:
                # Validate the password
                validate_password(password1)
                
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password1)
                if user:
                    messages.success(request, "You have registered successfully!")
                    login(request, user)
                    return redirect('home')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)  # Display specific validation errors

    return render(request, "website/register.html", {})
def add_record(req):
    if req.method == "POST":
        firstname = req.POST['first_name']
        lastname = req.POST['last_name']
        email = req.POST['email']
        number = req.POST['number']
        state = req.POST['state']
        zipcode = req.POST['zipcode']

        record = Record.objects.create(
            first_name=firstname,
            last_name=lastname,
            email=email,
            number=number,
            state=state,
            zipcode=zipcode
        )

        if record:
            messages.success(req, "You have added the record successfully")
            return redirect('home')
        else:
            messages.error(req, "Failed to add the record")

    return render(req, 'website/add_record.html', {})
def costumer_record(req,pk):
    customer=Record.objects.get(id=pk)
    return render(req,'website/record.html',{'customer':customer})
def delete_record(req,pk):
    if req.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(req, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(req, "You Must Be Logged In To Do That...")
        return redirect('home')
def update_record(req,pk):
    if req.user.is_authenticated:
        customer=Record.objects.get(id=pk)
        if req.method=='POST':
            customer.first_name=req.POST['first_name']
            customer.last_name=req.POST['last_name']
            customer.email=req.POST['email']
            customer.number=req.POST['number']
            customer.state=req.POST['state']
            customer.zipcode=req.POST['zipcode']
            try:
                customer.full_clean()
                customer.save()
                messages.success(req, "Record updated successfully.")
                return redirect('home')
            except ValidationError as e:
                messages.error(req, "Please correct the error below.")
                for field, error in e.message_dict.items():
                    messages.error(req, f"{field}: {error}")
    return render(req, 'website/update_record.html', {'customer': customer})