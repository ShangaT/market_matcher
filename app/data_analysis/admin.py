from django.contrib import admin

# Импорт модуля admin из библиотеки Django.contrib
from django.contrib import admin
# Импорт модели MyModel из текущего каталога (".")
from .models import Product
# Регистрация модели MyModel для административного сайта
admin.site.register(Product)
#admin.site.register(Store)

