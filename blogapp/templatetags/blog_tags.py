from django import template
from ..models import Post, Comment, User
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe
from ..views import *
import random
register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context


#
# @register.inclusion_tag("partials/popular_post.html")
# def most_popular_posts(count=5):
#      # return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]
#     post1 = Post.published.filter(max(coount))
# #     coount = Post.published.filter(comments__created__gte=1)
# #     post2 = Comment.objects.filter(post__publish__gte=coount)
# #     # post = (post2).order_by()[:count]
#     context = {
#         'post1': post1
#     }
#     return context
# @register.inclusion_tag("partials/popular_post.html")
# def most_popular_posts():
#     post = Post.published.annotate(count=post_comment.comment)
#     return post


@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))


@register.inclusion_tag("partials/longest_post.html")
def longest_reading_time(count=3):
    long_post = Post.published.filter(reading_time__gt=1).order_by("-reading_time")[:count]
    context = {
        'long_post': long_post
    }
    return context


@register.inclusion_tag("partials/shortest_post.html")
def shortest_reading_time(count=3):
    short_post = Post.published.filter(reading_time__lt=30).order_by("reading_time")[:count]
    context = {
        'short_post': short_post
    }
    return context


@register.inclusion_tag("partials/popular_user.html")
def popular_user(count=5):
    user = User.objects.annotate(post_count=Count('user_posts')).order_by('-post_count')[:count]

    context = {
        'user': user
    }
    return context


@register.filter(name="cansor")
def to_cansor(text):
    r = str(text).lower()
    result1 = r.split()
    search = ['shit', 'fuck']
    for i in range(len(result1)):
        for j in search:
            if j in result1[i]:
                result1[i] = '!!!'
    return " ".join(result1)

@register.inclusion_tag('partials/rand-post.html')
def random_post():
    post = Post.published.all()
    rand = random.choice(post)

    context = {
        'rand': rand
    }
    print(rand)
    return context





