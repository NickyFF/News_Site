from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import Post, Category, Author
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
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

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class ProtectedView(LoginRequiredMixin, TemplateView):
    update_name = 'news_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.change_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    html_content = render_to_string(
        'send_email.html',
        {
            'category': category.tematic,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{user} {category.tematic}',
        body=category.tematic,
        from_email='nikitakryz2000@yandex.ru',
        to=['nikirakryzx@gmail.com'],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

    message = 'Вы подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})