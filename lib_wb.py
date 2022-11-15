import re
from lxml import html
import requests
import pandas as pd
import numpy as np
import json



class WB_Seller(object):
    """Класс сбора информации о прадавце WB. WB_seller."""


    def __init__(self, id_list):
        self.URL_USER = 'https://www.wildberries.ru/webapi/seller/data/short/%s'
        self.URL_RATING = 'https://suppliers-shipment.wildberries.ru/api/v1/suppliers/%s'
        self.id_list = id_list
        self.HEADERS_USER =  { 'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'ru,en;q=0.9,la;q=0.8',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.710 Yowser/2.5 Safari/537.36',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest',
                    'x-spa-version': '9.3.58.1'
                    }

        self.HEADERS_RATING = {
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                    'x-client-name': 'site'
        }


    def get_status(r):
        r = requests.get(self.url ,headers=self.headers)
        status = r.status_code
        return status

    def get_json(self):
        r = requests.get(self.url ,headers=self.headers)
        self.data = json.loads(r.text)
        return self.data

    def get_df(self):
        #print(type(self.data))
        d = self.data
        df = pd.DataFrame()
        df = df.append(d, ignore_index=True)
        return df

    def get_list_url(self):
        r_list = []
        u_list = []
        
        #print(self.id_list)
        for url in [self.URL_USER % i for i in self.id_list]:

            r_u = requests.get(url ,headers=self.HEADERS_USER)
            u_list.append(json.loads(r_u.text))
            
        df_u = pd.DataFrame()
        df_u = df_u.append(u_list, ignore_index=True)
        df_u['id'] = df_u['id'].astype("Int64")
        df_u.rename(columns = {'name':'Наименование','trademark':'Товарный знак','ogrn':'ОГРН',}, inplace = True)
        #print(df_u)

        for url in [self.URL_RATING % i for i in self.id_list]:
            k = 1 
            id = url.rsplit('/', 1)
            r_r = requests.get(url ,headers=self.HEADERS_RATING)
            status = r_r.status_code
            data = json.loads(r_r.text)
           
            if status == 200:
                if not data.get("id", None):
                    data = {'id': str(id),'saleItemQuantity':'1'}
                    
                    r_list.append(data)
                else:
                    r_list.append(data)
        print(r_list)
        df_r = pd.DataFrame()
        df_r = df_r.append(r_list, ignore_index=True)
        df_r['id'] = df_r['id'].astype("Int64")#.replace('.0','')
        df_r.rename(columns = {'saleItemQuantity': 'Проданно товаров', 'registrationDate':'Дата регистрации','valuation':'Рейтинг','feedbacksCount':'Отзывов'}, inplace = True)

        

        df = df_u.set_index('id').join(df_r.set_index('id'))
        df = df.dropna(subset=['Проданно товаров','deliveryDuration'])
        return df

