from django.urls import path
from . import views

app_name = 'cocoding'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('newstudy/', views.post_create, name='post_create'),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment, name="new_comment"),
    path('post_delete/<int:pk>/', views.post_delete, name="post_delete"),
    path('comment_delete/<int:pk>/', views.comment_delete, name="comment_delete"),
    path('post_update/<int:pk>/', views.PostUpdate.as_view()),
    path('comment_update/<int:pk>/', views.CommentUpdate.as_view(), name="comment_update"),
    path('search/<str:q>/', views.PostSearch.as_view(), name='post_search'),
    path('set_recruit/<int:pk>/', views.set_recruit, name="set_recruit"),

    # path('post/<slug:slug>/', views.detail_view, name='detail'),
    # path('tag/<slug:slug>/', views.tagged, name='taged'),
    #path('newstudy/', views.PostCreate.as_view(), name='post_create'),
]