from builtins import staticmethod

from masters import db
from datetime import datetime
from pytz import *


class IdGeneratorModel(db.Model):
    __tablename__ = 'idGenerator'

    idKey = db.Column(db.String(10), unique=True, primary_key=True)
    idValue = db.Column(db.Integer)
    createdDate = db.Column(db.DateTime(timezone=True))
    modifiedDate = db.Column(db.DateTime(timezone=True))

    @staticmethod
    def getnewid(key):

        idgenerator = IdGeneratorModel.query.filter_by(idKey=key).first()

        eastern = timezone('Europe/London')
        loc_dt = eastern.localize(datetime.now())

        if idgenerator is None:
            newidgenerator = IdGeneratorModel(
                idKey=key,
                idValue=1,
                createdDate=loc_dt
            )
            db.session.add(newidgenerator)
            db.session.commit()
            idgenerator = newidgenerator;
        else:
            value = idgenerator.idValue + 1;

            idgenerator.idValue = value;
            idgenerator.modifiedDate = loc_dt;

            db.session.add(idgenerator)
            db.session.commit()

        return idgenerator.idKey + "" + idgenerator.idValue.__str__();
