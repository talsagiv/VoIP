import sqlite3


conn = sqlite3.connect('test.db')

print "Opened database successfully"



"""conn.execute('''CREATE TABLE USERS
       (NAME           TEXT    NOT NULL,
       PASS            TEXT     NOT NULL,
       ADDR        CHAR(50),
       ONLINE         BOOL     NOT NULL);''')
"""



def add_user(name, password, addr):
    conn.execute("INSERT INTO USERS (NAME, PASS, ADDR, ONLINE) \
      VALUES (" + name + ", " + password + ", " + addr + ", TRUE )")



