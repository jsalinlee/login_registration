from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NUM_REGEX = re.compile(r'^[a-zA-Z]+$')
# Manager
class UserManager(models.Manager):
    def register(self, regData):
        error_messages = ["First name must be at least 2 characters!", "First name can't have numbers or special characters!", "Last name must be at least 2 characters!", "Last name can't have numbers or special characters!", "Invalid email!", "Password must be at least 8 characters!", "Password and confirmation do not match!", "That email is already taken."]
        error_list = []
        if len(regData['fname']) < 2:
            error_list.append(error_messages[0])
        if not NUM_REGEX.match(regData['fname']):
            error_list.append(error_messages[1])
        if len(regData['lname']) < 2:
            error_list.append(error_messages[2])
        if not NUM_REGEX.match(regData['lname']):
            error_list.append(error_messages[3])
        if not EMAIL_REGEX.match(regData['email']):
            error_list.append(error_messages[4])
        for i in range(len(User.objects.all())):
            if regData['email'] == User.objects.all()[i].email:
                error_list.append(error_messages[7])
        if len(regData['password']) < 8:
            error_list.append(error_messages[5])
        if regData['password'] != regData['pass_conf']:
            error_list.append(error_messages[6])
        if error_list == []:
            last_reg = self.create(fname = regData['fname'], lname = regData['lname'], email = regData['email'], password = bcrypt.hashpw(regData['password'].encode(), bcrypt.gensalt()))
            return (True, last_reg.id)
        else:
            return (False, error_list)
    def login(self, logData):
        for i in User.objects.all():
            if logData['log_email'] == i.email:
                if bcrypt.hashpw(logData['log_pass'].encode(), i.password.encode()) == i.password:
                    print "login success!"
                    return True
        return False

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length = 255)
    lname = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
