from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from random import randint, choice, choices

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

# Create your views here.

testUser = {
    "name": "Master Yoda",
    "avatar": "/img/avatars/profile_1.svg",
}

testTags = []
for i in range(50):
    testTags.append(f"Tag #{i}")

testQuestions = []
for i in range(100):
    testQuestions.append({
        "title": "title " + str(i + 1),
        "id": i,
        "text": "text" + str(i + 1),
        "date": i * randint(0, 1000),
        "tags": choices(testTags, k=5),
        "likes": randint(1, 10),
        "myLike": randint(1, 2) == 1,
        "answers_count": 0,
    })

testAnswers = []
for i in range(100):
    question = choice(testQuestions)
    question["answers_count"] += 1
    testAnswers.append({
        "title": "Answer " + str(i + 1),
        "id": i,
        "text": "My answer is " + str(i + 1),
        "date": i * randint(0, 1000),
        "tags": choices(question["tags"], k=2),
        "question": question["id"],
        "likes": randint(1, 10),
        "myLike": randint(1, 2) == 1,
    })

testTags.sort(key=lambda x: sum([x in question["tags"] for question in testQuestions]), reverse=True)

testHotQuestions = testQuestions.copy()
testHotQuestions.sort(key = lambda x: x["date"], reverse=True)

def indexPage(request):
    page = paginate(testQuestions, request)
    return render(request, 'index.html', context={ 
        "questions": page.object_list, 
        "page": page, 
        "user": testUser,
        "popular_tags": testTags[:15],
    })

def hotPage(request):
    page = paginate(testHotQuestions, request)
    return render(request, 'hot.html', context={ 
        "questions": page.object_list, 
        "page": page, 
        "user": testUser,
        "popular_tags": testTags[:15],
    })

def tagPage(request, tag_name):
    page = paginate(list(filter(lambda x: tag_name in x["tags"], testQuestions)), request)
    print(tag_name)
    return render(request, 'tag.html', context={ 
        "questions": page.object_list, 
        "page": page, 
        "user": testUser, 
        "popular_tags": testTags[:15],
        "tag_name": tag_name,
    })

def questionPage(request, question_id):
    questionsFilter = list(filter(lambda x: x["id"] == question_id, testQuestions))
    if len(questionsFilter) == 0:
        return HttpResponseNotFound("<h1>404: Question not found!") 
    page = paginate(list(filter(lambda x: x["question"] == question_id, testAnswers)), request)
    return render(request, 'question.html', context={ 
        "answers": page.object_list, 
        "page": page, 
        "user": testUser, 
        "popular_tags": testTags[:15],
        "question": list(filter(lambda x: x["id"] == question_id, testQuestions))[0],
    })

def loginPage(request):
    return render(request, 'login.html', context={ 
        "popular_tags": testTags[:15],
        "user": None,
    })

def signUpPage(request):
    return render(request, 'signup.html', context={  
        "popular_tags": testTags[:15],
        "user": None,
    })

def askPage(request):
    return render(request, 'ask.html', context={  
        "popular_tags": testTags[:15],
        "user": testUser,
    })

def settingsPage(request):
    return render(request, 'settings.html', context={  
        "popular_tags": testTags[:15],
        "user": testUser,
    })