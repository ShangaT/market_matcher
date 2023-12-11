from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from classifier_training.market_analysis import Diagram, join_by_names
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render

from pandas import DataFrame

def get_cashed_data():
    try:
        data = cache.get('processed_products')
        if DataFrame(data).empty:
            raise TypeError("Cashed data is empty") 
        print("data cached (index)")
    except TypeError:
        print("data not cached (index)")
        data = join_by_names()
        cache.set('processed_products', data)
    return DataFrame(data)

def index(request):
    categories = get_cashed_data()['general_category'].cat.categories.tolist()
    content = {"categories": categories}
    return render(request, 'data_analysis/index.html', content)

def visualization(request):
    df = get_cashed_data()
    Diagram.top_10_max(df)
    Diagram.top_10_min(df)
    Diagram.pivot_table_mean(df)
    Diagram.pivot_table_mod(df)
    return render(request, 'data_analysis/graphics.html')

def page_1(request):
    df = get_cashed_data()
    df = DataFrame(df['general_category'] == 'Бакалея и соусы')
    content = {
        "product_data": df,
        "category": "Бакалея и соусы",
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False),
        "shapeX": df.shape[0],
        "shapeY": df.shape[1],
        "columns": df.columns,
        }
    return render(request, "data_analysis/products_table.html", content)

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

