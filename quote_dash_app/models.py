from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']="First name must be longer than 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name']="Last name must be longer than 2 characters"
        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']="Password must be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw']="Password and confirm password must match"
        return errors
    def authenticate(self, email, password):
        logged_users = self.filter(email=email)
        if not logged_users:
            return False
        logged_user = logged_users[0]
        return bcrypt.checkpw(password.encode(), logged_user.password.encode())
    def profile_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])==0:
            errors['first_name'] = "First Name field cannot be left blank"
        if len(postData['last_name'])==0:
            errors['last_name']= "Last Name field cannot be left blank"
        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        return errors
    def email_edit_validator(request, postData):
        email_error={}
        to_check = User.objects.filter(email=postData['email'])
        if len(to_check)>0:
            print(to_check)
            email_error['reg_email'] = "Email is already registered"
        return email_error

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author'])<4:
            errors['author']="Author name must be more than 3 characters"
        if len(postData['content'])<11:
            errors['content']="Quote must be more than 10 characters"
        return errors 

class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()