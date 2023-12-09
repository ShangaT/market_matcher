import sqlite3, string, joblib
from data_analysis.models import Product
#from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from django_pandas.io import read_frame

def preprocess_text(input_string):
    clear_string = input_string.translate(str.maketrans('', '', string.punctuation + string.digits))
    clear_string = clear_string.lower()
    return clear_string

def classification(database):

    products = read_frame(database)

    products.drop_duplicates(inplace=True)
    products.dropna(inplace=True)

    with open('classifier_training/model.pkl', 'rb') as f:
        model = joblib.load(f)

    print(products.columns)

    products['clear_category'] = products['category'].apply(preprocess_text)
    prediction = model.predict(products['clear_category'])
    products['general_category'] = prediction    

    products.category = products.category.astype('category')
    products.category_code = products.category_code.astype('category')
    products.general_category = products.general_category.astype('category')

    conditions = [(products['store__id'] == 1),
                  (products['store__id'] == 2), (products['store__id'] == 3)]
    values = ['Ашан', 'Магнит', 'Перекресток']
    products['shop_rus'] = np.select(conditions, values)

    return products

class Diagram():

    def top_10_max(df):
        top_10 = df.sort_values(by='price', ascending=False).head(10)
        sns.set_style('darkgrid')
        plt.figure(figsize=(7,5))
        sns.barplot(x = 'price', y = 'name', data = top_10, palette='rocket')
        plt.title('10 САМЫХ ДОРОГИХ ПРОДУКТОВ', fontsize=22)
        plt.xlabel('Стоимость', fontsize=16)
        plt.ylabel('Наименование', fontsize=16)
        plt.tick_params(axis='x', labelsize=10)
        plt.tick_params(axis='y', labelsize=10)
        chart_path = 'data_analysis/static/data_analysis/img/top_10.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

    def top_10_min(df):
        top_10 = df.sort_values(by='price', ascending=True).head(10)
        sns.set_style('darkgrid')
        plt.figure(figsize=(7,5))
        sns.barplot(x = 'price', y = 'name', data = top_10, palette='rocket')
        plt.title('10 САМЫХ ДЕШЕВЫХ ПРОДУКТОВ', fontsize=22)
        plt.xlabel('Стоимость', fontsize=16)
        plt.ylabel('Наименование', fontsize=16)
        plt.tick_params(axis='x', labelsize=10)
        plt.tick_params(axis='y', labelsize=10)
        chart_path = 'data_analysis/static/data_analysis/img/top_10_min.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

    def pivot_table_mean(df):
        plt.figure(figsize=(10,5))
        pivot_table = df.pivot_table(index='general_category', columns='shop_rus', values='price', aggfunc='mean')
        plt.title('ТЕПЛОВАЯ КАРТА СРЕДНЕЙ СТОИМОСТИ ТОВАРОВ', fontsize=20)
        sns.heatmap(pivot_table, cmap='rocket', annot=True, fmt=".1f")
        plt.xlabel('Магазин', fontsize=16)
        plt.ylabel('Категория', fontsize=16)
        plt.tick_params(axis='x', labelsize=12)
        plt.tick_params(axis='y', labelsize=12)
        chart_path = 'data_analysis/static/data_analysis/img/pivot_table_mean.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

    def pivot_table_mod(df):
        plt.figure(figsize=(10,5))
        pivot_table = df.pivot_table(index='general_category', columns='shop_rus', values='price', aggfunc=lambda x: x.mode().max())
        plt.title('ТЕПЛОВАЯ КАРТА МОДЫ СТОИМОСТИ ТОВАРОВ', fontsize=20)
        sns.heatmap(pivot_table, cmap='rocket', annot=True, fmt=".1f")
        plt.xlabel('Магазин', fontsize=16)
        plt.ylabel('Категория', fontsize=16)
        plt.tick_params(axis='x', labelsize=12)
        plt.tick_params(axis='y', labelsize=12)
        chart_path = 'data_analysis/static/data_analysis/img/pivot_table_mod.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

def get_products_queryset():
    return Product.objects.values('id', 'store__id', 'product_id',
                           'name', 'code', 'category', 'category_code', 'price')

if __name__ == '__main__':

    products_qs = get_products_queryset()

    df = classification(products_qs)
    top_max = Diagram.top_10_max(df)
    top_min = Diagram.top_10_min(df)
    mean = Diagram.pivot_table_mean(df)
    mod = Diagram.pivot_table_mod(df)
    plt.show()