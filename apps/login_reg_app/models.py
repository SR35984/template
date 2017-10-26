from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors =[]
        name = form_data['name']
        alias = form_data['alias']
        email = form_data['email'].lower()
        password = form_data['password']
        confirmation_password = form_data['password_confirmation']

        if len(name) == 0:
            errors.append("First Name is required.")

        if len(alias) == 0:
            errors.append("Last Name is required.")
      
        if len(email) == 0:
            errors.append("Email is required.")
        elif not EMAIL_REGEX.match(email):
            errors.append("Not a valid email!")
      
        if len(password) == 0:
            errors.append("Password is required.")
        if len(password) < 8:
            errors.append("Password must be > 8 characters long")
        elif password != confirmation_password:
            errors.append("Passwords must match.")

        if not errors:
            user_list = self.filter(email=email)
            if user_list:
                errors.append('Email already taken')

        return errors

    def validate_login(self, form_data):
        errors = []
        email = form_data['email'].lower()
        password = form_data['password']
       
        if len(email) == 0:
            errors.append("Email is required.")
       
        if len(password) == 0:
            errors.append("Password is required.")

        if not errors:
            user_list = User.objects.filter(email=email)

            if user_list:
                user = user_list[0]
                user_password = password.encode()
                db_password = user.password.encode()

                if bcrypt.checkpw(user_password, db_password):
                    return {'user': user}

        errors.append("Email or Password invalid")

        return {'errors': errors}

    def create_user(self, form_data):
        password = form_data['password']
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        return User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'].lower(),
            password = hashedpw,
    )

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()