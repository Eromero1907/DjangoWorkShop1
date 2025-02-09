from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    # return HttpResponse('<h1>Welcome to Home Page</h1>')
    return render(request, 'home.html', {'name':'Esteban Romero'})

def about(request):
    # return HttpResponse('<h1>Welcome to About page</h1>')
    return render(request, 'about.html', {'name':'Esteban Romero'})