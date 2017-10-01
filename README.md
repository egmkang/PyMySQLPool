This `Pool` is very simple, you can use it as usual.
```
def create_conn():
    return pymysql.connect(host=mysql_host, port=mysql_port, 
                    user=mysql_user, password=mysql_password,
                    database=mysql_db, charset='utf8',
                    autocommit=True)
pool = pymysqlpool.Pool(create_instance=create_conn)

conn = pool.get()
cur = conn.cursor()
cur.execute("select 1")
for x in cur:
    pass
cur.close()
conn.close()
```