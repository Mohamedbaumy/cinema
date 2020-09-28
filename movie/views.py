from django.shortcuts import render,get_object_or_404
from .models import Movie,Episode,Category,Series,SeriesImages
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q

# Create your views here.

def home(request):
    movies = Movie.objects.all()[0:12]
    last_movies = Movie.objects.all()[0:6]
    Episodes =Episode.objects.all()
    context = {
        'movies':movies,
        'Episodes':Episodes,
        'last_movies':last_movies
    }
    return render(request,'movie/home.html',context)


def category_list(request,slug_movie=None,slug_series=None):
    if slug_movie:
        category = Category.objects.get(slug_movie=slug_movie)
        item_list = Movie.objects.filter(category=category)
    if slug_series:
        category = Category.objects.get(slug_series=slug_series)
        item_list = Series.objects.filter(category=category)
    paginator = Paginator(item_list,24)
    page = request.GET.get('page')
    try:
        item_list = paginator.page(page)
    except PageNotAnInteger:
        item_list = paginator.page(1)
    except EmptyPage:
        item_list = paginator.page(paginator.num_pages)
    context = {
        'category':category,
        'item_list':item_list,
        'page':page
        }

    return render(request,'movie/category.html',context)

def movie_detail(request,slug_movie=None,slug_episode=None):
    if slug_movie:
        movie = get_object_or_404(Movie,slug=slug_movie)
        images = movie.movie_photo.all()
    if slug_episode:
        movie = get_object_or_404(Episode,slug=slug_episode)
        images = None
    
    context = {
        'movie':movie,
        'images':images
    }
    return render(request,'movie/movie_detial.html',context)

def series_detail(request,slug):
    series = get_object_or_404(Series,slug=slug)
    context = {'series':series}
    return render(request,'movie/series_detail.html',context)

def search(request):
    query = request.GET.get('q')
    item_list = Movie.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
    series_list = Series.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
    context = {
        'item_list':item_list,
        'query':query,
        'series_list':series_list
    }
    return render(request,'movie/category.html',context)