import sqlite3

#takes a rin/id tuple and connection ubject
def add_to_database(rin_id, conn):
    if type(rin_id) != tuple:
        raise TypeError('%s is not a tuple' % type(rin_id))
    if len(rin_id) != 2:
        raise TypeError('rin_id is not of length 2')
    c = conn.cursor()
    c.execute("INSERT INTO rin__testing_id VALUES (?, ?)", (rin_id[0], rin_id[1]))
    conn.commit()


conn = sqlite3.connect('test.db')

c = conn.cursor()

try:
    c.execute('CREATE TABLE rin__testing_id (rin text unique, testing_id text unique)')
except sqlite3.OperationalError as e:
    pass

add_to_database(('a','b'),conn)

#testing
c.execute('SELECT * FROM rin__testing_id')
print (c.fetchall())

conn.close()
