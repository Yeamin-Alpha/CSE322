from django.shortcuts import render


def login(request):
    return render(request,template_name='login.html')

def index(request):
    return render(request,template_name='index.html')