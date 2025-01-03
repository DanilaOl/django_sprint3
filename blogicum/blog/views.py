from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=timezone.now())
    ).order_by('-pub_date').select_related(
        'category',
        'location',
        'author'
    ).all()[0:5]

    context = {'post_list': post_list}

    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'

    post = get_object_or_404(Post, pk=post_id)

    if (not post.is_published
            or not post.category.is_published
            or post.pub_date > timezone.now()):
        raise Http404()

    context = {'post': post}

    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug)

    if not category.is_published:
        raise Http404()

    post_list = Post.objects.filter(
        Q(category=category)
        & Q(is_published=True)
        & Q(pub_date__lte=timezone.now())
    ).all()

    context = {'category': category, 'post_list': post_list}

    return render(request, template, context)
