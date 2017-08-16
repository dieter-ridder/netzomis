import sqlite3

DATABASE="netzomi.sqlite"

class DBHelper:
    def __init__(self, dbname=DATABASE):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # Table: Student
    # Columns: studentId, chatId - integer
    # os: iOS, Android
    # mailAddress: text
    # current course - integer
    # recent step -  integer
    
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS student (\
           studentId integer, \
           chatId integer, \
           os text, \
           device text, \
           mailAddress text, \
           currentCourse text, \
           recentStep integer\
           lastContact numeric\
           CONSTRAINT studentPK PRIMARY KEY (studentId))"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO items (description) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]