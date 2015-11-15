from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Post


def list_posts(request):
    try:
        page = int(request.GET['page'])
        if page < 1:
            page = 1
    except Exception:
        page = 1
    per_page = 5

    posts = Post.objects.order_by('-created_at')[page-1:page*per_page]

    return render(request, 'list.html', {
        'posts': posts,
    })


def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'view.html', {
        'post': post,
    })
