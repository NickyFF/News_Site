from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .models import Post
from .filters import PostFilter
from .forms import PostForm
# from .forms import PostForm
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'

class PostSearch(ListView):
        model = Post
        ordering = 'time_in'
        template_name = 'post_search.html'
        context_object_name = 'search'
        paginate_by = 2

        def get_queryset(self):
            queryset = super().get_queryset()
            self.filterset = PostFilter(self.request.GET, queryset=queryset)
            return self.filterset.qs

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['filterset'] = self.filterset
            return context

class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.news = True
        return super().form_valid(form)

class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        articles = form.save(commit=False)
        articles.news = False
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')