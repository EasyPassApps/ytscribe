from django.urls import path
from . import views
from .views import HomeView, ArticleDetailView, AddPostView, Test

urlpatterns = [
    #path('',views.home,name="home"),
    path('',HomeView.as_view(),name="home"),
    path('article/<int:pk>/<yt>',ArticleDetailView.as_view(),name="article-detail"),
    path('add_post/',AddPostView.as_view(),name="add_post"),
    path('test/',views.test,name="test"),
    #path('new_post/',views.new_post,name="new_post"),
]

