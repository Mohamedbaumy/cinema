from django.contrib import admin
from .models import Movie,MovieImages,Series,Season,Episode,Category,SeriesImages

# Register your models here.


class MovieImageInline(admin.TabularInline):
    model = MovieImages
    raw_id_fields = ['movie']
    extra = 0

class SeriesImageInline(admin.TabularInline):
    model = SeriesImages
    raw_id_fields = ['series']
    extra = 0

class EpisodeInline(admin.StackedInline):
    model = Episode
    fields = ['season','episode_num','banner','episode_trailer','air_date','runing_time','link']
    raw_id_fields = ['series']
    extra = 0


class SeasonInline(admin.TabularInline):
    model = Season
    fields = ['season_num','banner']
    raw_id_fields = ['series']
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MovieImageInline]
    search_fields = ['title']

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']
    inlines = [SeriesImageInline,SeasonInline,EpisodeInline]
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_movie': ('name',),'slug_series': ('name',)}
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    fields = ['series','season_num','banner']
    list_display = ['series']
    inlines = [EpisodeInline]
    list_filter = ['series']
    search_fields = ['series']

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    fields = ['series','season','banner','episode_num','episode_trailer','air_date','runing_time','rate','quality','link']
    list_display = ['series','season']
    list_filter = ['series']
    search_fields = ['series']





