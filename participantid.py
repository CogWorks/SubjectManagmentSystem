import sqlite3
import participant_gui
from tkinter import Tk

#takes a rin/id tuple and connection ubject
def add_to_database(rin_id, conn):
    if type(rin_id) != tuple:
        raise TypeError('%s is not a tuple' % type(rin_id))
    if len(rin_id) != 2:
        raise TypeError('rin_id is not of length 2')
    c = conn.cursor()
    c.execute("INSERT INTO rin__testing_id VALUES (?, ?)", (rin_id[0], rin_id[1]))
    conn.commit()

def connect_to_database(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE rin__testing_id (rin text unique, testing_id text unique)')
    except sqlite3.OperationalError as e:
        pass
    return conn

#gui startup
app = participant_gui.App_Gui()
app.mainloop()


#testing
# conn = connect_to_database('test.db')
# c = conn.cursor()
#
# c.execute('SELECT * FROM rin__testing_id')
# print (c.fetchall())
#
# conn.close()
