from .models import Question, Choice

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


# def home_polls(request):
#     lates_question_list = Question.objects.all()
#     return render(request, 'polls/index.html', {'lates_question_list': lates_question_list})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lates_question_list'    
    
    def get_queryset(self):
        return Question.objects.all()
        
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(question.pub_date)
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # ! id_choice
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Seleccione una opción válida"
        })


