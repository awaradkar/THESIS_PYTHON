from run import db
from datetime import datetime
from pytz import *
from masters.idGenerator import model_id


class PackModel(db.Model):
    __tablename__ = 'packs'

    packId = db.Column(db.String(10), unique=True, primary_key=True)
    packType = db.Column(db.String(100))
    packDeduction = db.Column(db.Float(512))
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdBy = db.Column(db.String(512))
    modifiedBy = db.Column(db.String(512))


def save_to_db(self):
    pack = self

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    pack.packId = model_id.getNewId("PACK")
    pack.createdDate(loc_dt);
    db.session.add(pack)
    db.session.commit()


@classmethod
def update_to_db(cls, self):
    updatepack = self;

    dbpack = cls.query.filter_by(packId=updatepack.packId).first()

    dbpack.packType = updatepack.packType
    dbpack.packType = updatepack.packType
    dbpack.modifiedBy = updatepack.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dbpack.modifiedDate(loc_dt);

    db.session.add(dbpack)
    db.session.commit()


@classmethod
def find_by_packid(cls, packid):
    def to_json(x):
        return {
            'packId': x.packId,
            'packType': x.packType,
            'packDeduction': x.packDeduction,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }
    pack = cls.query.filter_by(packid=packid).first()
    return to_json(pack);


@classmethod
def return_all(cls):
    def to_json(x):
        return {
            'packId': x.packId,
            'packType': x.packType,
            'packDeduction': x.packDeduction,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }
    return {'packs': list(map(lambda x: to_json(x), PackModel.query.all()))}


@classmethod
def delete_by_packid(cls, packid):
    try:
        obj = PackModel.query.filter_by(packId=packid).one()
        db.session.delete(obj)
        db.session.commit()
        return {'message': 'Pack deleted successfully'}
    except:
        return {'message': 'Something went wrong'}