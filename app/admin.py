from django.contrib import admin
from app.models import *

# Register your models here.

admin.register(Profile)
admin.register(Tag)
admin.register(Question)
admin.register(QuestionLike)
admin.register(Answer)
admin.register(AnswerLike)

admin.register(QuestionTag)

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(QuestionLike)
admin.site.register(Answer)
admin.site.register(AnswerLike)

admin.site.register(QuestionTag)