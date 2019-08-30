from datetime import datetime

from billing.models_bill import IdGeneratorModel
from billing.dbConnection import Connection


class IdGeneratorDao:

    def getnewid(key):

        idGenerator = IdGeneratorModel()

        try:
            conn = Connection.connection()

            selectsql = """SELECT idKey, idValue from ID_GENERATOR where idKey = %s"""

            cursor = conn.cursor()
            select_tuple = {key}

            cursor.execute(selectsql, select_tuple)
            row = cursor.fetchone()

            if cursor.rowcount>0:
                idGenerator.idKey = row[0]
                idGenerator.idValue = row[1]+1

                updateSql = "update ID_GENERATOR set idValue = %s, modifiedDate = %s where idKey = %s";
                select_tuple_upd = {idGenerator.idValue, datetime.now(),idGenerator.idKey}
                cursor.close();
                cursor = conn.cursor()
                cursor.execute(updateSql, select_tuple_upd)
            else:
                idGenerator.idKey = key
                idGenerator.idValue = 1
                insertSql = "insert into ID_GENERATOR (idKey, idValue, createdDate) values (%s,%s,%s)";
                select_tuple_upd = {idGenerator.idKey,idGenerator.idValue, datetime.now()}
                cursor.close();
                cursor = conn.cursor()
                cursor.execute(insertSql, select_tuple_upd)

            cursor.close()
            conn.close()
            return  idGenerator;

        except:
            return {'message': 'Something went wrong'}, 500
