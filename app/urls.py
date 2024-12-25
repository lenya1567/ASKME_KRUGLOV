from django.urls import path

from app import views

urlpatterns = [ 
    path('', views.indexPage, name="index"),
    path('hot', views.hotPage, name="hot_question"),
    path('tag/<str:tag_name>', views.tagPage, name="tag"),
    path('question/<int:question_id>', views.questionPage, name="question"),
    path('question/right', views.setRightAnswer, name="right_answer"),
    path('make_like', views.createLike, name="like"),
    path('login', views.loginPage, name="login"),
    path('signup', views.signUpPage, name="signup"),
    path('ask', views.askPage, name="ask"),
    path('settings', views.settingsPage, name="settings"),
    path('logout', views.logoutPage, name="logout")
]
