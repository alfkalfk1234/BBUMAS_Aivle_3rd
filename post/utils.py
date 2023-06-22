from .models import Post

def create_post(title, content):
    post = Post(post_title=title, post_content=content)
    post.save()
    return post
