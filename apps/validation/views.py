from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
# Create your views here.
def index(req):
    return render(req, 'validation/index.html')
def register(req):
    if req.method == "POST":
        if User.objects.register(req.POST)[0]:
            req.session['user_id'] = User.objects.register(req.POST)[1]
            messages.info(req, "Thank you for registering!")
            return redirect('/success')
        else:
            for error in User.objects.register(req.POST)[1]:
                messages.info(req, error)
            return redirect('/')
def success(req):
    if 'user_id' not in req.session:
        messages.info(req, "Please log in.")
        return redirect('/')
    context = {
        'current_user': User.objects.filter(id = req.session['user_id'])
    }
    return render(req, 'validation/success.html', context)
def login(req):
    if req.method == 'POST':
        if User.objects.login(req.POST):
            req.session['user_id'] = User.objects.filter(email = req.POST['log_email'])[0].id
            messages.info(req, "You've successfully logged in.")
            return redirect('/success')
    return redirect('/')
def logout(req):
    req.session.clear()
    messages.info(req, "You've successfully logged out. Have a nice day!")
    return redirect('/')
