from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from classifier_training.market_analysis import classification
from classifier_training.market_analysis import Diagram

def index(request):
    products = Product.objects.all()
    categories = classification(products)['general_category'].cat.categories.tolist()
    contant = {"categories": categories}
    return render(request, 'data_analysis/index.html', contant)

def visualization(request):
    products = Product.objects.all()
    df = classification(products)
    Diagram.top_10_max(df)
    Diagram.top_10_min(df)
    Diagram.pivot_table_mean(df)
    Diagram.pivot_table_mod(df)
    return render(request, 'data_analysis/graphics.html')

def page_1(request):
    return HttpResponse("Бакалея и соусы")

def page_2(request):
    return HttpResponse("Выпечка и хлеб")

def page_3(request):
    return HttpResponse("Консервы, мед, варенье")

def page_4(request):
    return HttpResponse("Молочные продукты")

def page_5(request):
    return HttpResponse("Мясные продукты")

def page_6(request):
    return HttpResponse("Напитки")

def page_7(request):
    return HttpResponse("Овощи, фрукты, закуски")

def page_8(request):
    return HttpResponse("Прочее")

def page_9(request):
    return HttpResponse("Рыба и морепродукты")

def page_10(request):
    return HttpResponse("Сладости")

def page_11(request):
    return HttpResponse("Чай, кофе, какао, сахар")

