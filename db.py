import sqlite3

class DB:
    
    DB_PATH = "/home/david/udemy-current/data.db"


    @classmethod
    def get_connection(cls):
        
        cn = sqlite3.connect(cls.DB_PATH)
        cursor = cn.cursor()
        return cn, cursor


    @classmethod
    def get_connection_read_only(cls):
        path = "file:" + cls.DB_PATH + "?mode=ro"
        cn = sqlite3.connect(path, uri=True)
        cursor = cn.cursor()
        return cn, cursor
    

    @classmethod
    def close_connection(cls, cn, commit):
        
        if cn:
            if commit:
                cn.commit()
            else:
                cn.rollback()
            cn.close()
            cn = None

    
    @classmethod
    def close_connection_read_only(cls, cn):
        if cn:
            cn.close()
            cn = None


    def set_DB(cls, path):

        cls.DB_PATH = path
        