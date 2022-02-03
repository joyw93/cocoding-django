from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.core.exceptions import PermissionDenied
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, ListView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.http import JsonResponse
from django.db.models import Q


class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['paginator'] = Paginator(Post.objects.all().order_by('-pk'), 8)
        return context


@login_required(login_url='/account/signin/')
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            current_user = request.user
            form.instance.author = current_user
            newpost = form.save(commit=False)
            newpost.slug = slugify(newpost.title)
            newpost.save()
            form.save_m2m()
            return redirect('cocoding:post_list')
    else:
        form = PostForm()
    context = {'form': form}    
    return render(request, 'cocoding/post_form.html', context)


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        return context


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated and request.user == post.author:
        post.delete()
        return redirect('cocoding:post_list')
    else:
        raise PermissionDenied


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method=='POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
        
    else:
        raise PermissionDenied


def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'cocoding/post_update_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'cocoding/comment_update_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



class PostSearch(PostList):
    paginate_by = 8
    
    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct().order_by('-pk')
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        context['paginator'] = Paginator(self.get_queryset(), 8)
        
        return context
    
    

def set_recruit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated and request.user == post.author:
        post.recruiting = not post.recruiting
        post.save()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied