from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, ListView
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


# Create your views here.
def index(reqeust):
    return render(reqeust, "blog/index.html")


def post_list(reqeust, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:

        posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = reqeust.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
    }
    return render(reqeust, "blog/list.html", context)


def posts_details(reqeust, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'time': datetime.datetime.now(),
        'comments': comments
    }
    return render(reqeust, "blog/detail.html", context)


@login_required
def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, "forms/comment.html", context)


def post_search(request):
    query = None
    result = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result1 = Post.published.annotate(similarity=TrigramSimilarity('title', query)). \
                filter(similarity__gt=0.1)

            result2 = Post.published.annotate(similarity=TrigramSimilarity('description', query)). \
                filter(similarity__gt=0.1)
            result3 = Image.objects.annotate(similarity=TrigramSimilarity('description', query)). \
                filter(similarity__gt=0.1)

            result4 = Image.objects.annotate(similarity=TrigramSimilarity('title', query)). \
                filter(similarity__gt=0.1)

            result = (result1 | result2).order_by('-similarity')
            result_img = (result3 | result4).order_by('-similarity')

            context = {
                'query': query,
                'result': result,
                'result_img': result_img
            }

    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    post_pag = Post.published.all()
    user = request.user
    posts = Post.published.filter(author=user)
    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page', 3)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    print(post_pag)
    context = {
        'posts': posts,
        'post_pag': post_pag
    }

    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create-post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile")
    return render(request, 'forms/delete-post.html', {'post': post})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create-post.html', {'form': form, 'post': post})


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        form = UserRigesterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(
                user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRigesterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
            return redirect('blog:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {
        'account_form': account_form,
        'user_form': user_form
    }
    return render(request, 'registration/edit_account.html', context)

def user(request):
    print(request.user.id)
    user = Account.objects.filter(user_id=request.user.id)
    post = Image.objects.filter(post__author_id=request.user.id)
    context = {
        'user': user,
        'post': post
    }

    return render(request, 'blog/user.html', context)


def post_comment_user(request, post_id):
    post = Comment.objects.filter(post_id=post_id, active=True)
    print(post)
    return render(request, 'blog/post-comment.html', {'post': post})


