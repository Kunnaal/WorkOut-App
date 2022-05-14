from django.http import HttpResponse
from django.shortcuts import redirect, render

def home(request):
    return HttpResponse(render(request, 'welcome/index.html'))

def dne(request):
    return HttpResponse(render(request, 'welcome/dne.html'))