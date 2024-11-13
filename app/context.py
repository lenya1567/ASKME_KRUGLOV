from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from app.models import *

testUser = {
    "name": "Master Yoda",
    "avatar": "/img/avatars/profile_1.svg",
}

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

def indexPageContext(request):
    page = paginate(Question.objects.latest(), request)
    return {
        "questions": page.object_list, 
        "page": page, 
        "user": testUser,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def hotPageContext(request):
    page = paginate(Question.objects.popular(), request)
    return {
        "questions": page.object_list, 
        "page": page, 
        "user": testUser,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def tagPageContext(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    page = paginate(tag.question_tags.all(), request)
    return {
        "tag": tag,
        "questions": page.object_list, 
        "page": page, 
        "user": testUser,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def questionPageContext(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    page = paginate(question.question_answer.all(), request)
    return {
        "question": question,
        "answers": page.object_list, 
        "page": page, 
        "user": testUser,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def defaultContext(request):
    return {
        "user": testUser,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }

def defaultNotLoginContext(request):
    return {
        "user": None,
        "popular_tags": Tag.objects.popular(),
        "popular_authors": Profile.objects.popular(),
    }
