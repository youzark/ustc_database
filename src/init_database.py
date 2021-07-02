import sqlite3

conn = sqlite3.connect("./../database/video_platform.db")

c = conn.cursor()
print ("Opened database successfully")

sql = "create table accounts (id integer primary key autoincrement,user_name string  unique not null,password string not null);"
c.execute(sql)
conn.commit()

sql = "create table video (id integer primary key autoincrement,name string ,path string not null ,user_name string not null,time string not null);"
c.execute(sql)
conn.commit()

sql = 'create table Comment (comment_id integer primary key autoincrement,comment string not null,video_id integer ,user_name string not null,time string not null);'
c.execute(sql)
conn.commit()

sql = 'create table emails(email_id integer primary key autoincrement,send_user string not null,receive_user string not null,message string not null,time string not null)'
c.execute(sql)
conn.commit()

sql = 'create table friends(relation integer primary key autoincrement,owner_name string not null,servant_name string not null)'
c.execute(sql)
conn.commit()

conn.close()
