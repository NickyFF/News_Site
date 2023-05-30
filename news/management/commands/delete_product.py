from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category, PostCategory
 
 
class Command(BaseCommand):
    help = 'Удаление новостей из каталога' # показывает подсказку при вводе "python manage.py <ваша команда> --help"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
    
    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(f'Do you really want to delete {options["category"]} posts? yes/no') # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer =  input() # считываем подтверждение 
        
        if answer == 'yes': # в случае подтверждения действительно удаляем все товары
            category = Category.objects.get(tematic=options["categoty"])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully wiped posts from category {category.tematic}!'))
            return
 
        self.stdout.write(self.style.ERROR('Access denied')) # в случае неправильного подтверждения, говорим, что в доступе отказано