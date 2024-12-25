from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from app.models import *

NullPlaceholder = {"placeholder": ""}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Login", widget=forms.TextInput(attrs=NullPlaceholder))
    password = forms.CharField(max_length=32, required=True, label="Password", widget=forms.PasswordInput(attrs=NullPlaceholder))
    
    def clean(self):
        data = super().clean()
        username = data.get("username")
        
        if username == None or not username.replace("_", "").isalnum():
            self.add_error("username", "Can contains only letters, numbers and symbol '_'!")
        
        return data 

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=20, required=True, label="Login", widget=forms.TextInput(attrs=NullPlaceholder))
    email = forms.EmailField(max_length=32, required=True, label="Email", widget=forms.EmailInput(attrs=NullPlaceholder))
    first_name = forms.CharField(max_length=32, required=True, label="NickName", widget=forms.TextInput(attrs=NullPlaceholder))
    password = forms.CharField(max_length=32, required=True, label="Password", widget=forms.PasswordInput(attrs=NullPlaceholder))
    repeatPassword = forms.CharField(max_length=32, required=True, label="Repeat password", widget=forms.PasswordInput(attrs=NullPlaceholder))
    avatar = forms.ImageField(label="Upload avatar", required=False, widget=forms.FileInput(attrs={ "accept": ".gif,.jpg,.jpeg,.png" }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password')
    
    def clean(self):
        data = super().clean()
    
        password = data.get("password")
        repeatPassword = data.get("repeatPassword")
        
        if password != repeatPassword:
            self.add_error("repeatPassword", "Passwords don't match!")
        
        return data
        
    def save(self, file, commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        user.save()
        
        profile = Profile.objects.create(user=user)
        
        if file != None:
            profile.avatar.save(file.name, file)
        
        profile.save()
        
        return user

class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=20, required=True, label="Login", widget=forms.TextInput(attrs=NullPlaceholder))
    email = forms.EmailField(max_length=32, required=True, label="Email", widget=forms.EmailInput(attrs=NullPlaceholder))
    first_name = forms.CharField(max_length=32, required=True, label="NickName", widget=forms.TextInput(attrs=NullPlaceholder))
    avatar = forms.ImageField(label="Upload avatar", required=False, widget=forms.FileInput(attrs={ "accept": ".gif,.jpg,.jpeg,.png" }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
    
    def clean(self):
        data = super().clean()
        
        password = data.get("password")
        repeatPassword = data.get("repeatPassword")
        
        if password != repeatPassword:
            self.add_error("repeatPassword", "Passwords don't match!")
        
        return data
        
    def save(self, file, commit=True):
        user = super().save(commit=True)
        
        profile = Profile.objects.get(user=user)
        
        if file != None:
            profile.avatar.save(file.name, file)
        
        profile.save()
        
        return user

class QuestionForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, label="Name", widget=forms.TextInput(attrs=NullPlaceholder))
    description = forms.CharField(max_length=256, required=True, label="Description", widget=forms.Textarea(attrs=NullPlaceholder))
    tags = forms.CharField(max_length=50, required=True, label="Tags", widget=forms.TextInput(attrs=NullPlaceholder))
    
    class Meta:
        model = Question
        fields = ('name', 'description')
    
    def clean(self):
        data = super().clean()
        
        tags = data.get("tags")
        
        if tags == None or not tags.replace("_", "").replace(" ", "").isalnum():
            self.add_error("tags", "Tag can contains only letters, numbers and symbol '_'!")
        
        return data
        
    def save(self, user, commit=True):
        question = super().save(commit=False)
        
        tags = []
        for tag in list(set(self.cleaned_data["tags"].split())):
            dbTags = Tag.objects.filter(name=tag)
            if len(dbTags) == 0:
                newTag = Tag.objects.create(name=tag)
                newTag.save()
                tags.append(newTag)
            else:
                tags.append(dbTags[0])
        
        question.createdAt = timezone.now()
        question.author = user.profile        
        question.save()
        
        question.tags.set(tags)
        
        return question

class AnswerForm(forms.ModelForm):
    description = forms.CharField(max_length=50, required=True, label="Description:", widget=forms.Textarea(attrs={ "placeholder": "Enter your answer here..." }))
    
    class Meta:
        model = Answer
        fields = ('description',)
        
    def save(self, user, question, commit=True):
        answer = super().save(commit=False)
        
        answer.createdAt = timezone.now()
        answer.author = user.profile
        answer.question = question
        answer.save()
        
        return answer