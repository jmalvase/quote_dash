from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Quote

## RENDER
def index(request):
    return render(request, 'log_reg.html')
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'all_quotes' : Quote.objects.all()
    }
    return render(request, 'dash.html', context)

##LOGOUT
def logout(request):
    request.session.clear()
    return redirect('/')


## REGISTER
def register(request):
    if request.method=='POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/dash')
    return redirect('/')
def login(request):
    if request.method=="POST":
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/dash')
    return redirect('/')

## CREATE/EDIT/UPDATE
def add_quote(request):
    if request.method=="POST":
        errors = Quote.objects.quote_validator(request.POST)
        for error in errors:
            messages.error(request, errors[error])
            return redirect('/dash')
        Quote.objects.create(content=request.POST['content'], author=request.POST['author'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/dash')
    return redirect('/dash')
def edit_profile(request, user_id):
    edit_profile = User.objects.get(id=user_id)
    context = {
        'profile': edit_profile
    }
    return render(request, 'edit_profile.html', context)

def update_profile(request, profile_id):
    if request.method=="POST":
        errors = User.objects.profile_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(f'/my_account/{profile_id}')
        email_error = User.objects.email_edit_validator(request.POST)
        if email_error:
            for error in email_error:
                messages.error(request, email_error[error])
            return redirect(f'/my_account/{profile_id}')
        to_update=User.objects.get(id=profile_id)
        to_update.first_name=request.POST['first_name']
        to_update.last_name=request.POST['last_name']
        to_update.email=request.POST['email']
        to_update.save()
        return redirect(f'/user/{profile_id}')
    return redirect('/dash')


## READ
def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'profile.html', context)

## DELETE
def delete_quote(request, quote_id):
    Quote.objects.get(id=quote_id).delete()
    return redirect('/dash')

## LIKE
def like_quote(request, quote_id):
    liked_quote = Quote.objects.get(id=quote_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_quote.user_likes.add(user_liking)
    return redirect('/dash')


