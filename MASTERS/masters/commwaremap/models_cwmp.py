from masters import db
from datetime import datetime
from pytz import *
from masters.idGenerator import model_id


class WareCommMapModel(db.Model):
    __tablename__ = 'ware_comm_map'

    wareCommId = db.Column(db.String(10), unique=True, primary_key=True)
    warehouseCode = db.Column(db.String(100))
    commodityCode = db.Column(db.Float(512))
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdBy = db.Column(db.String(512))
    modifiedBy = db.Column(db.String(512))


def save_to_db(self):
    commwaremap = self

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    commwaremap.wareCommId = model_id.getNewId("WCM")
    commwaremap.createdDate= loc_dt;
    db.session.add(commwaremap)
    db.session.commit()


def update_to_db(cls, self):
    updatepcommwaremap = self;

    dbcommwaremap = WareCommMapModel.query.filter_by(wareCommId=updatepcommwaremap.wareCommId).first()

    dbcommwaremap.warehouseCode = dbcommwaremap.warehouseCode
    dbcommwaremap.commodityCode = dbcommwaremap.commodityCode
    dbcommwaremap.modifiedBy = dbcommwaremap.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dbcommwaremap.modifiedDate=loc_dt;
    db.session.commit()


@staticmethod
def find_by_warecommid(wareCommId):
    x = WareCommMapModel.query.filter_by(wareCommId=wareCommId).first()
    warecomm =  {
            'wareCommId':x.wareCommId,
            'warehouseCode':x.warehouseCode,
            'commodityCode':x.commodityCode,
            'createdDate':x.createdDate,
            'modifiedDate':x.modifiedDate,
            'createdBy' :x.createdBy,
            'modifiedBy':x.modifiedBy
            }
    return warecomm;


@staticmethod
def return_all(cls):
    def to_json(x):
        return {
            'wareCommId': x.wareCommId,
            'warehouseCode': x.warehouseCode,
            'commodityCode': x.commodityCode,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }
    return {'commwaremaps': list(map(lambda x: to_json(x), WareCommMapModel.query.all()))}


@staticmethod
def delete_by_commwaremapid(wareCommId):
    try:
        obj = WareCommMapModel.query.filter_by(wareCommId=wareCommId).first()
        db.session.delete(obj)
        db.session.commit()
        return {'message': 'WareCommMap deleted successfully'}
    except:
        return {'message': 'Something went wrong'}