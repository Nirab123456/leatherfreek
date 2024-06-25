from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'events/index.html')

def index_trial(request):
    return render(request, 'events/index_trial.html')