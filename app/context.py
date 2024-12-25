from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse

from urllib.parse import urlencode

from app.models import *
from app.forms import *

def paginate(objects_list, request, per_page=10):
    try: 
        page_index = request.GET.get("page", "1")
    except: 
        page_index = 1

    paginator = Paginator(objects_list, per_page)

    try: 
        page = paginator.get_page(page_index)
    except (PageNotAnInteger, EmptyPage): 
        page = 1

    return page

def pageView(request, template, context):
    if type(context) == dict:
        return render(request, template, context)
    else:
        return context

def indexPageContext(request):
    page = paginate(Question.objects.latest(), request)
    return {
        "questions": loadQuestionsLike(page.object_list, request.user), 
        "page": page,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def hotPageContext(request):
    page = paginate(Question.objects.popular(), request)
    return {
        "questions": loadQuestionsLike(page.object_list, request.user), 
        "page": page, 
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def tagPageContext(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    page = paginate(tag.question_tags.all(), request)
    return {
        "tag": tag,
        "questions": loadQuestionsLike(page.object_list, request.user), 
        "page": page, 
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def questionPageContext(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    form = AnswerForm
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(request.user, question)
            pageIndex = abs(len(question.answers()) - 1) // 10 + 1
            return redirect(reverse("question", args=[question.id]) + f"?page={pageIndex}#answer_{answer.id}")
    
    page = paginate(question.answers(), request)
    
    return {
        "form": form,
        "question": loadQuestionsLike(question, request.user),
        "answers": loadAnswersLike(page.object_list, request.user), 
        "page": page, 
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def loginPageContext(request):
    form = LoginForm
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.GET.get("continue", "/"))
            else:
                form.add_error("username", "Пользователь не найден!")
    
    return {
        "form": form,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }
    
def registerPageContext(request):
    form = RegisterForm
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(request.FILES.get('avatar'))
            user = auth.authenticate(**form.cleaned_data)
            auth.login(request, user)
            return redirect(reverse('index'))
    
    return {
        "form": form,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

@login_required(redirect_field_name="continue")
def settingsContext(request):
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(request.FILES.get('avatar'))
            
    form = SettingsForm(instance=request.user)
    
    return {
        "form": form,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }
    
@login_required(redirect_field_name="continue")
def askPageContext(request):
    form = QuestionForm
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            newQuestion = form.save(request.user)
            return redirect(reverse("question", args=[newQuestion.id]))
    
    return {
        "form": form,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def defaultContext(request):
    return {
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def defaultNotLoginContext(request):
    return {
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def logoutContext(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

# AJAX

def createLikeResponse(request):
    if request.method == "POST":
        likeType = request.POST.get("type") # 0 - for question, 1 - for answer
        id = request.POST.get("id") # id of question or of answer
        if likeType == '0':
            question = get_object_or_404(Question, id=id)
            like, createdNew = QuestionLike.objects.get_or_create(question=question, author=request.user.profile)
            if not createdNew:
                like.delete()
            return JsonResponse({ "likes_count": question.question_like.count() })
        else:
            answer = get_object_or_404(Answer, id=id)
            like, createdNew = AnswerLike.objects.get_or_create(answer=answer, author=request.user.profile)
            if not createdNew:
                like.delete()
            return JsonResponse({ "likes_count": answer.answer_like.count() })
    else:
        return JsonResponse({ "error": 405 })
    
def setRightAnswerResponse(request):
    if request.method == "POST":
        questionId = request.POST.get("question")
        rightAnswerId = request.POST.get("answer")
        
        question = get_object_or_404(Question, id=questionId)
        rightAnswer = get_object_or_404(Answer, id=rightAnswerId)
        
        if question.author == request.user.profile:
            question.changeRightAnswer(rightAnswer)
            return JsonResponse({ "error": 0 })
        else:
            return JsonResponse({ "error": 403 })
    else:
        return JsonResponse({ "error": 405 })