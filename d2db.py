import sqlite3

class d2db:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.cur.close()
        self.conn.close()

    def query(self, definition, hash_id):
        query = "SELECT json FROM {} WHERE id={}"       
        self.cur.execute(query.format(definition, hash_id))
        return (self.cur.fetchall())

    

