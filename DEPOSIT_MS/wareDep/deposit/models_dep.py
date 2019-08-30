from run import db
from datetime import datetime
from pytz import *
from wareDep.idGenerator import model_id


class DepositModel(db.Model):
    __tablename__ = 'deposit'

    depositId = db.Column(db.String(10), unique=True, primary_key=True)
    txnId = db.Column(db.String(100), unique=True, nullable=False)
    clientId = db.Column(db.String(10))
    clientName = db.Column(db.String(100))
    warehouseCode = db.Column(db.String(10))
    warehouseName = db.Column(db.String(100))
    commodityCode = db.Column(db.String(10))
    commodityName = db.Column(db.String(100))
    uomCode = db.Column(db.String(10))
    packType = db.Column(db.String(100))
    active = db.Column(db.String(10))
    status = db.Column(db.String(20))
    noOfBags = db.Column(db.Float(Precision='25,5'))
    quantity = db.Column(db.Float(Precision='25,5'))
    netQuantity = db.Column(db.Float(Precision='25,5'))
    currenyQty = db.Column(db.Float(Precision='25,5'))
    currentPacks = db.Column(db.Float(Precision='25,5'))
    depositDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)
    lastBilledDate = db.Column(db.DateTime(timezone=True), nullable=False)
    billingType = db.Column(db.String(10));
    createdBy = db.Column(db.String(20))
    modifiedBy = db.Column(db.String(20))


def save_to_db(self):
    deposit = self

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    mainSession = db.session;

    deposit.depositId = model_id.getNewId("DEP", mainSession)
    deposit.txnId = model_id.getNewId("TXN", mainSession)

    deposit.createdDate(loc_dt);
    deposit.depositDate = eastern.localize(datetime.strptime(deposit.depositDate, '%Y-%m-%d'));

    mainSession.add(deposit)
    mainSession.commit()


@classmethod
def update_to_db(cls, self):
    updateDep = self;

    dbdeposit = cls.query.filter_by(depositId=updateDep.depositId).first()

    dbdeposit.status = updateDep.status
    dbdeposit.modifiedBy = updateDep.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dbdeposit.modifiedDate(loc_dt);

    db.session.add(dbdeposit)
    db.session.commit()


@classmethod
def update_after_deposit(cls, self, session):
    updateDep = self;

    dbdeposit = cls.query.filter_by(depositId=updateDep.depositId).first()

    dbdeposit.active = updateDep.active
    dbdeposit.currenyQty = updateDep.currenyQty
    dbdeposit.currentPacks = updateDep.currentPacks
    dbdeposit.modifiedBy = updateDep.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dbdeposit.modifiedDate(loc_dt);

    session.add(dbdeposit)



@classmethod
def find_by_depid(cls, depId):
    def to_json(x):
        return {
            'depositId':x.depositId,
            'txnId':x.txnId,
            'clientId':x.clientId,
            'clientName':x.clientName,
            'warehouseCode':x.warehouseCode,
            'warehouseName':x.warehouseName,
            'commodityCode':x.commodityCode,
            'commodityName':x.commodityName,
            'uomCode':x.uomCode,
            'packType':x.packType,
            'active':x.active,
            'status':x.status,
            'noOfBags':x.noOfBags,
            'quantity':x.quantity,
            'netQuantity':x.netQuantity,
            'currenyQty':x.currenyQty,
            'currentPacks':x.currentPacks,
            'depositDate':x.depositDate,
            'createdDate':x.createdDate,
            'modifiedDate':x.modifiedDate,
            'createdBy':x.createdBy,
            'modifiedBy':x.modifiedBy
        }
    deposit = cls.query.filter_by(depositId=depId).first()
    return to_json(deposit);

@classmethod
def find_by_depid_for_withdrawal(cls, depId):
    deposit = cls.query.filter_by(depositId=depId).first()
    return deposit

@classmethod
def return_all(cls):
    def to_json(x):
        return {
            'depositId':x.depositId,
            'txnId':x.txnId,
            'clientId':x.clientId,
            'clientName':x.clientName,
            'warehouseCode':x.warehouseCode,
            'warehouseName':x.warehouseName,
            'commodityCode':x.commodityCode,
            'commodityName':x.commodityName,
            'uomCode':x.uomCode,
            'packType':x.packType,
            'active':x.active,
            'status':x.status,
            'noOfBags':x.noOfBags,
            'quantity':x.quantity,
            'netQuantity':x.netQuantity,
            'currenyQty':x.currenyQty,
            'currentPacks':x.currentPacks,
            'depositDate':x.depositDate,
            'createdDate':x.createdDate,
            'modifiedDate':x.modifiedDate,
            'createdBy':x.createdBy,
            'modifiedBy':x.modifiedBy
        }
    return {'deposits': list(map(lambda x: to_json(x), DepositModel.query.all()))}


@classmethod
def delete_by_depid(cls, depid):
    try:
        obj = DepositModel.query.filter_by(depositid=depid).one()
        db.session.delete(obj)
        db.session.commit()
        return {'message': 'Deposit deleted successfully'}
    except:
        return {'message': 'Something went wrong'}