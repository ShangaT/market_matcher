from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from classifier_training.market_analysis import Classifier, Diagram, join_by_names
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
    return DataFrame(data), data['region_rus'].unique()

def visualization(region):
        classifer = Classifier()
        df = classifer.classification_by_category()        
        df_graphics = df[df['region_rus'] == region]
        Diagram.top_10_max(df_graphics)
        Diagram.top_10_min(df_graphics)    
        Diagram.pivot_table_mean(df_graphics)
        Diagram.pivot_table_mod(df_graphics)

class Index:

    def index(request):
        categories, cities = get_cashed_data()
        content = {"cities": cities}
        print(cities)
        return render(request, 'data_analysis/index.html', content)
    
    def city(request, city_destination):
        categories, cities = get_cashed_data()
        categories = categories['category_general'].cat.categories.tolist()
        content = {
            "categories": categories,
            "cities": cities,
            "category": 'home',
            "city": city_destination}
        visualization(city_destination)
        return render(request, 'data_analysis/index_regions.html', content)
    
    def category(request, city_destination, category_destination):
        data, cities = get_cashed_data()
        categories = data['category_general'].cat.categories.tolist()
        print(categories)
        data = DataFrame(data[data['category_general'] == category_destination])
        data = DataFrame(data[data['region_rus'] == city_destination])
        print(data.columns)
        data = data[['name', 'price_magnit', 'price_perekrestok']]
        # data = data[['name', 'price_magnit', 'price_perekrestok', 'price_auchan']]
        
        data.rename(columns={ 
                'name': 'Наименование',
                'price_magnit': 'Цена в магните',
                'price_perekrestok': 'Цена в пятерочке',
                # 'price_auchan': 'Цена в ашане'
            },  inplace=True)
        content = {   
            "city": city_destination,
            "categories": categories, 
            "cities": cities,
            "category": category_destination,
            "html_table": data.to_html(classes='table table-hover table-striped table-bordered', index=False).replace('<td>', '<td align="right">'),
            }
        return render(request, "data_analysis/products_table.html", content)