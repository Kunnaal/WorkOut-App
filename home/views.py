from django.shortcuts import render

def home(request):
    return render(request, 'authentication/index.html')