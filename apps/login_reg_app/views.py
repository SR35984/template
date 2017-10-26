from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User

def flash_errors(errors, request):
    for error in errors:
       messages.error(request, error)

def current_user(request):
    return User.objects.get(id=request.session['user_id'])

def user(request, id):
	context={
		'user': current_user(request),
	}
	return render(request, 'login_reg_app/index.html')

def index(request):
    return render(request, 'login_reg_app/index.html')

def register(request):
    if request.method =="POST":
        errors = User.objects.validate_registration(request.POST)

        if not errors:
            user = User.objects.create_user(request.POST)
            request.session['user_id'] = user.id
            return redirect(reverse('success'))

        flash_errors(errors, request)
    return redirect(reverse('landing'))

def login(request):
    if request.method == "POST":
        check = User.objects.validate_login(request.POST)
        print check

        if 'user' in check:
            request.session['user_id'] = check['user'].id

            return redirect(reverse('success'))

        flash_errors(check['errors'], request)
    return redirect(reverse('landing'))

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'login_reg_app/success.html', context)

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')
    return redirect(reverse('landing'))
