from datetime import datetime
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Post
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'