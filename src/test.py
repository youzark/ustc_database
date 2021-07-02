import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
print ("Opened database successfully")
'''
sql = "create table accounts (id integer primary key autoincrement,user_name string  unique not null,password string not null);"
c.execute(sql)
conn.commit()
sql = "insert into accounts (user_name,password) values('Wchlove','wuchenghui')"
c.execute(sql)
sql = "insert into accounts (user_name,password) values('War','war')"
c.execute(sql)
sql = "insert into accounts (user_name,password) values('Nkj','nkj')"
c.execute(sql)
conn.commit()
print ("Records created successfully")

usr = 'xyz'
passwd = 'xyz'
sql ='insert into accounts (user_name,password) values(?,?)'
c.execute(sql,[usr,passwd])
conn.commit()
print ("Records created successfully")
'
sql = 'select password from accounts where id=?'
cursor = c.execute(sql,[3])

for row in cursor:
    #print ("id = ", row[0])
    #print ("user_name = ", row[1])
    print ("password = ", row[0],"\n" )

res = c.fetchone()
print(res[0])
print ("Operation done successfully")

sql = "drop table video;"
c.execute(sql)
conn.commit()

sql = "create table video (id integer primary key autoincrement,name string ,path string not null ,user_name string not null,time string not null);"
c.execute(sql)

sql = 'drop table Comment;'
c.execute(sql)
conn.commit()
sql = 'create table Comment (comment_id integer primary key autoincrement,comment string not null,video_id integer ,user_name string not null,time string not null);'
c.execute(sql)
'''
sql = 'create table emails(email_id integer primary key autoincrement,send_user string not null,receive_user string not null,message string not null,time string not null)'
c.execute(sql)
sql = 'create table friends(relation integer primary key autoincrement,owner_name string not null,servant_name string not null)'
c.execute(sql)
conn.commit()
conn.close()