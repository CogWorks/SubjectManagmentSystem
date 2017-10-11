import sqlite3
from datetime import datetime


password = 'testing'

#takes a rin/id tuple and connection ubject
def add_to_database(rin_id, conn):
    """
    rin_id := (string rin, (sid_year_semester, sid_number)) (55123, (2017b, 1))
    conn := database connection
    """
    #check for duplicates
    c = conn.cursor()
    c.execute("SELECT * FROM rin__sid_id WHERE sid_year_semester=? AND sid_number=?", (rin_id[1][0],rin_id[1][1]))
    if c.fetchone() != None:
        raise sqlite3.OperationalError("That sid already exists in the database")

    c.execute("INSERT INTO rin__sid_id VALUES (?, ?, ?)", (rin_id[0], rin_id[1][0], rin_id[1][1]))
    conn.commit()


def find_sid(rin, conn):
    """
    rin := string rin
    conn := database connection
    returns (year_semester, number)
    """
    c = conn.cursor()
    c.execute("SELECT sid_year_semester, sid_number FROM rin__sid_id WHERE rin=?", rin)
    sid = c.fetchone()
    if sid == None:
        return None

    return tuple(sid)

def next_sid(conn):
    """
    conn := database connection
    returns (year_semester, number) i.e (2017F, 1) or (2016S, 120)
    """
    year = datetime.now().year
    month = datetime.now().month
    if month >= 8:
        month = 'f'
    else:
        month = 's'

    year_semester = "%s%s" %(year, month)
    # find largest number
    c = conn.cursor()
    try:
        c.execute("SELECT MAX(sid_number) FROM rin__sid_id WHERE sid_year_semester = ?", (year_semester,))
        return (year_semester,c.fetchone()[0])
    except sqlite3.OperationalError as e:
        return (year_semester,0)

def connect_to_database(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE rin__sid_id (rin text unique, sid_year_semester text, sid_number int)')
    except sqlite3.OperationalError as e:
        pass
    return conn
