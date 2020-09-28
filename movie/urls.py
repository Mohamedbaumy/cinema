from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('movie_detail/<slug_movie>/',views.movie_detail,name='movie_detail'),
    path('episode_detail/<slug_episode>/',views.movie_detail,name='episode_detail'),
    path('category/movie/<slug_movie>/',views.category_list,name='category_movie_list'),
    path('category/series/<slug_series>/',views.category_list,name='category_series_list'),
    path('series_detail/<slug>/',views.series_detail,name='series_detail'),
    path('search/',views.search,name='search'),
]