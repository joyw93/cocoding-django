from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag
from django.views.generic import CreateView, UpdateView, ListView, DetailView


def index(request):
    return render(
        request,
        'cocoding/main.html'
    )


class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        return context