from run import db
from datetime import datetime
from pytz import *


class IdGeneratorModel(db.Model):
    __tablename__ = 'idGenerator'

    idKey = db.Column(db.String(10), unique=True, primary_key=True)
    idValue = db.Column(db.Integer(100))
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)

@classmethod
def getNewId(cls,key,mainSession):
    idGenerator = cls.query.filter_by(key=key).first()

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    if idGenerator is None:
        newIdGenerator = IdGeneratorModel(
            idKey = key,
            idValue = 1,
            createdDate = loc_dt
        )
        mainSession.add(newIdGenerator)
        idGenerator = newIdGenerator;
    else:
        value = idGenerator.idValue+1;

        idGenerator.idValue = value;
        idGenerator.modifiedDate = loc_dt;

        mainSession.add(idGenerator)

    return idGenerator.idKey+""+idGenerator.idValue;