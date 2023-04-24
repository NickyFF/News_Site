from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Author, Category
from django_filters import DateFilter
from .forms import *

class PostFilter(FilterSet):
   author = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Author', empty_label='любой')
   date = DateFilter(field_name='time_in', widget=forms.DateInput(attrs={'type': 'date'}), label='Поиск по дате',
                      lookup_expr='date__gte')

   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'title': ['icontains'],
           'author' : ['exact'],
       }

