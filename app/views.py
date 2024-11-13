from django.shortcuts import render
from app.context import *

# Create your views here.

def indexPage(request):
    return render(request, 'index.html', indexPageContext(request))

def hotPage(request):
    return render(request, 'hot.html', hotPageContext   (request))

def tagPage(request, tag_name):
    return render(request, 'tag.html', context=tagPageContext(request, tag_name))

def questionPage(request, question_id):
    return render(request, 'question.html', context=questionPageContext(request, question_id))

def loginPage(request):
    return render(request, 'login.html', context=defaultNotLoginContext(request))

def signUpPage(request):
    return render(request, 'signup.html', context=defaultNotLoginContext(request))

def askPage(request):
    return render(request, 'ask.html', context=defaultContext(request))

def settingsPage(request):
    return render(request, 'settings.html', context=defaultContext(request))