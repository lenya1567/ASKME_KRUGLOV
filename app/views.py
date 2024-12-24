from django.shortcuts import render
from app.context import *

# Create your views here.

def indexPage(request):
    return pageView(request, 'index.html', indexPageContext(request))

def hotPage(request):
    return pageView(request, 'hot.html', hotPageContext (request))

def tagPage(request, tag_name):
    return pageView(request, 'tag.html', context=tagPageContext(request, tag_name))

def questionPage(request, question_id):
    return pageView(request, 'question.html', context=questionPageContext(request, question_id))

def loginPage(request):
    return pageView(request, 'login.html', context=loginPageContext(request))

def signUpPage(request):
    return pageView(request, 'signup.html', context=registerPageContext(request))

def askPage(request):
    return pageView(request, 'ask.html', context=askPageContext(request))

def settingsPage(request):
    return pageView(request, 'settings.html', context=settingsContext(request))

def logoutPage(request):
    return logoutContext(request)