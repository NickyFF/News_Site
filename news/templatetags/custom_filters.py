from django import template

register = template.Library()

EXCEPTION_SYMBOLS = [
   'редиска', 'баклажан', 'кабачок'
]

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   for word in EXCEPTION_SYMBOLS:
      if word in value:
         censor_word = word[0] + (len(word) - 2) * '*' + (len(word) - 1)
         value = value.replace(word, censor_word)
   # Возвращаемое функцией значение подставится в шаблон.
   return value