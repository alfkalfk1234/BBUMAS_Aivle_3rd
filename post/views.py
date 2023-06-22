from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Photo
from .forms import PostForm
from .utils import create_post
def index(request):
    return render(request, 'post/post.html')

# def posting(request):
#     return render(request, 'post/service-details.html')

def posting(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
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


