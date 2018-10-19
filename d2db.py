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
        return (self.cur.fetchone())

    #Finds what table an ID/Hash belongs to
    def find_id_table(self, hash_id):
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for tr in self.cur.fetchall():
            table = tr[0]
            query = "SELECT * FROM {} WHERE id=?"
            if(table == "DestinyHistoricalStatsDefinition"):
                query = "SELECT * FROM {} WHERE key=?"
            self.cur.execute(query.format(table), (hash_id,))
            for row in self.cur:
                for field in row.keys():
                    print(table, field, row[field])



    

