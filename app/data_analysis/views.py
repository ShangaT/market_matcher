from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from classifier_training.market_analysis import classification, Diagram, get_products_queryset

from django.core.paginator import Paginator
from django.shortcuts import render

def index(request):
    products = get_products_queryset()
    categories = classification(products)['general_category'].cat.categories.tolist()
    contant = {"categories": categories}
    return render(request, 'data_analysis/index.html', contant)

def visualization(request):
    products = get_products_queryset()
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
    return HttpResponse("Молочные продукты")

def page_4(request):
    return HttpResponse("Мясные продукты")

def page_5(request):
    return HttpResponse("Напитки")

def page_6(request):
    return HttpResponse("Овощи, фрукты, закуски")

def page_7(request):
    return HttpResponse("Прочее")

def page_8(request):
    return HttpResponse("Рыба и морепродукты")

def page_9(request):
    return HttpResponse("Сладости")

def page_10(request):
    return HttpResponse("Чай, кофе, какао, сахар")
def page_11(request):
    products = Product.objects.all()
    paginator = Paginator(products, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "data_analysis/products_list.html", {"page_obj": page_obj})
    # return HttpResponse("Чай, кофе, какао, сахар")

