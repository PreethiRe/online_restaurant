
import MySQLdb


user = "LKwknKWfkf"
database = "LKwknKWfkf"
password = "we5iXO6R7B"
host="remotemysql.com"

class MysqlConnection:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        self.conn = MySQLdb.connect(host, user, password,
                                    database)





