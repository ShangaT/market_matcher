import sqlite3, string, joblib
from data_analysis.models import Product
#from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from django_pandas.io import read_frame
from pandas import DataFrame

import nltk, re
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

from sklearn.feature_extraction.text import CountVectorizer
nltk.download('punkt')
nltk.download('wordnet')
#nltk.download('russian')

class Classifier:

    def transform_text(self, df_column):
        with open('classifier_training/category_dict.txt', 'r', encoding='utf8') as dictionary:
            words_for_vec = dictionary.read().split()

        new_text = []
        lemmatize = nltk.WordNetLemmatizer()
        for i in df_column:
            text = re.sub(r"\b\d+(г|шт)\b", "", i)
            text = re.sub("[^a-zA-Z]"," ",i) #удаляем неалфавитные символы
            text = nltk.word_tokenize(text) #токенизация
            text = [lemmatize.lemmatize(word) for word in i] #лемматизация
            text = "".join(text)
            new_text.append(text)

        count = CountVectorizer(vocabulary = words_for_vec) 
        matrix = count.fit_transform(new_text).toarray()
        #matrix = count.fit_transform(new_text).toarray() #векторизация
        return matrix
    
    def classification_by_category(self):
        products = read_frame(get_products_queryset())
        #очистка данных
        # products.drop_duplicates(inplace=True)
        # products.dropna(inplace=True)

        with open('classifier_training/model_category.pkl', 'rb') as f:
            model = joblib.load(f)
        #приведение входных данных в формат, понятный модели
        vectors_store_categories = self.transform_text(products['category'])
        prediction = model.predict(vectors_store_categories)
        products['category_general'] = prediction

        products.category = products.category.astype('category')
        products.category_code = products.category_code.astype('category')
        products.category_general = products.category_general.astype('category')

        conditions_store = [(products['store__id'] == 1),
                            (products['store__id'] == 2), 
                            (products['store__id'] == 3)]
        values_store = ['Ашан', 'Магнит', 'Перекресток']
        products['shop_rus'] = np.select(conditions_store, values_store)

        conditions_region = [(products['region__id'] == 59),
                            (products['region__id'] == 77), 
                            (products['region__id'] == 78)]
        values_region = ['Пермь', 'Москва', 'Санкт-Петербург']
        products['region_rus'] = np.select(conditions_region, values_region)

        return products

def preprocess_text(input_string):
    clear_string = input_string.translate(str.maketrans('', '', string.punctuation + string.digits))
    clear_string = clear_string.lower()
    return clear_string

def remove_words_with_g(string):
    pattern = r"\b\d+(г|шт)\b"
    modified_string = re.sub(pattern, "", string)
    return modified_string.strip()

def preprocess_text_long(text):
    nltk.download('stopwords')
    mystem = Mystem() 
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend(['лента','ассорт','разм','арт','что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', 'г', 'шт', 'магнит', 'перекрёсток'])
    text = str(text)
    text = remove_words_with_g(text)
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and len(token)>=3 \
              and token.strip() not in punctuation \
              and token.isdigit()==False]
    text = " ".join(sorted(tokens))
    return text

def join_by_names():
    calssifer = Classifier()
    products = calssifer.classification_by_category()
    
    # Очистка имен
    products['name_clear']=products['name'].apply(preprocess_text)

    processed_products = DataFrame()
    #дублируем наименования регионов
    processed_products['region_rus'] = products['region_rus']
    #processed_products['price'] = products['price']

    # Дублируются имена и очищенные имена для дальнейшей работы
    processed_products['name'] = products['name']
    processed_products['name_clear'] = products['name_clear']
    # Добавляются категории в итоговый датафрейм
    processed_products['category'] = products[products['name_clear'] == processed_products['name_clear']]['category']
    processed_products['category_general'] = products[products['name_clear'] == processed_products['name_clear']]['category_general']
    # Делаются отдельные выборки для дальнейшего распределения цен по полям
    products_perekrestok = products[products['shop_rus'] == 'Перекресток'].copy()
    products_magnit = products[products['shop_rus'] == 'Магнит'].copy()
    products_ashan = products[products['shop_rus'] == 'Ашан'].copy()
    # Добавляются цены в итоговую выборку, в соответвсии с очищенным именем товара и магазином
    processed_products = processed_products.merge(products_perekrestok[[
                                                  'name_clear', 'price']], how='left', on='name_clear', suffixes=('_perekrestok', ''))
    processed_products = processed_products.merge(products_magnit[[
                                                  'name_clear', 'price']], how='left', on='name_clear', suffixes=('_magnit', '_perekrestok'))
    # Очистка от товаров, встречающихся только в одном магазине и дубликатов
    processed_products = processed_products.dropna(axis=0, how='any')
    processed_products = processed_products.drop_duplicates(subset='name_clear', keep='first')

    return processed_products.reset_index()


