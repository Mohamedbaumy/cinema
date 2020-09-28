from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug_movie = models.SlugField(max_length=250,blank=True)
    slug_series = models.SlugField(max_length=250,blank=True)

    def get_absolute_url(self):
        return reverse('category_list',args={self.slug_movie,self.slug_series})
    
    def save(self,*args,**kwargs):
        if not slug_movie or not slug_series :
            self.slug_movie = slugify(self.name)
            self.slug_series = slugify(self.name)
        super(Category,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.name



class Series(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    banner = models.URLField(blank=True,null=True)
    trailer = models.URLField(blank=True,null=True)
    year = models.PositiveIntegerField(default=2000)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    age = models.PositiveIntegerField(default=3)
    country = models.CharField(max_length=200,default="USA")
    rate = models.DecimalField(max_digits=3,decimal_places=2,default=7.4)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('series_detail',args={self.slug})

    def save(self,*args,**kwargs):
        if "youtube" in str(self.trailer) and "embed" not in str(self.trailer):
            url = self.trailer.split("watch?v=")
            self.trailer = url[0] + "embed/" + url[1]
        super(Series,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class Season(models.Model):
    series = models.ForeignKey(Series,related_name='series_season',
                               on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250,blank=True)
    season_num = models.IntegerField(default=1)
    banner = models.URLField(blank=True,null=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(str(self.series)+ str(self.season_num))
        super(Season,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.season_num)


class Episode(models.Model):
    # ForeignKey
    season = models.ForeignKey(Season,related_name='season',
                                on_delete=models.CASCADE,blank=True,null=True)
    series = models.ForeignKey(Series,related_name='series_movie',
                               on_delete=models.CASCADE,blank=True,null=True)
    slug = models.SlugField(max_length=250,blank=True)
    episode_num = models.IntegerField(default=1)
    banner = models.URLField(blank=True,null=True,default='')
    episode_trailer = models.URLField(blank=True,null=True)
    air_date = models.DateField(default='2020-08-07')
    runing_time = models.PositiveIntegerField(default=120)
    rate = models.DecimalField(max_digits=3,decimal_places=2,default=7.4)
    # Links 
    quality = models.CharField(max_length=15,default="HD")
    link = models.URLField(null=True,blank=True)
    

    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('episode_detail',args={self.slug})

    def save(self,*args,**kwargs):
        if not self.slug:
            if self.season:
                self.slug = slugify(str(self.series)+ str(self.season.season_num) + str(self.episode_num))
            else:
                self.slug = slugify(str(self.series)+ str(self.episode_num) + str(self.episode_num))
        
        super(Episode,self).save(*args,**kwargs)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return str(self.series)

class Movie(models.Model):
    
    # Movie information
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,blank=True,null=True)
    description = models.TextField()
    year = models.PositiveIntegerField(default=2000)
    banner = models.URLField(blank=True,null=True,default='')
    age = models.PositiveIntegerField(default=3)
    movie_trailer = models.URLField(blank=True,null=True)
    runing_time = models.PositiveIntegerField(default=120)
    country = models.CharField(max_length=200,default="USA")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3,decimal_places=2,default=7.4)
    # Links 
    quality = models.CharField(max_length=15,default="HD")
    link = models.URLField(null=True,blank=True)

    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('created',)

    def save(self,*args,**kwargs):
        if "youtube" in str(self.movie_trailer) and "embed" not in str(self.movie_trailer) :
            url = self.movie_trailer.split("watch?v=")
            self.movie_trailer = url[0] + "embed/" + url[1]
        if "youtube" in str(self.link) and "embed" not in str(self.link):
            url = self.link.split("watch?v=")
            self.link = url[0] + "embed/" + url[1]
        super(Movie,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('movie_detail',args={self.slug})

    def __str__(self):
        return self.title


LINK_CHOICES = (
    ('D','DOWNLOAD LINK'),
    ('W','WATCH LINK')
)


class MovieImages(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie_photo',on_delete=models.CASCADE)
    image = models.URLField()

    def __str__(self):
        return str(self.image)

class SeriesImages(models.Model):
    series = models.ForeignKey(Series,related_name='series_photo',on_delete=models.CASCADE)
    image = models.URLField()

    def __str__(self):
        return str(self.image)

