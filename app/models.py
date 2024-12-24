from django.db import models
from django.contrib.auth.models import User

# Managers

class ProfileManager(models.Manager):
    def popular(self):
        return self.annotate(
            answers_count = models.Count("answer_author")
		).order_by("-answers_count")[:5]

class TagsManager(models.Manager):
	def popular(self):
		return self.annotate(
			question_count = models.Count("question_tags")
		).order_by("question_count")[:15]

class QuestionManager(models.Manager):
    def latest(self):
        return self.order_by("-createdAt")
    
    def popular(self):
        return self.annotate(likes_count = models.Count("question_like")).order_by("-likes_count")
    
# Models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="images/", null=True, blank=True, default="/default_profile.webp")
    objects = ProfileManager()

class Tag(models.Model):
	name = models.CharField(max_length=50)
	objects = TagsManager()

class Question(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    createdAt = models.DateTimeField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="question_tags", through="QuestionTag")
    objects = QuestionManager()
    
    def answers(self):
        return self.question_answer.annotate(likes_count = models.Count("answer_like")).order_by("createdAt").order_by("-likes_count")

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_like")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="question_author")

    class Meta:
        constraints = [
            models.UniqueConstraint('question', 'author', name='question_author_unique'),
        ]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_answer")
    description = models.CharField(max_length=256)
    createdAt = models.DateTimeField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answer_author")
    
    isRight = models.BooleanField(default=False)
    
    def likes_count(self):
        return self.answer_like.count()

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_like")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint('answer', 'author', name='answer_author_unique'),
        ]

# Tables for Many-To-Many

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)