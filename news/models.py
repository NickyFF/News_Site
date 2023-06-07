from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.core.cache import cache

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rate_user = models.FloatField(default = 0.0)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):

        rate_post_author = Post.objects.filter(author_id=self.pk).aggregate(rate_news=Sum('rate_news'))['rate_news'] * 3
        rate_comm_author = Comment.objects.filter(user_id=self.user).aggregate(rate_comment=Sum('rate_comment'))['rate_comment']
        rate_comm_to_author = Comment.objects.filter(post__author__user=self.user).aggregate(rate_comment=Sum('rate_comment'))['rate_comment']

        self.rate_user = rate_post_author + rate_comm_author + rate_comm_to_author
        self.save()

class Category(models.Model):
    culture = 'CULTURE'
    science = 'SCIENCE'
    tech = 'TECH'
    politics = 'POLITICS'
    sport = 'SPORT'
    entertainment = 'ENTERTAINMENT'
    economics = 'ECONOMICS'
    education = 'EDUCATIONS'

    CATEGORIES = [
        (culture, 'Культура'),
        (science, 'Наука'),
        (tech, 'Технология'),
        (politics, 'Политика'),
        (sport, 'Спорт'),
        (entertainment, 'Развлечения'),
        (economics, 'Экономика'),
        (education, 'Образование')
    ]
    tematic = models.CharField(max_length=100, unique = True, choices=CATEGORIES)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.tematic

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    news = models.BooleanField(default = True)
    time_in = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through ='PostCategory')
    title = models.CharField(max_length = 100)
    text_author = models.TextField(default = "Введите текст")
    rate_news = models.FloatField(default = 0.0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} : {self.text_author}'
    
    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rate_news += 1
        self.save()

    def dislike(self):
        self.rate_news -= 1
        self.save()
    
    def preview(self):
        return f'{self.text_author[0:124]}...'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.TextField(default = "Введите текст")
    time_in = models.DateTimeField(auto_now_add = True)
    rate_comment = models.FloatField(default = 0.0)

    def like(self):
        self.rate_comment += 1
        self.save()

    def dislike(self):
        self.rate_comment -= 1
        self.save()

class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user