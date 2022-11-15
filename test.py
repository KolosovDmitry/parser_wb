from lib_wb import WB_Seller
import datetime
import numpy as np
import pandas as pd
import random

#u = []
#for id in range(922000,924000):
#    u.append(id)

u = [id for id in range(32000,32020)]
print(u)
n = tuple(u)

URL_USER_LIST = ('29130','37424','2')
datetime_object = datetime.datetime.now()
wb_u = WB_Seller(n)


df_u = wb_u.get_list_url()


df_u['Дата регистрации'] = df_u['Дата регистрации'].astype('datetime64[ns]')
df_u['Срок жизни'] = ((datetime_object - df_u['Дата регистрации'])/np.timedelta64(1, 'M'))
df_u['Срок жизни'] = np.round(df_u['Срок жизни'], decimals = 0)
df_u['Срок жизни'] = df_u['Срок жизни'].astype("Int64")
df_u['Проданно товаров'] = df_u['Проданно товаров'].astype(int)
df_u['Среднее к-во продаж в месяц'] =  df_u['Проданно товаров'] / df_u['Срок жизни']
df_u['Среднее к-во продаж в месяц'] = df_u['Среднее к-во продаж в месяц'].astype("float64")
df_u['Среднее к-во продаж в месяц'] = np.round(df_u['Среднее к-во продаж в месяц'], decimals = 1)

print(df_u)
#df_u.to_excel('test.xlsx')
