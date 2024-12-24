from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from random import choice, choices
from time import time

from app.models import *

def printProgress(self, progress, max_value, start_time, message):
    if progress != -1:
        self.stdout.write(
            self.style.HTTP_INFO(f'{message.ljust(25, ' ')} [{format(time() - start_time, "2.2f")}s; {int(progress / max_value * 100)}%]    \r'),
            ending=""
        )
        self.stdout.flush()
    else:
        self.stdout.write(
            self.style.SUCCESS(f'{message.ljust(25, ' ')} [{format(time() - start_time, "2.2f")}s] - Done!'),
        )

class Command(BaseCommand):
    help = "Command for generate test database"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs="+", type=int)

    def handle(self, *args, **options):

        ratio = options["ratio"][0]
        dbBuffer = 1000

        # Создание тэгов

        index = 0
        totalCount = ratio
        allTags = [None] * totalCount

        start = time()
        printProgress(self, 0, totalCount, start, "Создание тэгов...")
        while index < totalCount:
            newTags = []

            for j in range(min(totalCount - index, dbBuffer)):
                newTag = Tag(name=f"tag #{index}")
                newTags.append(newTag)
                allTags[index] = newTag
                index += 1

                printProgress(self, index, totalCount, start, "Создание тэгов...") 

            Tag.objects.bulk_create(newTags)
        printProgress(self, -1, totalCount, start, "Создание тэгов...")

        # Создание профилей и пользователей

        index = 0
        totalCount = ratio
        allProfiles = [None] * totalCount

        start = time()
        printProgress(self, 0, totalCount, start, "Создание пользователей...")
        while index < totalCount:
            newProfiles = []
            newUsers = []

            for j in range(min(totalCount - index, dbBuffer)):
                user = User(username=f"user_{index}", email=f"user_{index}@gmail.com", password="password")
                profile = Profile(user=user, avatar="/default_profile.webp")
                
                allProfiles[index] = profile
                newUsers.append(user)
                newProfiles.append(profile)
                index += 1

                printProgress(self, index, totalCount, start, "Создание пользователей...") 

            User.objects.bulk_create(newUsers)
            Profile.objects.bulk_create(newProfiles)
        printProgress(self, -1, totalCount, start, "Создание пользователей...")

        # Создание вопросов

        index = 0
        totalCount = ratio * 10
        allQuestions = [None] * totalCount

        start = time()
        printProgress(self, 0, totalCount, start, "Создание вопросов...")
        while index < totalCount:
            newQuestions = []

            for j in range(min(totalCount - index, dbBuffer)):
                author = choice(allProfiles)
                question = Question(
                    name=f"Question #{index + 1}",
                    description=f"This is question about very important thing...)",
                    createdAt=timezone.now(),
                    author=author,
                )
                
                allQuestions[index] = question
                newQuestions.append(question)
                index += 1

                printProgress(self, index, totalCount, start, "Создание вопросов...") 

            Question.objects.bulk_create(newQuestions)
        printProgress(self, -1, totalCount, start, "Создание вопросов...")

        # Создание лайков для вопросов

        index = 0
        totalCount = ratio * 100
        allQuestionsLikes = set()

        start = time()
        printProgress(self, 0, totalCount, start, "Лайки для вопросов...")
        while index < totalCount:
            newLikes = []

            for j in range(min(totalCount - index, dbBuffer)):
                author = choice(allProfiles)
                question = choice(allQuestions)

                if f"{author.id};{question.id}" in allQuestionsLikes:
                    continue
                
                allQuestionsLikes.add(f"{author.id};{question.id}")

                like = QuestionLike(
                    question=question,
                    author=author,
                )
                
                newLikes.append(like)
                index += 1

                printProgress(self, index, totalCount, start, "Лайки для вопросов...") 

            QuestionLike.objects.bulk_create(newLikes)
        printProgress(self, -1, totalCount, start, "Лайки для вопросов...")

        # Привязка тэгов к вопросам

        index = 0
        totalCount = len(allQuestions)

        start = time()
        printProgress(self, 0, totalCount, start, "Тэги для вопросов...")
        while index < totalCount:
            newQuestionTags = []

            for j in range(min(totalCount - index, dbBuffer)):
                tags = choices(allTags, k=5)

                for tag in tags:
                    questionTag = QuestionTag(
                        question=allQuestions[index],
                        tag=tag,
                    )
                    newQuestionTags.append(questionTag)

                index += 1
                printProgress(self, index, totalCount, start, "Тэги для вопросов...") 

            QuestionTag.objects.bulk_create(newQuestionTags)
        printProgress(self, -1, totalCount, start, "Тэги для вопросов...")

        # Создание ответов

        index = 0
        totalCount = ratio * 100
        allAnswers = [None] * totalCount

        start = time()
        printProgress(self, 0, totalCount, start, "Создание ответов...")
        while index < totalCount:
            newAnswers = []

            for j in range(min(totalCount - index, dbBuffer)):
                author = choice(allProfiles)
                question = choice(allQuestions)
                answer = Answer(
                    question=question,
                    description=f"This is answer for very important question...)",
                    createdAt=timezone.now(),
                    author=author,
                )
                
                allAnswers[index] = answer
                newAnswers.append(answer)
                index += 1

                printProgress(self, index, totalCount, start, "Создание ответов...") 

            Answer.objects.bulk_create(newAnswers)
        printProgress(self, -1, totalCount, start, "Создание ответов...")

        # Создание лайков для ответов

        index = 0
        totalCount = ratio * 100
        allAnswersLikes = set()

        start = time()
        printProgress(self, 0, totalCount, start, "Лайки для ответов...")
        while index < totalCount:
            newLikes = []

            for j in range(min(totalCount - index, dbBuffer)):
                author = choice(allProfiles)
                answer = choice(allAnswers)

                if f"{author.id};{answer.id}" in allAnswersLikes:
                    continue
                
                allAnswersLikes.add(f"{author.id};{answer.id}")

                like = AnswerLike(
                    answer=answer,
                    author=author,
                )
                
                newLikes.append(like)
                index += 1

                printProgress(self, index, totalCount, start, "Лайки для ответов...") 

            AnswerLike.objects.bulk_create(newLikes)
        printProgress(self, -1, totalCount, start, "Лайки для ответов...")
        
        self.stdout.write(
            self.style.SUCCESS('-' * 42 + "\n" + "БД успешно сгенерирована!" + "\n" + '-' * 42),
        )