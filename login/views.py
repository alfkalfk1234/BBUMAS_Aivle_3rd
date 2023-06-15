from django.shortcuts import render

def index(request):
    return render(request, 'login/get-a-quote.html')