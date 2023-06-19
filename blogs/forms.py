from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . logger import logging
class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username","email","password1","password2")

    def save(self, commit = True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            # user.set_default("is_staff",True)
            user.save()
            logging.info("user created successfully")
        return user