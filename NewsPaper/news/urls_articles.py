from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, ArticleCreate, ArticleUpdate, PostDelete


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   #path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   #path('create/', NewsCreate.as_view(), name='create_news'),
   path('create/', ArticleCreate.as_view(), name='create_article'),
   path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]