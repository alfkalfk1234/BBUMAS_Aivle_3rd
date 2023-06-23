from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Photo
from .forms import PostForm
from .utils import create_post
def index(request):
    posts = Post.objects.all()  # get all posts
    return render(request, 'post/post.html', {'posts': posts})

# def posting(request):
#     return render(request, 'post/service-details.html')

def posting(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            post = form.save(commit=False)
            post.post_latitude = latitude
            post.post_longitude = longitude
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


