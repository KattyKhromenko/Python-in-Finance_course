# соединение Python и MySQL по pyodbc
import pyodbc

db_path = 'exercise1'
con_str = f"DRIVER={{MySQL ODBC 8.0 ANSI Driver}};SERVER=localhost; USER=root; Password=ketty7; DATABASE={db_path};Trusted_connection=yes"
conn = pyodbc.connect(con_str)
cursor = conn.cursor()

#Код предлагает пользователю ввести тикер
print('enter SEC_CODE:')
SEC_CODE = input()
print('SEC_CODE:', )

#Код предлагает пользователю ввести период времени
print('enter timestamp:')
timestamp = input()
print('timestamp:', timestamp)

#Запрос в MySQL возвращает поток заявок со стороны Sell по указанному тикеру и до заданного момента времени
sql_query1 = f'select PRICE, VOLUME from Orderlog where SECCODE="{SEC_CODE}" and BUYSELL="S" and time <={timestamp} ' \
    f'and PRICE > 0 group by PRICE order by PRICE DESC'
cursor.execute(sql_query1)
result1 = cursor.fetchmany(15000)
print(result1)

#Запрос в MySQL возвращает поток заявок со стороны Buy по указанному тикеру и до заданного момента времени
sql_query2 = f'select PRICE, VOLUME from Orderlog where SECCODE="{SEC_CODE}" and BUYSELL="B" and time <={timestamp} ' \
    f'and PRICE > 0 group by PRICE order by PRICE DESC'
cursor.execute(sql_query2)
result2 = cursor.fetchmany(15000)
print(result2)

#Отбор наилучших 10 заявок Bid и Ask
best_bids = sorted(result2, key=lambda n: -n[0])[:10]
best_asks = sorted(result1, key=lambda n: n[0])[:10]
print('best_bids:', best_bids)
print('best_asks:', best_asks)

#Визуализация стакана
from prettytable import PrettyTable
y = PrettyTable()
x = PrettyTable()
y1, y2 = zip(*best_asks)
x1, x2 = zip(*best_bids)
y.add_column("price", y1)
y.add_column("volume",y2)
x.add_column("price", x1)
x.add_column("volume", x2)
print(y)
print(x)

#Расчет bid-ask spread
bid_ask_spread = max(x1)-min(y1)
print('bid_ask_spread:', bid_ask_spread)

#Гистограмма на лучших ценах покупки и продажи
import matplotlib.pyplot as plt
plt.bar(*zip(*best_asks),label='Ask',color='red')
plt.bar(*zip(*best_bids),label='Bid', color='green')
plt.ylabel('Volume')
plt.xlabel('Price')
plt.title('Depth of Market')
plt.legend(loc='upper left')
plt.show()




