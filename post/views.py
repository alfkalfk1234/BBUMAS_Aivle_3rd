from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Photo
from .forms import PostForm
from .utils import create_post
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/post.html', {'posts': posts})

# def posting(request):
#     return render(request, 'post/service-details.html')

def posting(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            region = request.POST.get('address')
            post = form.save(commit=False)
            post.post_latitude = latitude
            post.post_longitude = longitude
            post.post_region = region
            post.author = request.user  # set author as the current user
            post.save()
            return redirect('post:post')
    else:
        form = PostForm()
    return render(request, 'post/service-details.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'post/post_detail.html', {'post': post})


def faq(request):
    return render(request, 'post/faq.html')

@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
        return JsonResponse({'success': True})
