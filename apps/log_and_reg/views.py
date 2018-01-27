from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# Create your views here.
import bcrypt
from models import *

def index(request):
    if request=='POST':
        return redirect('/')
    else:
        return render(request, 'log_and_reg/index.html')

def success(request):
    print "success"
    if request.session['user_id']:
        return render(request, 'log_and_reg/success.html', {"user": User.objects.get(id=request.session['user_id'])})
    else:
        return redirect('/')

def processRegistration(request):
    print("************")
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print email
        User.objects.create(first_name = first_name, last_name = last_name, email = email, password = password)
        this_user = User.objects.get(email=email)
        # user id in session
        request.session['user_id'] = this_user.id
        errors["success"] = "Successfully registered (or logged in)!"
        return redirect('/success')

def processLogin(request):
    email = request.POST['email']
    print "Trying to log in"
    try:
        this_user = User.objects.get(email=email)
        print this_user
        if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            request.session['user_name'] = this_user.first_name
            print "Logged in"
            messages.error(request, "Successfully registered (or logged in)!")
            return redirect('/success')
        else:
            print "wrong password"
            messages.error(request, "Wrong password")
            return redirect('/')
    except:
        messages.error(request, "Email not found")
        return redirect('/')

def logout(request):
    request.session['user_id'] = None
    print "Logged out"
    return redirect('/')
