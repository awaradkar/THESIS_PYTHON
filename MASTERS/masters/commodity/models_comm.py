
import threading
from builtins import print

from masters import db
from datetime import datetime
from pytz import *
from masters.idGenerator.model_id import IdGeneratorModel
import sys

lock = threading.RLock()
class CommModel(db.Model):
    __tablename__ = 'commodity'

    commodityId = db.Column(db.String(10), unique=True, primary_key=True)
    commodityName = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(512))
    uom = db.Column(db.String(512))
    createdDate = db.Column(db.DateTime(timezone=True))
    modifiedDate = db.Column(db.DateTime(timezone=True))
    createdBy = db.Column(db.String(512))
    modifiedBy = db.Column(db.String(512))

    def save(self):
        commodity = self

        print(commodity, file=sys.stderr);

        eastern = timezone('Europe/London')
        loc_dt = eastern.localize(datetime.now())
        idGenerator = IdGeneratorModel();

        lock.acquire()
        commodity.commodityId = idGenerator.getnewid("COM")
        lock.release()

        commodity.createdDate = loc_dt;

        print(commodity.commodityId, file=sys.stdout);
        print(commodity.createdDate, file=sys.stdout);

        db.session.add(commodity)
        db.session.commit()


    def update_to_db(self):
        updatecomm = self

        print(updatecomm, file=sys.stderr);

        dbcomm = CommModel.query.filter_by(commodityId=updatecomm.commodityId).first()
        print(dbcomm, file=sys.stderr);

        dbcomm.commodityName = updatecomm.commodityName
        dbcomm.description = updatecomm.description
        dbcomm.uom = updatecomm.uom
        dbcomm.modifiedBy = updatecomm.modifiedBy

        eastern = timezone('Europe/London')
        loc_dt = eastern.localize(datetime.now())

        dbcomm.modifiedDate=loc_dt;
        db.session.commit()

    @staticmethod
    def find_by_commodityname(commodityname):
        return CommModel.query.filter_by(commodityName=commodityname).first()

    @staticmethod
    def find_by_commid(commid):
        print(commid, file=sys.stdout);
        x = CommModel.query.filter_by(commodityId=commid).first();

        commodity = {
            'commodityId': x.commodityId,
            'commodityName': x.commodityName,
            'description': x.description,
            'uom': x.uom,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }

        return commodity;

    @staticmethod
    def return_all():
        def to_json(x):
            return {
                'commodityId': x.commodityId,
                'commodityName': x.commodityName,
                'description': x.description,
                'uom': x.uom,
                'createdDate': x.createdDate,
                'modifiedDate': x.modifiedDate,
                'createdBy': x.createdBy,
                'modifiedBy': x.modifiedBy
            }
        return {'commodities': list(map(lambda x: to_json(x), CommModel.query.all()))}

    @staticmethod
    def delete_by_commid(commId):
        try:
            obj = CommModel.query.filter_by(commodityId=commId).first()
            db.session.delete(obj)
            db.session.commit()
            return {'message': 'Commodity deleted successfully'}
        except:
            return {'message': 'Something went wrong'}
