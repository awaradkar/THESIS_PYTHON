from run import db
from datetime import datetime
from pytz import *
from wareDep.idGenerator import model_id
from wareDep.deposit import models_dep


class WithdrawalModel(db.Model):
    __tablename__ = 'withdrawal'

    withdrawalId = db.Column(db.String(10), unique=True, primary_key=True)
    depositId = db.Column(db.String(10))
    txnId = db.Column(db.String(100), unique=True, nullable=False)
    clientId = db.Column(db.String(512))
    clientName = db.Column(db.String(512))
    warehouseCode = db.Column(db.String(512))
    warehouseName = db.Column(db.String(512))
    commodityCode = db.Column(db.String(512))
    commodityName = db.Column(db.String(512))
    uomCode = db.Column(db.String(512))
    packType = db.Column(db.String(512))
    active = db.Column(db.String(512))
    status = db.Column(db.String(512))
    withDrawalNoOfBags = db.Column(db.Float(Precision='25,5'))
    withdrawalQuantity = db.Column(db.Float(Precision='25,5'))
    withdrawalDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdBy = db.Column(db.String(512))
    modifiedBy = db.Column(db.String(512))


def save_to_db(self):
    withdrawal = self

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    mainsession = db.session;

    deposit = models_dep.DepositModel.find_by_depid_for_withdrawal(withdrawal.depositId)
    depQty = deposit.currenyQty;
    depPacks = deposit.currentPacks

    depQty = depQty - withdrawal.withdrawalQuantity
    depPacks = depPacks - withdrawal.withDrawalNoOfBags

    deposit.currenyQty = depQty
    deposit.currentPacks = depPacks

    if depQty ==0 | depPacks == 0:
        deposit.active = "N"

    models_dep.DepositModel.update_after_deposit(deposit, mainsession);

    withdrawal.withdrawalDate = eastern.localize(datetime.strptime(withdrawal.withdrawalDate,'%Y-%m-%d'));
    withdrawal.depositId = model_id.getNewId("WDH", mainsession)
    withdrawal.txnId = model_id.getNewId("TXN", mainsession)

    withdrawal.createdDate = loc_dt
    mainsession.add(withdrawal)
    mainsession.commit()


@classmethod
def update_to_db(cls, self):
    withdrawal = self;

    dbwithdrawal = cls.query.filter_by(withdrawalId=withdrawal.withdrawalId).first()

    if "CANCELLED" == withdrawal.status:
        dbwithdrawal.active = "N"

    mainsession = db.session;

    deposit = models_dep.DepositModel.find_by_depid_for_withdrawal(withdrawal.depositId)

    depQty = deposit.currenyQty;
    depPacks = deposit.currentPacks

    depQty = depQty + withdrawal.withdrawalQuantity
    depPacks = depPacks + withdrawal.withDrawalNoOfBags

    deposit.currenyQty = depQty
    deposit.currentPacks = depPacks

    if "N" == deposit.active:
        deposit.active = "Y"

    models_dep.DepositModel.update_after_deposit(deposit,mainsession);

    dbwithdrawal.status = withdrawal.status
    dbwithdrawal.modifiedBy = withdrawal.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dbwithdrawal.modifiedDate(loc_dt);

    db.session.add(dbwithdrawal)
    db.session.commit()


@classmethod
def find_by_withdrawalid(cls, withdrawalId):
    def to_json(x):
        return {
            'withdrawalId': x.withdrawalId,
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
            'withDrawalNoOfBags':x.withDrawalNoOfBags,
            'withdrawalQuantity':x.withdrawalQuantity,
            'withdrawalDate':x.withdrawalDate,
            'createdDate':x.createdDate,
            'modifiedDate':x.modifiedDate,
            'createdBy':x.createdBy,
            'modifiedBy':x.modifiedBy
        }
    withdrawal = cls.query.filter_by(withdrawalId=withdrawalId).first()
    return to_json(withdrawal);


@classmethod
def return_all(cls):
    def to_json(x):
        return {
            'withdrawalId': x.withdrawalId,
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
            'withDrawalNoOfBags':x.withDrawalNoOfBags,
            'withdrawalQuantity':x.withdrawalQuantity,
            'withdrawalDate':x.withdrawalDate,
            'createdDate':x.createdDate,
            'modifiedDate':x.modifiedDate,
            'createdBy':x.createdBy,
            'modifiedBy':x.modifiedBy
        }
    return {'withdrawals': list(map(lambda x: to_json(x), WithdrawalModel.query.all()))}


@classmethod
def delete_by_withdrawalid(cls, withdrawalId):
    try:
        obj = WithdrawalModel.query.filter_by(withdrawalId=withdrawalId).one()
        db.session.delete(obj)
        db.session.commit()
        return {'message': 'Withdrawal deleted successfully'}
    except:
        return {'message': 'Something went wrong'}