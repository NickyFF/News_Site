# from django.db import models
# from datetime import datetime

# # Create your models here.

# class Staff(models.Model):
#     director = 'DI'
#     admin = 'AD'
#     cook = 'CO'
#     cashier = 'CA'
#     cleaner = 'CL'
   
#     POSITIONS = [
#     (director, 'Директор'),
#     (admin, 'Администратор'),
#     (cook, 'Повар'),
#     (cashier, 'Кассир'),
#     (cleaner, 'Уборщик')
# ]
#     full_name = models.CharField(max_length = 50)
#     position = models.CharField(max_length = 2, choices = POSITIONS, default = cashier)
#     labor_contract = models.IntegerField()
    
#     def get_last_name(self):
#         return self.fullname.split()[0]
         
# class Product(models.Model):
#     name = models.CharField(max_length = 255)
#     price = models.FloatField(default = 0.0)

# class Order(models.Model):
#     time_in = models.DateTimeField(auto_now_add = True)
#     time_out = models.DateTimeField(null = True)
#     cost = models.FloatField(default = 0.0)
#     pickup = models.BooleanField(default = False)
#     complete = models.BooleanField(default = False)
#     staff = models.ForeignKey(Staff, on_delete = models.CASCADE)
#     products = models.ManyToManyField(Product, through = 'ProductOrder')

#     def finish_order(self):
#         self.time_out = datetime.now()
#         self.complete = True
#         self.save()
    
#     def get_duration(self):
#         if self.complete:
#             return ((self.time_out - self.time_in).total_seconds()) // 60
#         else:
#             return ((datetime.now() - self.time_in).total_seconds()) // 60


# class ProductOrder(models.Model):
#     _amount = models.IntegerField(default = 1, db_column = 'amount')
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)

#     def product_sum(self):
#         product_price = self.product.price
#         return product_price * self.amount
    
#     @property
#     def amount(self):
#         return self._amount
    
#     @amount.setter
#     def amount(self, value):
#         self._amount = int(value) if value >= 0 else 0
#         self.save()

# # Author.objects.filter(-age__gt = 25)




