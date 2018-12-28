import pyodbc

db_path = 'exercise1'
con_str = f"DRIVER={{MySQL ODBC 8.0 ANSI Driver}};SERVER=localhost; USER=root; Password=ketty7; DATABASE={db_path};Trusted_connection=yes"
conn = pyodbc.connect(con_str)
cursor = conn.cursor()

print('enter SEC_CODE:')
SEC_CODE = input()
print('SEC_CODE:', )

print('enter timestamp:')
timestamp = input()
print('timestamp:', timestamp)

sql_query1 = f'select PRICE, VOLUME from Orderlog where SECCODE="{SEC_CODE}" and BUYSELL="S" and time <={timestamp} ' \
    f'and PRICE > 0 group by PRICE order by PRICE DESC'
cursor.execute(sql_query1)
result1 = cursor.fetchmany(15000)
print(result1)

sql_query2 = f'select PRICE, VOLUME from Orderlog where SECCODE="{SEC_CODE}" and BUYSELL="B" and time <={timestamp} ' \
    f'and PRICE > 0 group by PRICE order by PRICE DESC'
cursor.execute(sql_query2)
result2 = cursor.fetchmany(15000)
print(result2)

best_bids = sorted(result2, key=lambda n: -n[0])[:10]
best_asks = sorted(result1, key=lambda n: n[0])[:10]
print('best_bids:', best_bids)
print('best_asks:', best_asks)

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

bid_ask_spread = max(x1)-min(y1)
print('bid_ask_spread:', bid_ask_spread)

import matplotlib.pyplot as plt
plt.bar(*zip(*best_asks),label='Ask',color='red')
plt.bar(*zip(*best_bids),label='Bid', color='green')
plt.ylabel('Volume')
plt.xlabel('Price')
plt.title('Depth of Market')
plt.legend(loc='upper left')
plt.show()




