from django import forms
from notes.models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):

    class Meta:

        model=Task

        # fields="__all__"

        exclude=("created_date","status","updated_status","user")

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control"}),

            "description":forms.Textarea(attrs={"class":"form-control"}),

            "due_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),

            "category":forms.Select(attrs={"class":"form-control form-select"})

        }


class RegistrationForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]

        widgets={
            "password":forms.PasswordInput()
        }


class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField(widget=forms.PasswordInput())

    