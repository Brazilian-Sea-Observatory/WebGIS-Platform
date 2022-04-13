
# coding: utf-8

# In[ ]:


import pandas
from sqlalchemy import create_engine
import psycopg2

##1 - Prepare the file to read with panda
##2 - Filter Only Stations with TEMP and PSAL as parameter
##3 - Export to SQL

###################### ** ######################

#Original Fields
## platform_code,creation_date,update_date,wmo_platform_code,data_source,institution,
#institution_edmo_code,parameters,last_latitude_observation,last_longitude_observation,last_date_observation 


##Read CSV With Necessary Conditions
interest_fields = ['# platform_code', 'creation_date', 'update_date', 'last_date_observation ', 
                              'parameters', 'last_latitude_observation','last_longitude_observation']

df = pandas.read_csv('index_platform.txt', 
                     skiprows = 5,
                     usecols= interest_fields,
                     index_col='# platform_code',
                     parse_dates=['creation_date', 'update_date', 'last_date_observation '])
#                      usecols['platform_code', 'creation_date', 'update_date', 'last_date_observation'],
#                      index_col='platform_code',
#                      parse_dates=['creation_date', 'update_date', 'last_date_observation '],


##Filter with parameters interest
interestParams = 'PSAL|TEMP'
hasInterestParams = df['parameters'].str.contains(interestParams, regex=True)
df_filter = df[hasInterestParams]

df_filter['test'] = 2.000

print("Total of Rows Readed: " + str(df.shape[0]) + " \nRows who have the interest: " + str(df_filter.shape[0])) 

##Export to SQL 

# try:
#    connection = psycopg2.connect(user="postgres",
#                                   password="",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="platform_insitu")
#    cursor = connection.cursor()
#    postgres_insert_query = """ INSERT INTO new_table_test (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
#    record_to_insert = (5, 'One Plus 6', 950)
#    cursor.execute(postgres_insert_query, record_to_insert)
#    connection.commit()
#    count = cursor.rowcount
#    print (count, "Record inserted successfully into mobile table")
# except (Exception, psycopg2.Error) as error :
#     if(connection):
#         print("Failed to insert record into mobile table", error)
# finally:
#     #closing database connection.
#     if(connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")


engine = create_engine('postgresql://postgres:postgres@db:5432/platform_insitu')
df_filter.to_sql(name='platforms',con=engine,if_exists='replace')
# df=pd.DataFrame(['A','B'],columns=['new_tablecol'])
# df_filter.to_sql(name='new_table_test',con=engine,if_exists='replace')


