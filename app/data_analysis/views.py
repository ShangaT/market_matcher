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
    categories = get_cashed_data()['category_general'].cat.categories.tolist()
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
    category = 'Бакалея и соусы'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_2(request):
    category = 'Выпечка и хлеб'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_3(request):
    category = 'Молочные продукты'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_4(request):
    category = 'Мясные продукты'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_5(request):
    category = 'Напитки'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_6(request):
    category = 'Овощи, фрукты, закуски'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_7(request):
    category = 'Прочее'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_8(request):
    category = 'Рыба и морепродукты'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_9(request):
    category = 'Сладости'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_10(request):
    category = 'Чай, кофе, какао, сахар'
    df = get_cashed_data()
    df = DataFrame(df[df['category_general'] == category])[['name', 'price_magnit', 'price_perekrestok']]
    df.rename(columns={ 
            'name': 'Наименование',
            'price_magnit': 'Цена в магните',
            'price_perekrestok': 'Цена в пятерочке'
         },  inplace=True)
    content = {    
        "category": category,
        "html_table": df.to_html(classes='table table-bordered table-striped', index=False)
        }
    return render(request, "data_analysis/products_table.html", content)

def page_11(request):
    products = Product.objects.all()
    paginator = Paginator(products, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "data_analysis/products_list.html", {"page_obj": page_obj})
    # return HttpResponse("Чай, кофе, какао, сахар")

