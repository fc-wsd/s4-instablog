from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Category
from .models import Post


def create_post(request):
    category = get_object_or_404(Category, pk=request.POST.get('category'))

    # 이곳에 글을 저장하는 코드를 작성하세요.
    post = None

    # 저장한 글(post)의 pk를(post.pk) 이곳에 할당하세요.
    post_pk = None
    return redirect(reverse('blogtest:view_post', kwargs={'pk': post_pk}))


def view_post(request, pk):
    # 글을 가져와서 post 에 담으세요.
    post = None

    return render(request, 'view_post.html', {
        'post': post,
    })


def list_posts(request):
    # 글 전체를 가져와서 posts 에 담으세요.
    posts = None

    return render(request, 'list_posts.html', {
        'posts': posts,
    })
