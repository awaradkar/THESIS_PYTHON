import pymysql

class Connection:

    def connection(self):

        host = "http://localhost:3306/deposit_py"
        user = "anirudh"
        password = "Mumbai123"
        db = "mysql"

        conn = pymysql.connect(host=host, user=user, passwd=password, db=db);

        return conn
