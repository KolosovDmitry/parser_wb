from lib_wb import WB_Seller
import datetime
import numpy as np
import pandas as pd


URL_USER_LIST = ('29130','37424','2')
datetime_object = datetime.datetime.now()
wb_u = WB_Seller(URL_USER_LIST)


df_u = wb_u.get_list_url()

print(df_u)
df_u['Дата регистрации'] = df_u['Дата регистрации'].astype('datetime64[ns]')
df_u['Месяцев'] = ((datetime_object - df_u['Дата регистрации'])/np.timedelta64(1, 'M'))
df_u['Месяцев'] = np.round(df_u['Месяцев'], decimals = 0)
df_u['Месяцев'] = df_u['Месяцев'].astype("Int64")
df_u['Проданно товаров'] = df_u['Проданно товаров'].astype(int)
df_u['Среднее к-во продаж в месяц'] =  df_u['Проданно товаров'] / df_u['Месяцев']
df_u['Среднее к-во продаж в месяц'] = df_u['Среднее к-во продаж в месяц'].astype("Int64")


df_u.to_excel('test.xlsx')
