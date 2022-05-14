from django.shortcuts import render
from django.test import TestCase

# Create your tests here.
def home(request):
    return render(request, 'authentication/index.html')

def index(request, fname):
    return render(request, 'authentication/index.html', {'fname': user.first_name})