class Diagram:

    def top_10_max(df):
        top_10 = df.sort_values(by='price', ascending=False).head(10)
        sns.set_style('white')
        plt.figure(figsize=(7,5))
        sns.barplot(x = 'price', y = 'name', data = top_10, palette='Blues')
        plt.title('10 САМЫХ ДОРОГИХ ПРОДУКТОВ', fontsize=22)
        plt.xlabel('Стоимость', fontsize=16)
        plt.ylabel('Наименование', fontsize=16)
        plt.tick_params(axis='x', labelsize=10)
        plt.tick_params(axis='y', labelsize=10)
        chart_path = 'data_analysis/static/data_analysis/img/max.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

    def top_10_min(df):
        top_10 = df.sort_values(by='price', ascending=True).head(10)
        sns.set_style('white')
        plt.figure(figsize=(7,5))
        sns.barplot(x = 'price', y = 'name', data = top_10, palette='Blues')
        plt.title('10 САМЫХ ДЕШЕВЫХ ПРОДУКТОВ', fontsize=22)
        plt.xlabel('Стоимость', fontsize=16)
        plt.ylabel('Наименование', fontsize=16)
        plt.tick_params(axis='x', labelsize=10)
        plt.tick_params(axis='y', labelsize=10)
        chart_path = 'data_analysis/static/data_analysis/img/min.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

    def pivot_table_mean(df):
        plt.figure(figsize=(10,5))
        pivot_table = df.pivot_table(index='category_general', columns='shop_rus', values='price', aggfunc='mean')
        plt.title('ТЕПЛОВАЯ КАРТА СРЕДНЕЙ СТОИМОСТИ ТОВАРОВ', fontsize=20)
        sns.heatmap(pivot_table, cmap='Blues', annot=True, fmt=".1f")
        plt.xlabel('Магазин', fontsize=16)
        plt.ylabel('Категория', fontsize=16)
        plt.tick_params(axis='x', labelsize=12)
        plt.tick_params(axis='y', labelsize=12)
        chart_path = 'data_analysis/static/data_analysis/img/mean.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

    def pivot_table_mod(df):
        plt.figure(figsize=(10,5))
        pivot_table = df.pivot_table(index='category_general', columns='shop_rus', values='price', aggfunc=lambda x: x.mode().max())
        plt.title('ТЕПЛОВАЯ КАРТА МОДЫ СТОИМОСТИ ТОВАРОВ', fontsize=20)
        sns.heatmap(pivot_table, cmap='Blues', annot=True, fmt=".1f")
        plt.xlabel('Магазин', fontsize=16)
        plt.ylabel('Категория', fontsize=16)
        plt.tick_params(axis='x', labelsize=12)
        plt.tick_params(axis='y', labelsize=12)
        chart_path = 'data_analysis/static/data_analysis/img/mod.png'
        plt.savefig(chart_path,  bbox_inches = 'tight')        
        return chart_path

def get_products_queryset():
    # return Product.objects.values('id', 'store__id', 'product_id',
    #                        'name', 'code', 'category', 'category_code', 'price', 'region__id')
    return Product.objects.all().values('id', 'store__id', 'product_id', 'name', 'code', 'category', 'category_code', 'price', 'region__id')

if __name__ == '__main__':

    top_max = Diagram.top_10_max()
    top_min = Diagram.top_10_min()
    mean = Diagram.pivot_table_mean()
    mod = Diagram.pivot_table_mod()
    plt.show()