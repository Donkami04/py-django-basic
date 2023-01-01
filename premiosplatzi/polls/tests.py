import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

def create_quesiton(question_text, days):     
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time) 

def create_choice(question, choice_text, vote):
    choice = Choice.objects.create(question=question, choice_text=choice_text, votes=vote)
    return choice


class QuestionMethodTestCase(TestCase):
    
    def testing_was_published_recently_30days_after(self):
        time = timezone.now() + datetime.timedelta(days=30)
        fake_question = Question(question_text="Azul o amarillo", pub_date=time)
        self.assertEqual(fake_question.was_published_recently(), False ) 

    def testing_was_published_recently_now(self):
        time = timezone.now()
        fake_question = Question(question_text="Azul o amarillo", pub_date=time)
        self.assertEqual(fake_question.was_published_recently(), True )
        
    def testing_was_published_recently_afer_two_days(self):
        time = timezone.now() - datetime.timedelta(days=2)
        fake_question = Question(question_text="Azul o amarillo", pub_date=time)
        self.assertEqual(fake_question.was_published_recently(), False )             
 

class QuestionIndexViewTestCase(TestCase):
    
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are avaible.')
        self.assertQuerysetEqual(response.context['lates_question_list'], [])
        
    def test_show_questions_lte_date_now(self):
        question = create_quesiton("Past question", days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lates_question_list'], [question])

    def test_show_questions_gte_date_now(self):
        create_quesiton("future question", days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are avaible.')
        self.assertQuerysetEqual(response.context['lates_question_list'], [])
        
    def test_display_only_past_questions(self):
        past_question = create_quesiton("Past question", days=-10)
        future_question = create_quesiton("future question", days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lates_question_list'], [past_question])
        
    def test_display_all_the_past_questions(self):
        past_question1 = create_quesiton("Past question 1", days=-10)
        past_question2 = create_quesiton("Past question 2", days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lates_question_list'], [past_question1, past_question2])
        
    def test_dont_display_future_questions(self):
        create_quesiton("future question 1", days=+10)
        create_quesiton("future question 2", days=+20)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are avaible.')
        self.assertQuerysetEqual(response.context['lates_question_list'], [])
        
    # def test_question_with_atleast_2_choices_could_be_displayed(self):
    #     question = create_quesiton("Past question", days=-10)
    #     choice1 = create_choice(question, "choice 1", 0)
    #     choice2 = create_choice(question, "choice 2", 0)
    #     response = self.client.get(reverse('polls:index'))-
    #     self.assertQuerysetEqual(response.context['lates_question_list'], [question])
        
class QuestionDetailViewTestCase(TestCase):
    
    def test_future_question_detail(self):
        future_question = create_quesiton("future question", days=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
class QuestionResultViewTestCase(TestCase):

    def test_display_results_from_a_past_question(self):
        question = create_quesiton("This is a question", days=-10)
        choice = create_choice(question, "This is a choice", 10)
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
        self.assertContains(response, choice.votes)
        self.assertContains(response, choice.choice_text)
    
    def test_dont_display_results_from_a_future_question(self):  
        future_question = create_quesiton("future question", days=10)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_display_only_the_result_from_a_old_question_between_many_questions(self):
        past_question = create_quesiton("Past question", days=-10)
        future_question = create_quesiton("future question", days=10)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        self.assertNotContains(response, future_question.question_text)

    
 