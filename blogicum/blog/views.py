from django.http import Http404
from django.shortcuts import render


def index(request):
    template = 'blog/index.html'
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    requested_post = None

    for post in posts:
        if post['id'] == post_id:
            requested_post = post

    if requested_post is None:
        raise Http404

    template = 'blog/detail.html'
    context = {'post': requested_post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    context = {'category': category_slug}
    return render(request, template, context)
