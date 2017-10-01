import pymysql
import pymysqlpool

mysql_host = '192.168.16.102'
mysql_port = 3306
mysql_user = 'root'
mysql_password = '111'
mysql_db = 'db'

def create_conn():
    return pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_db,
                    charset='utf8', autocommit=True)


pool = pymysqlpool.Pool(create_instance=create_conn)

conn = pool.get()
cur = conn.cursor()
cur.execute("select 1")
for x in cur:
    print(x)

for x in range(20):
    conn = pool.get()
    print(x)
    if x % 2 == 0:
        conn.close()


cur.close()
conn.close()
pass