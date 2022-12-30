import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice

class QuestionTestCasse(TestCase):
    
    def testing_was_published_recently(self):
        time = timezone.now() + datetime.timedelta(days=30)
        fake_question = Question(question_text="Azul o amarillo", pub_date=time)
        self.assertIs(fake_question.was_published_recently(), False )        