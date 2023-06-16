from django.shortcuts import render

def index(request):
    return render(request, 'post/post.html')

def posting(request):
    return render(request, 'post/service-details.html')

def faq(request):
    return render(request, 'post/faq.html')